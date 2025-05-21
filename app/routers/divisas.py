from fastapi import APIRouter, HTTPException
from app.models.divisa import ConversionRequest
from app.services.divisas_api import convertir_divisa

router = APIRouter(
    prefix="/divisas",
    tags=["Divisas"]
)

@router.post("/convertir")
def convertir(request: ConversionRequest):
    try:
        resultado = convertir_divisa(request.from_currency, request.to_currency, request.amount)
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))