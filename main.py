from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from model import user, makanan, bmi, kriteria, hasil, admin, bobot_preferensi, nilai_gizi
from routes.admin import admin_auth, admin_makanan

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

app.include_router(admin_auth.router)
app.include_router(admin_makanan.router) 

@app.get("/")
def read_root():
    return {"message": "Welcome to the Gym Food DSS API!"}
