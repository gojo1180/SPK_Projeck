# routes/makanan_routes.py

from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional

from utils.DB import get_db
from controller.Admin import update_makanan_controller
from controller import Admin
from utils.security import get_current_admin
from typing import List
from schema.makanan_schemas import MakananCreate, Makanan as MakananSchema, MakananOut

router = APIRouter(
    prefix="/admin/makanan",
    tags=["Admin - Makanan"],
    dependencies=[Depends(get_current_admin)]
)

@router.post("/", response_model=MakananSchema, status_code=201)
async def add_makanan(
    db: Session = Depends(get_db),
    nama: str = Form(...),
    deskripsi: Optional[str] = Form(None),
    gambar: UploadFile = File(...)
):
    """
    Endpoint untuk membuat data makanan baru.

    - **nama**: Nama makanan (wajib).
    - **deskripsi**: Deskripsi singkat tentang makanan (opsional).
    - **gambar**: File gambar makanan (wajib).
    """
    makanan_create = MakananCreate(nama=nama, deskripsi=deskripsi)
    return await Admin.create_makanan(db=db, makanan=makanan_create, gambar=gambar)

@router.get("/", response_model=List[MakananOut], status_code=200)
def list_makanan(db: Session = Depends(get_db)):
    return Admin.get_all_makanan(db)

@router.put("/{makanan_id}", response_model=MakananOut)
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