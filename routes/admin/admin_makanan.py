from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from utils.DB import get_db
from model import makanan as makanan_model, nilai_gizi as nilai_gizi_model
from schema import makanan_schemas
from utils.security import get_current_admin
from model import admin

router = APIRouter(
    prefix="/admin/makanan",
    tags=["Admin - Makanan"],
    #authorization 
    dependencies=[Depends(get_current_admin)]
)

@router.post("/", response_model=makanan_schemas.Makanan, status_code=status.HTTP_201_CREATED)
def create_makanan(makanan: makanan_schemas.MakananCreate, db: Session = Depends(get_db)):
    """
    Membuat entri makanan baru beserta nilai gizinya.
    """
    db_makanan = makanan_model.Makanan(
        nama=makanan.nama, 
        deskripsi=makanan.deskripsi, 
        gambar_url=makanan.gambar_url
    )
    db.add(db_makanan)
    db.flush() # Gunakan flush untuk mendapatkan ID makanan sebelum commit

    # Buat entri nilai gizi
    for ng in makanan.nilai_gizi:
        db_ng = nilai_gizi_model.NilaiGizi(
            id_makanan=db_makanan.id_makanan,
            id_kriteria=ng.id_kriteria,
            nilai=ng.nilai
            # id_pengguna_pembuat bisa diisi dengan id admin jika perlu
        )
        db.add(db_ng)
    
    db.commit()
    db.refresh(db_makanan)
    return db_makanan

@router.get("/", response_model=List[makanan_schemas.Makanan])
def read_all_makanan(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Membaca semua data makanan.
    """
    makanans = db.query(makanan_model.Makanan).offset(skip).limit(limit).all()
    return makanans

@router.get("/{makanan_id}", response_model=makanan_schemas.Makanan)
def read_makanan_by_id(makanan_id: int, db: Session = Depends(get_db)):
    """
    Membaca data makanan spesifik berdasarkan ID.
    """
    db_makanan = db.query(makanan_model.Makanan).filter(makanan_model.Makanan.id_makanan == makanan_id).first()
    if db_makanan is None:
        raise HTTPException(status_code=404, detail="Makanan not found")
    return db_makanan

@router.delete("/{makanan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_makanan(makanan_id: int, db: Session = Depends(get_db)):
    """
    Menghapus data makanan berdasarkan ID.
    """
    db_makanan = db.query(makanan_model.Makanan).filter(makanan_model.Makanan.id_makanan == makanan_id).first()
    if db_makanan is None:
        raise HTTPException(status_code=404, detail="Makanan not found")
    
    db.delete(db_makanan)
    db.commit()
    return None # No content