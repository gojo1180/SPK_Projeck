import base64
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from schema.hasil_schemas import HasilCreate
from schema.hasil_schemas import HasilWithNamaResponse
from model.hasil import Hasil
from model import makanan as makanan_model
from utils.security import get_current_user
from utils.DB import get_db
from typing import List

router = APIRouter()

@router.post("/api/spk/simpan")
def simpan_hasil_spk(
    hasil_list: list[HasilCreate],
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    print("HASIL MASUK:", hasil_list)  # Debug print

    for idx, item in enumerate(hasil_list):
        print("Item ke-", idx, ":", item)
        hasil = Hasil(
            id_pengguna=current_user.id_pengguna,
            id_makanan=item.id_makanan,
            skor_total=item.skor_total,
            ranking=item.ranking
        )
        db.add(hasil)
    db.commit()
    return {"message": "Hasil SPK berhasil disimpan."}

@router.get("/api/spk/histori", response_model=List[HasilWithNamaResponse])
def get_histori_spk(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    hasil_join = (
        db.query(
            Hasil.id_hasil,
            Hasil.id_makanan,
            makanan_model.Makanan.nama.label("nama_makanan"),
            makanan_model.Makanan.gambar.label("gambar_blob"),
            Hasil.skor_total,
            Hasil.ranking,
            Hasil.tanggal_rekomendasi
        )
        .join(makanan_model.Makanan, Hasil.id_makanan == makanan_model.Makanan.id_makanan)
        .filter(Hasil.id_pengguna == current_user.id_pengguna)
        .order_by(desc(Hasil.tanggal_rekomendasi))
        .all()
    )

    hasil_with_gambar = []
    for row in hasil_join:
        # Encode gambar jika ada
        gambar_base64 = None
        if row.gambar_blob:
            gambar_base64 = f"data:image/jpeg;base64,{base64.b64encode(row.gambar_blob).decode('utf-8')}"
        
        hasil_with_gambar.append({
            "id_hasil": row.id_hasil,
            "id_makanan": row.id_makanan,
            "nama_makanan": row.nama_makanan,
            "gambar": gambar_base64,
            "skor_total": row.skor_total,
            "ranking": row.ranking,
            "tanggal_rekomendasi": row.tanggal_rekomendasi
        })

    return hasil_with_gambar