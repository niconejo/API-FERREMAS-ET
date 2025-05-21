from fastapi import APIRouter, HTTPException
from app.models.login import LoginRequest
from app.auth.users_db import fake_users_db
from app.auth.auth_handler import create_access_token

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/login")
def login(request: LoginRequest):
    user = fake_users_db.get(request.username)

    if not user or request.password != user["password"]:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token = create_access_token(data={
        "sub": request.username,
        "role": user["role"]
    })

    return {"access_token": token, "token_type": "bearer"}