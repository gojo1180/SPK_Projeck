from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.DB import Base, engine
from routes import pengguna_routes

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(pengguna_routes.router)