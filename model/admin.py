from sqlalchemy import Column, Integer, String
from utils.DB import Base

class User(Base):
    __tablename__ = "admin"

    id_admin = Column(Integer, primary_key=True, index=True)
    email = Column(String(250), unique=True, index=True)
    Password = Column(String(250))
