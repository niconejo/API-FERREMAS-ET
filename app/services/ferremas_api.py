import requests
from app.models.pedido import PedidoRequest
from app.services.database import get_db_engine;
from sqlmodel import Session, select
from app.models.articulo import Articulo

BASE_URL = "https://ea2p2assets-production.up.railway.app"
TOKEN = "SaGrP9ojGS39hU9ljqbXxQ=="

headers = {
    "x-authentication": TOKEN
}
#GET ARTICULOS
def get_articulos():
    # 1. Obtener desde API externa
    url = f"{BASE_URL}/data/articulos"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    articulos_externos = response.json()

    # 2. Guardar en la base de datos local
    with Session(get_db_engine()) as session:
        for art in articulos_externos:
            articulo_existente = session.exec(
                select(Articulo).where(Articulo.id == art["id"])
            ).first()

            if articulo_existente:
                # actualizar si ya existe
                articulo_existente.categoria = art.get("categoria", "")
                articulo_existente.subcategoria = art.get("subcategoria", "")
                articulo_existente.nombre = art.get("nombre", "")
                articulo_existente.marca = art.get("marca", "")
                articulo_existente.precio = art.get("precio", 0)
                articulo_existente.stock = art.get("stock", 0)
            else:
                # crear nuevo
                nuevo = Articulo(
                    id=art.get("id"),
                    categoria=art.get("categoria", ""),
                    subcategoria=art.get("subcategoria", ""),
                    nombre=art.get("nombre", ""),
                    marca=art.get("marca", ""),
                    precio=art.get("precio", 0),
                    stock=art.get("stock", 0)
                )
                session.add(nuevo)

        session.commit()

    return articulos_externos

def get_articulo_id(articulo_id: str):
    url = f"{BASE_URL}/data/articulos/{articulo_id}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if not data or not isinstance(data, dict):
            raise ValueError("Artículo no encontrado o respuesta vacía")

        return data

    except requests.HTTPError as e:
        raise ValueError(f"Error al obtener el artículo: {e}")

    return data
#PUT ARTICULO
def actualizar_stock_articulo(articulo_id: str, nuevo_stock: int):
    url = f"{BASE_URL}/data/articulos/venta/{articulo_id}"
    headers_with_auth = {
        "x-authentication": TOKEN
    }

    params = {
        "cantidad": nuevo_stock  
    }
    print(f"PUT {url}?cantidad={nuevo_stock}")

    response = requests.put(url, headers=headers_with_auth, params=params)
    response.raise_for_status()
    return response.json()

#GET SUCURSALES
def get_sucursales():
    url = f"{BASE_URL}/data/sucursales"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_sucursal_id(sucursal_id: str):
    url = f"{BASE_URL}/data/sucursales/{sucursal_id}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    if not data:  # si devuelve {}
        raise ValueError("Sucursal no encontrado o respuesta vacía")

    return data
#GET VENDEDORES
def get_vendedores():
    url = f"{BASE_URL}/data/vendedores"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_vendedores_por_sucursal(sucursal_id: str):
    todos = get_vendedores()
    return [v for v in todos if v.get("sucursal") == sucursal_id]

def get_vendedor_id(vendedor_id: str):
    url = f"{BASE_URL}/data/vendedores/{vendedor_id}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    if not data:  # si devuelve {}
        raise ValueError("Vendedor no encontrado o respuesta vacía")

    return data
#CREAR PEDIDO
def crear_pedido(pedido: PedidoRequest):
    url = f"{BASE_URL}/data/pedidos/nuevo"
    headers_with_auth = {
        "x-authentication": TOKEN
    }
    # Le ponemos id=0 como pide la estructura
    payload = pedido.dict()
    payload["id"] = 0

    response = requests.post(url, headers=headers_with_auth, json=payload)
    if not response.ok:
        print("STATUS:", response.status_code)
        print("BODY:", response.text)

    response.raise_for_status()
    return response.json()