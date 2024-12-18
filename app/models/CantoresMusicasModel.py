
from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint
from app.configs.Database import Base
from sqlalchemy.orm import relationship
from typing import Dict

class CantoresMusicasModel(Base):
    
    __tablename__ = "cantores_musicas"
    
    fk_id_cantor = Column(Integer, ForeignKey('cantores.id_cantor'), nullable=False)
    fk_id_musica = Column(Integer, ForeignKey('musicas.id_musica'), nullable=False)
    
    __table_args__ = (PrimaryKeyConstraint('fk_id_cantor', 'fk_id_musica'),)
    
    musica = relationship('MusicasModel', back_populates='cantor_musica')
    cantor = relationship('CantoresModel', back_populates='cantor_musica')
    
    def __init__(self, id_cantor:int, id_musica:int)->None:
        self.fk_id_cantor = id_cantor
        self.fk_id_musica = id_musica
    
    def __repr__(self)->str:
        return f"<CantorMusica: {self.id_cantor_musica}>"
    
    def to_dict(self)->Dict[str,int]:
        return{
            "id": self.id_cantor_musica,
            "id_cantor": self.fk_id_cantor,
            "id_musica": self.fk_id_musica
        }