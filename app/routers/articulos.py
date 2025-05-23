from fastapi import APIRouter, Path, HTTPException, Depends
from app.services.ferremas_api import get_articulos, get_articulo_id
from app.auth.auth_bearer import JWTBearer
from app.auth.role_checker import validar_rol
from app.auth.roles import ROLES
from sqlmodel import Session, select
from app.models.articulo import Articulo, Novedad, Promocion
from app.services.database import engine
import requests
from sqlalchemy import or_

router = APIRouter(prefix="/data/articulos", tags=["Articulos"])

def sincronizar_articulos():
    respuesta = requests.get("https://api-ferremas.com/data/articulos")
    if respuesta.status_code == 200:
        articulos = respuesta.json()
        with Session(engine) as session:
            for art in articulos:
                if not session.get(Articulo, art["id"]):
                    articulo = Articulo(**art)
                    session.add(articulo)
            session.commit()

@router.get("/", dependencies=[Depends(JWTBearer())])
def listar_articulos(payload=Depends(JWTBearer())):
    validar_rol(payload, [ROLES["bodega"], ROLES["admin"], ROLES["jefe_tienda"]])
    return get_articulos()

@router.get("/novedades", response_model=list[Articulo], dependencies=[Depends(JWTBearer())])
def obtener_novedades(payload=Depends(JWTBearer())):
    try:
        validar_rol(payload, [ROLES["bodega"], ROLES["admin"], ROLES["jefe_tienda"], ROLES["mantenedor"]])
        with Session(engine) as session:
            # Obtenemos IDs
            ids = session.exec(select(Novedad.articulo_id)).all()
            if ids and isinstance(ids[0], tuple):
                ids = [id[0] for id in ids]
            print(f"IDs encontrados (limpios): {ids}")

            # Verificamos si los artículos existen en DB con consulta directa
            for id_test in ids:
                art_test = session.get(Articulo, id_test)
                print(f"Artículo con id {id_test}: {art_test}")

            # Intentamos con in_()
            articulos = session.exec(select(Articulo).where(Articulo.id.in_(ids))).all()
            print(f"Artículos encontrados con in_(): {articulos}")

            return articulos
    except Exception as e:
        print(f"ERROR en /novedades: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener novedades: " + str(e))
            
@router.get("/promociones", response_model=list[Articulo], dependencies=[Depends(JWTBearer())])
def obtener_promociones(payload=Depends(JWTBearer())):
    try:
        validar_rol(payload, [ROLES["bodega"], ROLES["admin"], ROLES["jefe_tienda"], ROLES["mantenedor"]])
        with Session(engine) as session:
            print("Obteniendo IDs de artículos en promociones...")
            resultados = session.exec(select(Promocion.articulo_id)).all()
            ids = []
            for r in resultados:
                if isinstance(r, tuple) or isinstance(r, list):
                    ids.append(str(r[0]).strip())
                else:
                    ids.append(str(r).strip())
            print(f"IDs encontrados (limpios): {ids}")

            if not ids:
                return []

            articulos = session.exec(select(Articulo).where(Articulo.id.in_(ids))).all()
            print(f"Artículos encontrados: {articulos}")
            return articulos
    except Exception as e:
        print(f"ERROR en /promociones: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener promociones: " + str(e))

@router.post("/nuevo", response_model=Articulo, dependencies=[Depends(JWTBearer())])
def agregar_articulo(articulo: Articulo, payload=Depends(JWTBearer())):
    validar_rol(payload, [ROLES["mantenedor"]])
    with Session(engine) as session:
        session.add(articulo)
        session.commit()
        session.refresh(articulo)
        return articulo

@router.post("/novedades/{articulo_id}", dependencies=[Depends(JWTBearer())])
def agregar_a_novedades(articulo_id: str, payload=Depends(JWTBearer())):
    validar_rol(payload, [ROLES["mantenedor"],
                          ROLES["admin"]])
    with Session(engine) as session:
        session.add(Novedad(articulo_id=articulo_id))
        session.commit()
    return {"mensaje": f"Articulo {articulo_id} marcado como novedad"}

@router.post("/promociones/{articulo_id}", dependencies=[Depends(JWTBearer())])
def agregar_a_promociones(articulo_id: str, payload=Depends(JWTBearer())):
    validar_rol(payload, [ROLES["mantenedor"], ROLES["admin"]])
    with Session(engine) as session:
        session.add(Promocion(articulo_id=articulo_id))
        session.commit()
    return {"mensaje": f"Articulo {articulo_id} marcado como promoción"}

@router.get("/{articulo_id}", dependencies=[Depends(JWTBearer())])
def obtener_articulo(
    articulo_id: str = Path(..., description="ID del artículo"),
    payload=Depends(JWTBearer())
):
    validar_rol(payload, [ROLES["bodega"], ROLES["admin"], ROLES["jefe_tienda"]])
    try:
        return get_articulo_id(articulo_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")
