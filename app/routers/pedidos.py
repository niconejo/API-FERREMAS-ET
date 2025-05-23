from fastapi import APIRouter, HTTPException, Depends
from app.models.pedido import PedidoRequest, PedidoMultipleRequest
from app.services.ferremas_api import crear_pedido, get_articulo_id, actualizar_stock_articulo
from app.services.local_pedido_store import guardar_pedido_local
from app.auth.role_checker import validar_rol
from app.auth.roles import ROLES
from app.auth.auth_bearer import JWTBearer

router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)
#pedido con un solo producto
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
        print("Stock actual:", stock_actual)
        print("Cantidad pedida:", pedido.cantidad)
        nuevo_stock = stock_actual - pedido.cantidad
        print("Nuevo stock a enviar:", nuevo_stock)

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
# pedido con mas de un producto
@router.post("/nuevo-multiple", dependencies=[Depends(JWTBearer())])
def registrar_pedido_multiple(pedido: PedidoMultipleRequest, payload=Depends(JWTBearer())):
    validar_rol(payload, [ROLES["client"]])

    if not pedido.articulos:
        raise HTTPException(status_code=400, detail="Debe incluir al menos un articulo")

    resultados = []
    errores = []

    for item in pedido.articulos:
        try:
            if item.cantidad <= 0:
                raise ValueError(f"La cantidad para {item.articulo} debe ser mayor a 0")

            articulo = get_articulo_id(item.articulo)
            stock_actual = articulo.get("stock")

            if stock_actual is None:
                raise ValueError(f"El artículo {item.articulo} no contiene campo 'stock'")

            if stock_actual < item.cantidad:
                raise ValueError(f"No hay suficiente stock para {item.articulo}")

            resultado_pedido = crear_pedido(PedidoRequest(
                sucursal=pedido.sucursal,
                articulo=item.articulo,
                cantidad=item.cantidad
            ))

            nuevo_stock = stock_actual - item.cantidad
            actualizar_stock_articulo(item.articulo, nuevo_stock)

            resultados.append({
                "articulo": item.articulo,
                "mensaje": "Pedido creado",
                "stock_restante": nuevo_stock
            })

        except Exception as e:
            guardar_pedido_local(PedidoRequest(
                sucursal=pedido.sucursal,
                articulo=item.articulo,
                cantidad=item.cantidad
            ))

            errores.append({
                "articulo": item.articulo,
                "error": str(e)
            })

    return {
        "resultados": resultados,
        "errores": errores
    }