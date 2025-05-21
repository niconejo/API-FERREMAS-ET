import requests
from app.models.pedido import PedidoRequest

BASE_URL = "https://ea2p2assets-production.up.railway.app"
TOKEN = "SaGrP9ojGS39hU9ljqbXxQ=="

headers = {
    "x-authentication": TOKEN
}
#GET ARTICULOS
def get_articulos():
    url = f"{BASE_URL}/data/articulos"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_articulo_id(articulo_id: str):
    url = f"{BASE_URL}/data/articulos/{articulo_id}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    if not data:  # si devuelve {}
        raise ValueError("Artículo no encontrado o respuesta vacía")

    return data
#PUT ARTICULO
def actualizar_stock_articulo(articulo_id: str, nuevo_stock: int):
    url = f"{BASE_URL}/data/articulos/{articulo_id}"
    headers_with_auth = {
        "x-authentication": TOKEN,
        "Content-Type": "application/json"
    }

    payload = {
        "cantidad": nuevo_stock  
    }

    response = requests.put(url, headers=headers_with_auth, json=payload)
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