from sqlalchemy import Column, Integer, String
from app.configs.Database import Base
from typing import Dict

class UsuarioModel(Base):
    __tablename__ = "usuarios"
    
    id_usuario = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    senha = Column(String(255), nullable=False)
    
    def __init__(self, nome:str, email:str, senha:str)->None:
        self.nome = nome
        self.email = email
        self.senha = senha
    
    def __repr__(self)->str:
        return f"<Usuário {self.id_usuario}>"
    
    def to_dict(self)->Dict[str,int]:
        return{
            "id":self.id_usuario,
            "nome": self.nome,
            "email": self.email,
            "senha": self.senha
        }