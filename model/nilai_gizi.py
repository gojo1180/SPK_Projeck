from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from utils.DB import Base

class NilaiGizi(Base):
    __tablename__ = "nilai_gizi"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_makanan = Column(Integer, ForeignKey("makanan.id_makanan"), nullable=False)
    id_kriteria = Column(Integer, ForeignKey("kriteria.id_kriteria"), nullable=False)
    nilai = Column(Float, nullable=False)
    
    # Relationships
    makanan = relationship("Makanan", back_populates="nilai_gizi")
    kriteria = relationship("Kriteria", back_populates="nilai_gizi")
