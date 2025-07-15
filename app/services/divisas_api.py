import os
from dotenv import load_dotenv
from bcchapi import Siete
from datetime import datetime, timedelta
import pandas as pd

load_dotenv()

BCCH_USER = os.getenv("BCCH_USER")
BCCH_PASS = os.getenv("BCCH_PASS")

def convertir_divisa_bcch(from_currency: str, to_currency: str, amount: float):
    if from_currency != "CLP" or to_currency != "USD":
        raise Exception("Actualmente solo se soporta conversión CLP a USD vía Banco Central.")

    try:
        siete = Siete(BCCH_USER, BCCH_PASS)
        hoy = datetime.today()
        
        # Buscar hacia atrás hasta 7 días por la última tasa disponible
        for i in range(1, 8):
            fecha_final = hoy - timedelta(days=i)
            fecha_ini = fecha_final.strftime("%Y-%m-%d")
            fecha_fin = fecha_ini  # Consultar solo un día
            df = siete.cuadro(
                series=["F073.TCO.PRE.Z.D"],
                nombres=["tasa"],
                desde=fecha_ini,
                hasta=fecha_fin
            )
            if not df.empty and not pd.isna(df.iloc[-1]["tasa"]):
                break

        if df.empty:
            raise Exception("No se encontraron tasas de cambio disponibles en los últimos 7 días.")

        tasa = df.iloc[-1]["tasa"]

        if tasa == 0 or pd.isna(tasa):
            raise Exception("Tasa de cambio inválida.")

        resultado = round(amount / tasa, 2)

        return {
            "from": from_currency,
            "to": to_currency,
            "original": amount,
            "convertido": resultado,
            "tasa": tasa,
            "fecha": fecha_ini
        }

    except Exception as e:
        raise Exception(f"Error al obtener tasa desde el Banco Central: {str(e)}")
