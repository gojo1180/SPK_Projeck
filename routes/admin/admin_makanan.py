from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional, List

from utils.DB import get_db
from controller.Admin import update_makanan_controller
from controller import Admin
from utils.security import get_current_admin
from schema.makanan_schemas import MakananCreate, Makanan as MakananSchema, MakananOut
from model.kriteria import Kriteria
from schema.kriteria_schemas import KriteriaResponse
from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException, status # Pastikan status diimpor

# HAPUS prefix
router = APIRouter(
    tags=["Admin - Makanan"],
    dependencies=[Depends(get_current_admin)]
)

# TAMBAHKAN ENDPOINT BARU INI
@router.get("/admin/kriteria/", response_model=List[KriteriaResponse])
def list_kriteria(db: Session = Depends(get_db)):
    """
    Mengambil daftar semua kriteria yang tersedia untuk form nilai gizi.
    """
    return db.query(Kriteria).all()

@router.post("/admin/makanan/", response_model=MakananSchema, status_code=201)
async def add_makanan(
    db: Session = Depends(get_db),
    nama: str = Form(...),
    deskripsi: Optional[str] = Form(None),
    gambar: UploadFile = File(...),
    nilai_gizi: str = Form('[]') # <-- TAMBAHKAN ini, default ke string array kosong
):
    makanan_create = MakananCreate(nama=nama, deskripsi=deskripsi)
    # Teruskan nilai_gizi ke controller
    return await Admin.create_makanan(db=db, makanan=makanan_create, gambar=gambar, nilai_gizi_json=nilai_gizi)

# ... (list_makanan tidak berubah) ...

@router.put("/admin/makanan/{makanan_id}", response_model=MakananOut)
async def update_makanan(
    makanan_id: int,
    nama: str = Form(...),
    deskripsi: str = Form(""),
    nilai_gizi: str = Form('[]'), # <-- TAMBAHKAN ini
    gambar: UploadFile = None,
    db: Session = Depends(get_db)
):
    return await update_makanan_controller(
        db=db,
        makanan_id=makanan_id,
        nama=nama,
        deskripsi=deskripsi,
        nilai_gizi_json=nilai_gizi, # <-- Teruskan ke controller
        gambar=gambar
    )

# TAMBAHKAN path lengkap
@router.get("/admin/makanan/", response_model=List[MakananOut], status_code=200)
def list_makanan(db: Session = Depends(get_db)):
    return Admin.get_all_makanan(db)


@router.delete("/admin/makanan/{makanan_id}/force", status_code=status.HTTP_200_OK)
def force_delete_makanan_route(
    makanan_id: int,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin) # Asumsi Anda punya dependensi keamanan
):
    """
    Endpoint untuk menghapus makanan beserta semua data terkait (force delete).
    Memerlukan autentikasi admin.
    """
    if not current_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tidak diizinkan",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Admin.force_delete_makanan(db=db, makanan_id=makanan_id)
