from fastapi import APIRouter, Path, HTTPException
from app.services.ferremas_api import get_articulos, get_articulo_id

router = APIRouter(prefix="/data/articulos",
                    tags=["Articulos"])

@router.get("/")
def listar_articulos():
    return get_articulos()

@router.get("/{articulo_id}")
def obtener_articulo(articulo_id: str = Path(..., description="ID del artículo")):
    try:
        return get_articulo_id(articulo_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")