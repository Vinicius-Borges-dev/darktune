from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.configs.Database import Base
from typing import Dict

class MusicasCategoriasModel(Base):
    
    __tablename__ = 'musicas_categorias'
    
    id_musicas_categoria = Column(Integer, primary_key=True)
    fk_id_musica = Column(Integer, ForeignKey('musicas.id_musica'))
    fk_id_categoria = Column(Integer, ForeignKey('categorias.id_categoria'))
    
    musica = relationship('MusicasModel', back_populates='musicas_categorias')
    categoria = relationship('CategoriasModel', back_populates='musicas_categorias')
    
    def __init__(self, id_musica:int, id_categoria:int)->None:
        self.fk_id_musica = id_musica
        self.fk_id_categoria = id_categoria
    
    def __repr__(self)->str:
        return f"<MusicaCategoria: {self.id_musicas_categoria}>"
    
    def to_dict(self)->Dict[str,int]:
        return{
            "id": self.id_musicas_categoria,
            "id_musica": self.fk_id_musica,
            "id_categoria": self.fk_id_categoria
        }