from pydantic import BaseModel

class PedidoRequest(BaseModel):
    sucursal: str
    articulo: str
    cantidad: int