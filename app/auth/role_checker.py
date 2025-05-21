from fastapi import HTTPException

def validar_rol(payload: dict, roles_permitidos: list):
    user_role = payload.get("role")
    if user_role not in roles_permitidos:
        raise HTTPException(status_code=403, detail=f"Acceso denegado para el rol: {user_role}")