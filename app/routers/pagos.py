from fastapi import APIRouter, HTTPException
from app.models.pago import PagoRequest
from app.services.stripe import crear_sesion_pago

router = APIRouter(
    prefix="/pagos",
    tags=["Pagos"]
)

@router.post("/checkout")
def iniciar_pago(pago: PagoRequest):
    try:
        url_pago = crear_sesion_pago(
            precio=pago.precio,
            descripcion=pago.descripcion,
            email_cliente=pago.email
        )
        return {"url": url_pago}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))