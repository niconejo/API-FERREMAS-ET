from fastapi import APIRouter, Depends
from app.models.contacto import ContactoRequest
from app.services.contacto_store import guardar_contacto
from app.auth.auth_bearer import JWTBearer
from app.auth.role_checker import validar_rol
from app.auth.roles import ROLES

router = APIRouter(prefix="/contacto", tags=["Contacto"])
#crea el msj para contactarse
@router.post("/", dependencies=[Depends(JWTBearer())])
def enviar_contacto(contacto: ContactoRequest, payload=Depends(JWTBearer())):
    validar_rol(payload, [ROLES["client"]])
    contacto_guardado = guardar_contacto(contacto.dict())
    return {
        "mensaje": "Tu mensaje ha sido enviado al vendedor.",
        "datos": contacto_guardado
    }