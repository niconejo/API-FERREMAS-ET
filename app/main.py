#app/main.py
from fastapi import FastAPI
from app.routers import articulos, auth, sucursales, vendedores, pedidos, contacto, pagos, divisas
from app.services.database import crear_bd


app = FastAPI(
    title="Ferremas Integration API",
    description="API puente entre Ferremas y servicios externos",
    version="1.0"
)
crear_bd()
app.include_router(auth.router)
app.include_router(articulos.router)
app.include_router(sucursales.router)
app.include_router(vendedores.router)
app.include_router(pedidos.router)
app.include_router(contacto.router)
app.include_router(pagos.router)
app.include_router(divisas.router)
