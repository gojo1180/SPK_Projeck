from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional, List

from utils.DB import get_db
from controller.Admin import update_makanan_controller
from controller import Admin
from utils.security import get_current_admin
from schema.makanan_schemas import MakananCreate, Makanan as MakananSchema, MakananOut

# HAPUS prefix
router = APIRouter(
    tags=["Admin - Makanan"],
    dependencies=[Depends(get_current_admin)]
)

# TAMBAHKAN path lengkap
@router.post("/admin/makanan/", response_model=MakananSchema, status_code=201)
async def add_makanan(
    db: Session = Depends(get_db),
    nama: str = Form(...),
    deskripsi: Optional[str] = Form(None),
    gambar: UploadFile = File(...)
):
    makanan_create = MakananCreate(nama=nama, deskripsi=deskripsi)
    return await Admin.create_makanan(db=db, makanan=makanan_create, gambar=gambar)

# TAMBAHKAN path lengkap
@router.get("/admin/makanan/", response_model=List[MakananOut], status_code=200)
def list_makanan(db: Session = Depends(get_db)):
    return Admin.get_all_makanan(db)

# TAMBAHKAN path lengkap
@router.put("/admin/makanan/{makanan_id}", response_model=MakananOut)
async def update_makanan(
    makanan_id: int,
    nama: str = Form(...),
    deskripsi: str = Form(""),
    gambar: UploadFile = None,
    db: Session = Depends(get_db)
):
    return await update_makanan_controller(
        db=db,
        makanan_id=makanan_id,
        nama=nama,
        deskripsi=deskripsi,
        gambar=gambar
    )