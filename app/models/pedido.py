from pydantic import BaseModel
from typing import List

class PedidoRequest(BaseModel):
    sucursal: str
    articulo: str
    cantidad: int

class PedidoItem(BaseModel):
    articulo: str
    cantidad: int
    
class PedidoMultipleRequest(BaseModel):
    sucursal :str
    articulos: List[PedidoItem]