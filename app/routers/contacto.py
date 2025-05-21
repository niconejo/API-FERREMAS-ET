from fastapi import APIRouter, HTTPException
from app.models.contacto import ContactoRequest
from app.services.contacto_store import guardar_contacto

router = APIRouter(
    prefix="/contacto",
    tags=["Contacto"]
)

@router.post("/")
def enviar_contacto(contacto: ContactoRequest):
    contacto_guardado = guardar_contacto(contacto.dict())
    return {
        "mensaje": "Tu mensaje ha sido enviado al vendedor.",
        "datos": contacto_guardado
    }