from fastapi import APIRouter, HTTPException
from app.models.pedido import PedidoRequest
from app.services.ferremas_api import crear_pedido
from app.services.local_pedido_store import guardar_pedido_local
router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)
## ESTA BUGEADA LA CREACIÓN DE PEDIDOS PARECE, ME DA ERROR 500
## AUNQUE LOS DATOS ESTEN BIEN 
@router.post("/nuevo")
def registrar_pedido(pedido: PedidoRequest):
    if pedido.cantidad <= 0:
        raise HTTPException(status_code=400, detail="La cantidad debe ser mayor a 0")

    try:
        resultado = crear_pedido(pedido)
        return {"mensaje": "Pedido creado correctamente", "resultado": resultado}
    except:
        return guardar_pedido_local(pedido)
   # except Exception as e:
   #    raise HTTPException(status_code=500, detail=str(e))