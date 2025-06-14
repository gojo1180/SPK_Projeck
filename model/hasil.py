# app/models/hasil.py
from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, func, String, DateTime, Text
from sqlalchemy.orm import relationship
from utils.DB import Base
from datetime import datetime

mode_penggunaan = Column(String, default="preset")

class Hasil(Base):
    __tablename__ = "hasil"

    id_hasil = Column(Integer, primary_key=True, autoincrement=True)
    id_pengguna = Column(Integer, ForeignKey("pengguna.id_pengguna"), nullable=False)
    id_makanan = Column(Integer, ForeignKey("makanan.id_makanan"), nullable=False)
    skor_total = Column(Float)
    ranking = Column(Integer)
    tanggal_rekomendasi = Column(DateTime(timezone=True), server_default=func.now())
    fase_latihan = Column(Text)
    waktu_makan = Column(Text)


    # Relationships
    pengguna = relationship("Pengguna", back_populates="hasil")
    makanan = relationship("Makanan", back_populates="hasil")