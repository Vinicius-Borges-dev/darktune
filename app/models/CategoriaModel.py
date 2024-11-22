from sqlalchemy import Column, Integer, String
from app.configs.Database import Base
from typing import Dict

class CategoriaModel(Base):
    __tablename__="categorias"
    
    id_categoria = Column(Integer, primary_key=True)
    nome_categoria = Column(String(50), nullable=False)
    
    def __init__(self, nome_categoria:str)->None:
        self.nome_categoria = nome_categoria
    
    def __repr__(self)->str:
        return f"<Categoria: {self.id_categoria}>"
    
    def to_dict(self)->Dict[str,int]:
        return {
            "id", self.id_categoria,
            "nome", self.nome_categoria
        }