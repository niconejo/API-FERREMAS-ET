import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY") 


def convertir_divisa(from_currency: str, to_currency: str, amount: float):
    url = "https://api.apilayer.com/fixer/convert"
    params = {
        "from": from_currency,
        "to": to_currency,
        "amount": amount,
        "to": to_currency
    }

    headers = {
        "apikey": API_KEY
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        print("RESPUESTA FIXER:", data)

        if not data.get("success", False):
            raise Exception(data.get("error", {}).get("info", "Error desconocido en la conversión."))

        return {
            "from": data["query"]["from"],
            "to": data["query"]["to"],
            "original": data["query"]["amount"],
            "convertido": data["result"],
            "tasa": data["info"]["rate"]
        }

    except requests.Timeout:
        raise Exception("Timeout al contactar con Fixer.io")
    except Exception as e:
        raise Exception(f"Error al convertir divisas: {str(e)}")