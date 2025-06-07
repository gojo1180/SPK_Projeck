from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from utils.DB import Base

class NilaiGizi(Base):
    __tablename__ = "nilai_gizi"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_makanan = Column(Integer, ForeignKey("makanan.id_makanan"), nullable=False)
    id_kriteria = Column(Integer, ForeignKey("kriteria.id_kriteria"), nullable=False)
    nilai = Column(Float, nullable=False)
    
    # FK ke pengguna, diisi jika ini makanan custom buatan pengguna
    id_pengguna_pembuat = Column(Integer, ForeignKey("pengguna.id_pengguna"), nullable=True)

    # Relationships
    makanan = relationship("Makanan", back_populates="nilai_gizi")
    kriteria = relationship("Kriteria", back_populates="nilai_gizi")
    pembuat = relationship("Pengguna", back_populates="nilai_gizi_custom")