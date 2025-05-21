from fastapi import APIRouter, Path, HTTPException, Depends
from app.services.ferremas_api import get_articulos, get_articulo_id
from app.auth.auth_bearer import JWTBearer
from app.auth.role_checker import validar_rol
from app.auth.roles import ROLES

router = APIRouter(prefix="/data/articulos",
                    tags=["Articulos"])

@router.get("/", dependencies=[Depends(JWTBearer())])
def listar_articulos(payload=Depends(JWTBearer())):
    # ✅ Solo usuarios con rol 'bodega' pueden acceder
    validar_rol(payload, [ROLES["bodega"]])
    return get_articulos()

@router.get("/{articulo_id}", dependencies=[Depends(JWTBearer())])
def obtener_articulo(
    articulo_id: str = Path(..., description="ID del artículo"),
    payload=Depends(JWTBearer())
):
    validar_rol(payload, [ROLES["bodega"]])
    try:
        return get_articulo_id(articulo_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")