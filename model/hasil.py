from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from utils.DB import Base

class Hasil(Base):
    __tablename__ = "hasil"

    id_hasil = Column(Integer, primary_key=True, autoincrement=True)
    id_pengguna = Column(Integer, ForeignKey("pengguna.id_pengguna"), nullable=False)
    id_makanan = Column(Integer, ForeignKey("makanan.id_makanan"), nullable=False)
    skor_total = Column(Float)
    ranking = Column(Integer)
    tanggal_rekomendasi = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    pengguna = relationship("Pengguna", back_populates="hasil")
    makanan = relationship("Makanan", back_populates="hasil")