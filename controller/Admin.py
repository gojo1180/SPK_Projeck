# controllers/makanan_controller.py

from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status
from model.makanan import Makanan
from schema.makanan_schemas import MakananCreate
import base64

async def create_makanan(db: Session, makanan: MakananCreate, gambar: UploadFile):
    existing = db.query(Makanan).filter(Makanan.nama == makanan.nama).first()
    if existing:
        raise HTTPException(status_code=400, detail="Makanan dengan nama tersebut sudah ada")

    gambar_bytes = await gambar.read()

    new_makanan = Makanan(
        nama=makanan.nama,
        deskripsi=makanan.deskripsi,
        gambar=gambar_bytes
    )
    db.add(new_makanan)
    db.commit()
    db.refresh(new_makanan)
    return new_makanan

def get_all_makanan(db: Session):
    makanan_list = db.query(Makanan).all()
    
    # Konversi gambar menjadi base64 untuk ditampilkan di frontend
    result = []
    for m in makanan_list:
        result.append({
            "id_makanan": m.id_makanan,
            "nama": m.nama,
            "deskripsi": m.deskripsi,
            "gambar": base64.b64encode(m.gambar).decode('utf-8') if m.gambar else None
        })
    return result

async def update_makanan_controller(
    db: Session,
    makanan_id: int,
    nama: str,
    deskripsi: str,
    gambar: UploadFile = None
):
    makanan = db.query(Makanan).filter(Makanan.id_makanan == makanan_id).first()

    if not makanan:
        raise HTTPException(status_code=404, detail="Makanan tidak ditemukan")

    makanan.nama = nama
    makanan.deskripsi = deskripsi

    if gambar:
        content = await gambar.read()
        makanan.gambar = base64.b64encode(content).decode("utf-8")

    db.commit()
    db.refresh(makanan)
    return makanan