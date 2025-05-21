from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from app.auth.auth_handler import decode_token

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            token = credentials.credentials
            payload = decode_token(token)
            if payload:
                return payload  # retorna datos del usuario y rol
            raise HTTPException(status_code=403, detail="Token inválido o expirado")
        else:
            raise HTTPException(status_code=403, detail="Token requerido")