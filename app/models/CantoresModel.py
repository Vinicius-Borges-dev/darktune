from sqlalchemy import Column, Integer, String
from app.configs.Database import Base
from typing import Dict
from sqlalchemy.orm import relationship

class CantoresModel(Base):
    
    __tablename__ = "cantores"
    
    id_cantor = Column(Integer, primary_key=True)
    nome_cantor = Column(String(100), nullable=False)
    
    cantor_musica = relationship('CantoresMusicasModel')
    
    def __init__(self, nome_cantor:str)->None:
        self.nome_cantor = nome_cantor
    
    def __repr__(self)->str:
        return f"<Cantor: {self.id_cantor}>"
    
    def to_dict(self)->Dict[str,int]:
        return{
            "id": self.id_cantor,
            "nome": self.nome_cantor
        }