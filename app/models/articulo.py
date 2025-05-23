from sqlmodel import SQLModel, Field
from typing import Optional

class Articulo(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    categoria: str
    subcategoria: str
    nombre: str
    marca: str
    precio: int
    stock: int

class Promocion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    articulo_id: str = Field(foreign_key="articulo.id")

class Novedad(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    articulo_id: str = Field(foreign_key="articulo.id")