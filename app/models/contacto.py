from pydantic import BaseModel, EmailStr

class ContactoRequest(BaseModel):
    nombre: str
    email: EmailStr
    vendedor_id: str
    mensaje: str