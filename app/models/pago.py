
from pydantic import BaseModel, EmailStr

class PagoRequest(BaseModel):
    descripcion: str
    precio: int  # Monto en CLP
    email: EmailStr
