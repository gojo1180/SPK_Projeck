import base64
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import desc
from schema.hasil_schemas import HasilCreate, HasilWithNamaResponse
from model.hasil import Hasil
from model import makanan as makanan_model
from model.user import Pengguna
from utils.security import get_current_user
from utils.DB import get_db
from typing import List

router = APIRouter()

# Endpoint menyimpan hasil SPK
@router.post("/api/spk/simpan")
def simpan_hasil_spk(
    hasil_list: list[HasilCreate],
    db: Session = Depends(get_db),
    current_user: Pengguna = Depends(get_current_user)
):
    for item in hasil_list:
        hasil = Hasil(
            id_pengguna=current_user.id_pengguna,
            id_makanan=item.id_makanan,
            skor_total=item.skor_total,
            ranking=item.ranking,
            fase_latihan=item.fase_latihan,
            waktu_makan=item.waktu_makan,
            tanggal_rekomendasi=datetime.now()
        )
        db.add(hasil)
    db.commit()
    return {"message": "Hasil SPK berhasil disimpan."}

# Endpoint histori SPK biasa (flat)
@router.get("/api/spk/histori", response_model=List[HasilWithNamaResponse])
def get_histori_spk(
    db: Session = Depends(get_db),
    current_user: Pengguna = Depends(get_current_user),
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

# Endpoint histori SPK versi grouped (UX friendly)
@router.get("/api/spk/histori/group")
def get_histori_grouped(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    hasil = (
        db.query(
            Hasil.id_hasil,
            Hasil.id_makanan,
            makanan_model.Makanan.nama.label("nama_makanan"),
            makanan_model.Makanan.gambar.label("gambar_blob"),
            Hasil.skor_total,
            Hasil.ranking,
            Hasil.tanggal_rekomendasi,
            Hasil.fase_latihan,
            Hasil.waktu_makan
        )
        .join(makanan_model.Makanan, Hasil.id_makanan == makanan_model.Makanan.id_makanan)
        .filter(Hasil.id_pengguna == current_user.id_pengguna)
        .order_by(desc(Hasil.tanggal_rekomendasi), Hasil.ranking)
        .all()
    )

    grouped = {}
    for row in hasil:
        key = f"{row.fase_latihan}__{row.waktu_makan}"
        if key not in grouped:
            grouped[key] = []

        gambar_base64 = None
        if row.gambar_blob:
            gambar_base64 = f"data:image/jpeg;base64,{base64.b64encode(row.gambar_blob).decode('utf-8')}"

        grouped[key].append({
            "id_hasil": row.id_hasil,
            "id_makanan": row.id_makanan,
            "nama_makanan": row.nama_makanan,
            "gambar": gambar_base64,
            "skor_total": row.skor_total,
            "ranking": row.ranking,
            "tanggal_rekomendasi": row.tanggal_rekomendasi
        })

    # Pastikan setiap grup diurutkan berdasarkan ranking
    for key in grouped:
        grouped[key] = sorted(grouped[key], key=lambda x: x['ranking'])

    return grouped
