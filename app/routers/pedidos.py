from fastapi import APIRouter, HTTPException, Depends
from app.models.pedido import PedidoRequest
from app.services.ferremas_api import crear_pedido, get_articulo_id, actualizar_stock_articulo
from app.services.local_pedido_store import guardar_pedido_local
from app.auth.role_checker import validar_rol
from app.auth.roles import ROLES
from app.auth.auth_bearer import JWTBearer

router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)
 
@router.post("/nuevo", dependencies=[Depends(JWTBearer())])
def registrar_pedido(pedido: PedidoRequest, payload=Depends(JWTBearer())):
    validar_rol(payload, [ROLES["client"]])

    if pedido.cantidad <= 0:
        raise HTTPException(status_code=400, detail="La cantidad debe ser mayor a 0")

    try:
        # 1. Obtener datos del artículo
        articulo = get_articulo_id(pedido.articulo)
        stock_actual = articulo.get("stock")

        if stock_actual is None:
            raise HTTPException(status_code=500, detail="El artículo no contiene campo 'stock'")

        if stock_actual < pedido.cantidad:
            raise HTTPException(status_code=400, detail="No hay suficiente stock disponible")

        # 2. Crear el pedido en la API
        resultado_pedido = crear_pedido(pedido)

        # 3. Calcular nuevo stock
        nuevo_stock = stock_actual - pedido.cantidad

        # 4. Actualizar stock en la API
        actualizar_stock_articulo(pedido.articulo, nuevo_stock)

        return {
            "mensaje": "Pedido creado y stock actualizado.",
            "resultado": resultado_pedido,
            "stock_restante": nuevo_stock
        }

    except Exception as e:
        # Fallback: guardar localmente si falla la API externa
        resultado_local = guardar_pedido_local(pedido)
        return {
            "mensaje": "Pedido guardado localmente debido a error con la API externa.",
            "resultado": resultado_local,
            "error": str(e)
        }