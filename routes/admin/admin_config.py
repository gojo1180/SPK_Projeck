import json
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, status

from utils.security import get_current_admin
from schema import config_schemas

router = APIRouter(
    prefix="/admin/bobot-default",
    tags=["Admin - Konfigurasi Bobot"],
    dependencies=[Depends(get_current_admin)]
)

# Tentukan path ke file konfigurasi secara dinamis
CONFIG_FILE_PATH = Path(__file__).parent.parent.parent / "config" / "default_weights.json"

@router.get("/", response_model=config_schemas.DefaultWeightsSchema)
def get_default_weights():
    """
    Membaca dan menampilkan konfigurasi bobot default saat ini dari file JSON.
    """
    if not CONFIG_FILE_PATH.is_file():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File konfigurasi bobot tidak ditemukan.")
    
    with open(CONFIG_FILE_PATH, 'r') as f:
        weights_data = json.load(f)
    return weights_data

@router.put("/", response_model=config_schemas.DefaultWeightsSchema)
def update_default_weights(weights_data: config_schemas.DefaultWeightsSchema):
    """
    Memperbarui dan menyimpan konfigurasi bobot default ke dalam file JSON.
    """
    try:
        # Tulis kembali ke file dengan format yang rapi (indent=4)
        with open(CONFIG_FILE_PATH, 'w') as f:
            # Pydantic model perlu di-dump ke dict dulu sebelum disimpan sebagai JSON
            json.dump(weights_data.model_dump(), f, indent=4)
        return weights_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Gagal menyimpan file: {e}")