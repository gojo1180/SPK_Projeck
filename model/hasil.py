# app/models/hasil.py
from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from utils.DB import Base

class Hasil(Base):
    __tablename__ = "hasil"

    id_hasil = Column(Integer, primary_key=True, autoincrement=True)
    id_pengguna = Column(Integer, ForeignKey("pengguna.id_pengguna"))
    id_makanan = Column(Integer, ForeignKey("makanan.id_makanan"))
    skor_total = Column(Float)
    ranking = Column(Integer)

    pengguna = relationship("Pengguna", back_populates="hasil")
    makanan = relationship("Makanan", back_populates="hasil")