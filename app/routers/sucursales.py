from fastapi import APIRouter, Path, HTTPException
from app.services.ferremas_api import get_sucursales, get_sucursal_id

router = APIRouter(prefix="/data/sucursales",
                    tags=["Sucursales"])

@router.get("/")
def listar_sucursales():
    return get_sucursales()

@router.get("/{sucursal_id}")
def obtener_sucursal(sucursal_id: str = Path(..., description="ID de la sucursal")):
    try:
        return get_sucursal_id(sucursal_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")