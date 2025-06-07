from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from model import user, makanan, bmi, kriteria, penilaian, hasil, admin, bobot_preferensi, nilai_gizi

from utils.DB import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

