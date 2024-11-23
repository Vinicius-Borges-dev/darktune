from sqlalchemy import Column, Integer, String
from app.configs.Database import Base
from typing import Dict
from sqlalchemy.orm import relationship

class UsuariosModel(Base):
    __tablename__ = "usuarios"
    
    id_usuario = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    senha = Column(String(255), nullable=False)
    nivel = Column(String(20), nullable=False)
    
    curtida = relationship('CurtidasModel', back_populates='usuario')
    musicas = relationship('MusicasModel', back_populates='usuario')
    contatos_usuarios = relationship('ContatosUsuariosModel')
    
    def __init__(self, nome:str, email:str, senha:str, nivel:str)->None:
        self.nome = nome
        self.email = email
        self.senha = senha
        self.nivel = nivel
    
    def __repr__(self)->str:
        return f"<Usuário {self.id_usuario}>"
    
    def to_dict(self)->Dict[str,int]:
        return{
            "id":self.id_usuario,
            "nome": self.nome,
            "email": self.email,
            "senha": self.senha
        }