from fastapi import APIRouter, Path, HTTPException, Query, Depends
from app.services.ferremas_api import get_vendedores, get_vendedor_id, get_vendedores_por_sucursal
from app.auth.auth_bearer import JWTBearer
from app.auth.role_checker import validar_rol
from app.auth.roles import ROLES

router = APIRouter(prefix="/data/vendedores",
                    tags=["Vendedores"])

#TODOS los vendedores
#@router.get("/")
#def listar_vendedores():
#    return get_vendedores()

#VENDEDORES por sucursal
@router.get("/", dependencies=[Depends(JWTBearer())])
def listar_vendedores_por_sucursal(
    sucursal: str = Query(..., description="ID de la sucursal"),
    payload=Depends(JWTBearer())
):  #verificar rol necesario
    validar_rol(payload, [ROLES["jefe_tienda"],
                          ROLES["admin"]])

    try:
        vendedores = get_vendedores_por_sucursal(sucursal)
        if not vendedores:
            raise HTTPException(status_code=404, detail="No se encontraron vendedores para la sucursal")
        return vendedores
    except Exception:
        raise HTTPException(status_code=500, detail="Error al obtener los vendedores")

#VENDEDOR por id    
@router.get("/{vendedor_id}", dependencies=[Depends(JWTBearer())])
def obtener_vendedor(
    vendedor_id: str = Path(..., description="ID del vendedor"),
    payload=Depends(JWTBearer())
):
    validar_rol(payload, [ROLES["jefe_tienda"],
                          ROLES["admin"]])

    try:
        return get_vendedor_id(vendedor_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Vendedor no encontrado")
