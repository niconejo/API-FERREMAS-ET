from fastapi import APIRouter, Path, HTTPException, Query
from app.services.ferremas_api import get_vendedores, get_vendedor_id, get_vendedores_por_sucursal

router = APIRouter(prefix="/data/vendedores",
                    tags=["Vendedores"])

#TODOS los vendedores
#@router.get("/")
#def listar_vendedores():
#    return get_vendedores()

#VENDEDORES por sucursal
@router.get("/")
def listar_vendedores_por_sucursal(sucursal: str = Query(..., description="ID de la sucursal")):
    try:
        vendedores = get_vendedores_por_sucursal(sucursal)
        if not vendedores:
            raise HTTPException(status_code=404, detail="No se encontraron vendedores para la sucursal")
        return vendedores
    except Exception:
        raise HTTPException(status_code=500, detail="Error al obtener los vendedores")

#VENDEDOR por id    
@router.get("/{vendedor_id}")
def obtener_vendedor(vendedor_id: str = Path(..., description="ID del vendedor")):
    try:
        return get_vendedor_id(vendedor_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Vendedor no encontrado")
