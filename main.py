from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.DB import Base, engine

from sqlalchemy.orm import Session
from routes.admin import admin_auth, admin_makanan, admin_config
from routes import pengguna_routes, rekomendasi_routes, preferensi_routes,bmi_routes, spk_routes
from model.user import Pengguna         
from model.makanan import Makanan   

from utils.DB import get_db


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Gym Food Decision Support System API",
    description="API untuk rekomendasi makanan bagi gym enthusiast.",
    version="1.0.0"
)

@app.get("/api/stats")
def get_app_stats(db: Session = Depends(get_db)):
    """
    Endpoint untuk mendapatkan statistik aplikasi dari database Supabase:
    - Jumlah pengguna terdaftar
    - Jumlah makanan yang tersedia
    """
    try:
        total_users = db.query(Pengguna).count()
        total_makanan = db.query(Makanan).count()
        
        return {
            "pengguna_aktif": total_users,
            "rekomendasi_makanan": total_makanan
        }
    except Exception as e:
        print(f"Error fetching stats from Supabase DB: {e}")
        # Nilai fallback jika terjadi error
        return {
            "pengguna_aktif": 300,
            "rekomendasi_makanan": 100
        }



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Mendaftarkan router...")
app.include_router(spk_routes.router)
app.include_router(bmi_routes.router)
app.include_router(admin_auth.router)
app.include_router(admin_makanan.router) 
app.include_router(admin_config.router)
app.include_router(pengguna_routes.router) 
app.include_router(rekomendasi_routes.router) 
app.include_router(preferensi_routes.router) 
print("Semua router berhasil didaftarkan.")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Gym Food DSS API!"}