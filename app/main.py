#app/main.py
from fastapi import FastAPI
from app.routers import articulos, auth, sucursales, vendedores, pedidos, contacto, pagos, divisas
from sqlmodel import SQLModel;
from app.services.database import get_db_engine;


app = FastAPI(
    title="Ferremas Integration API",
    description="API puente entre Ferremas y servicios externos",
    version="1.0"
)
def create_tables():
    SQLModel.metadata.create_all(get_db_engine())


app.include_router(auth.router)
app.include_router(articulos.router)
app.include_router(sucursales.router)
app.include_router(vendedores.router)
app.include_router(pedidos.router)
app.include_router(contacto.router)
app.include_router(pagos.router)
app.include_router(divisas.router)
@app.on_event("startup")
def on_startup():
    create_tables()
    
@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de FERREMAS. Visita /docs para la documentación interactiva."}