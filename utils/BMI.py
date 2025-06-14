import os
import requests
from fastapi import HTTPException
from dotenv import load_dotenv
from model import bmi as bmi_model
from sqlalchemy.orm import Session

load_dotenv()  # Muat variabel .env sekali saja
def hitung_bmi_controller(weight: float, height: float, unit: str = "metric", db: Session = None, id_pengguna: int = None):
    api_key = os.getenv("BMI_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="API key tidak ditemukan.")

    url = "https://api.apiverve.com/v1/bmicalculator"
    params = {"weight": str(weight), "height": str(height), "unit": unit}
    headers = {"x-api-key": api_key}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json().get("data", {})

        bmi_value = data.get("bmi")
        summary = data.get("summary", "").lower()
        recommendation = data.get("recommendation")

        # Tentukan kategori enum dari nilai BMI (bukan dari summary)
        if bmi_value is None:
            raise HTTPException(status_code=400, detail="BMI tidak dapat dihitung.")

        if bmi_value < 18.5:
            kategori_enum = bmi_model.KategoriBMIEnum.underweight
            status = "Underweight"
        elif 18.5 <= bmi_value < 25:
            kategori_enum = bmi_model.KategoriBMIEnum.normal
            status = "Normal"
        elif 25 <= bmi_value < 30:
            kategori_enum = bmi_model.KategoriBMIEnum.overweight
            status = "Overweight"
        else:
            kategori_enum = bmi_model.KategoriBMIEnum.obese
            status = "Obese"

        if db and id_pengguna:
            new_bmi = bmi_model.BMI(
                id_pengguna=id_pengguna,
                berat_badan=weight,
                tinggi_badan=height,
                nilai_bmi=bmi_value,
                kategori=kategori_enum,
            )
            db.add(new_bmi)
            db.commit()
            db.refresh(new_bmi)

        return {
            "bmi": bmi_value,
            "status": status,
            "suggestion": recommendation,
            "unit": unit
        }

    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Error memanggil BMI API: {str(e)}")
