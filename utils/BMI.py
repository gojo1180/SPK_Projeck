import os
import requests
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()  # Muat variabel .env sekali saja

def hitung_bmi_controller(weight: float, height: float, unit: str = "metric"):
    api_key = os.getenv("BMI_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="API key tidak ditemukan.")

    url = "https://api.apiverve.com/v1/bmicalculator"
    params = {
        "weight": str(weight),
        "height": str(height),
        "unit": unit
    }
    headers = {
        "x-api-key": api_key
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json().get("data", {})

        return {
            "bmi": data.get("bmi"),
            "status": data.get("summary"),
            "suggestion": data.get("recommendation"),
            "unit": unit
        }

    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Error memanggil BMI API: {str(e)}")

