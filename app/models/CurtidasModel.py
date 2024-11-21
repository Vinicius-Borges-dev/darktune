from sqlalchemy import Column, Integer, ForeignKey
from app.configs.Database import Base
from sqlalchemy.orm import relationship
from typing import Dict

class CurtidasModel(Base):
    
    __tablename__ = "curtidas"
    
    id_curtida = Column(Integer, primary_key=True)
    fk_id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False)
    fk_id_musica = Column(Integer, ForeignKey('musicas.id_musica'), nullable=False)
    
    usuario = relationship('UsuarioModel', back_populates='curtida')
    musica = relationship('MusicasModel', back_populates='curtida')
    
    def __init__(self, id_usuario:int, id_musica:int)->None:
        self.fk_id_usuario = id_usuario
        self.fk_id_musica = id_musica
    
    def __repr__(self)->str:
        return f"<Curtida: {self.id_curtida}>"
    
    def to_dict(self)->Dict[str,int]:
        return{
            "id": self.id_curtida,
            "id_usuario": self.fk_id_usuario,
            "id_musica": self.fk_id_musica
        }