from fastapi import APIRouter, Path, HTTPException, Depends
from app.services.ferremas_api import get_sucursales, get_sucursal_id
from app.auth.auth_bearer import JWTBearer
from app.auth.role_checker import validar_rol
from app.auth.roles import ROLES

router = APIRouter(prefix="/data/sucursales", tags=["Sucursales"])

@router.get("/", dependencies=[Depends(JWTBearer())])
def listar_sucursales(payload=Depends(JWTBearer())):
    validar_rol(payload, [ROLES["client"]])
    return get_sucursales()

@router.get("/{sucursal_id}", dependencies=[Depends(JWTBearer())])
def obtener_sucursal(sucursal_id: str = Path(..., description="ID de la sucursal"), payload=Depends(JWTBearer())):
    validar_rol(payload, [ROLES["client"]])
    try:
        return get_sucursal_id(sucursal_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")