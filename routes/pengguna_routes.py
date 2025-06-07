from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.DB import get_db
from schema.pengguna_schema import UserCreate, UserLogin
from controller.pengguna_controller import register_user, login_user

router = APIRouter(
    prefix="/api",
    tags=["Pengguna"]
)

@router.post("/register")
def api_register(user: UserCreate, db: Session = Depends(get_db)):
    result = register_user(db, user)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return {"message": result["message"]}

@router.post("/login")
def api_login(credentials: UserLogin, db: Session = Depends(get_db)):
    result = login_user(db, credentials)
    if not result["success"]:
        raise HTTPException(status_code=401, detail=result["message"])
    return result
