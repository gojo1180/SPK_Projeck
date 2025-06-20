# models/admin.py
from sqlalchemy import Column, Integer, String
from utils.DB import Base

# gg
class Admin(Base): 
    __tablename__ = "admin"
    id_admin = Column(Integer, primary_key=True, index=True)
    email = Column(String(250), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)