from fastapi import APIRouter, HTTPException, Depends
from app.models.divisa import ConversionRequest
from app.services.divisas_api import convertir_divisa
from app.auth.auth_bearer import JWTBearer
from app.auth.role_checker import validar_rol
from app.auth.roles import ROLES

router = APIRouter(prefix="/divisas", tags=["Divisas"])

@router.post("/convertir", dependencies=[Depends(JWTBearer())])
def convertir(request: ConversionRequest, payload=Depends(JWTBearer())):
    validar_rol(payload, [ROLES["service_account"]])
    try:
        resultado = convertir_divisa(request.from_currency, request.to_currency, request.amount)
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))