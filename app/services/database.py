from sqlmodel import SQLModel, create_engine

sqlite_file_name = "catalogo.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine("sqlite:///ferremas.db")

def crear_bd():
    SQLModel.metadata.create_all(engine)