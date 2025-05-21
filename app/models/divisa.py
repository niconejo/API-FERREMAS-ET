from pydantic import BaseModel

class ConversionRequest(BaseModel):
    from_currency: str  # Moneda a cambiar
    to_currency: str    
    amount: float # Resultado