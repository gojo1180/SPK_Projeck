from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from model import user, makanan, bmi, kriteria, hasil, admin, bobot_preferensi, nilai_gizi
from routes.admin import admin_auth, admin_makanan, admin_config

from utils.DB import Base, engine
from routes import pengguna_routes
from fastapi.staticfiles import StaticFiles

Base.metadata.create_all(bind=engine)


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(admin_auth.router)
app.include_router(admin_makanan.router) 
app.include_router(admin_config.router)
app.include_router(pengguna_routes.router) 


@app.get("/")
def read_root():
    return {"message": "Welcome to the Gym Food DSS API!"}



from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from model import user, makanan, bmi, kriteria, hasil, admin, bobot_preferensi, nilai_gizi
from routes.admin import admin_auth, admin_makanan, admin_config

from utils.DB import Base, engine
from routes import pengguna_routes

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
app.include_router(admin_config.router)
app.include_router(pengguna_routes.router) 


@app.get("/")
def read_root():
    return {"message": "Welcome to the Gym Food DSS API!"}


