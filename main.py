from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.DB import Base, engine


from routes.admin import admin_auth, admin_makanan, admin_config
from routes import pengguna_routes, rekomendasi_routes, preferensi_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Gym Food Decision Support System API",
    description="API untuk rekomendasi makanan bagi gym enthusiast.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Mendaftarkan router...")
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