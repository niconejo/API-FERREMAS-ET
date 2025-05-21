from fastapi import APIRouter, HTTPException, Depends
from app.models.pago import PagoRequest
from app.services.stripe import crear_sesion_pago
from app.auth.auth_bearer import JWTBearer
from app.auth.role_checker import validar_rol
from app.auth.roles import ROLES

router = APIRouter(
    prefix="/pagos",
    tags=["Pagos"]
)

@router.post("/checkout", dependencies=[Depends(JWTBearer())])
def iniciar_pago(pago: PagoRequest, payload=Depends(JWTBearer())):
    #Solo el rol "client" puede acceder a este endpoint
    validar_rol(payload, [ROLES["client"]])

    try:
        url_pago = crear_sesion_pago(
            precio=pago.precio,
            descripcion=pago.descripcion,
            email_cliente=pago.email
        )
        return {"url": url_pago}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))