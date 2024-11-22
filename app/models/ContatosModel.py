from sqlalchemy import Column, Integer, String, Text
from app.configs.Database import Base
from typing import Dict
from sqlalchemy.orm import relationship


class ContatosModel(Base):

    __tablename__ = "contatos"

    id_contato = Column(Integer, primary_key=True)
    mensagem = Column(Text, nullable=False)
    
    contatos_usuarios = relationship('ContatosUsuariosModel', back_populates='contato')

    def __init__(self, mensagem: str) -> None:
        self.mensagem = mensagem

    def __repr___(self) -> str:
        return f"<Contato: {self.id_contato}>"

    def to_dict(self) -> Dict[str, int]:
        return {"id": self.id_contato, "mensagem": self.mensagem}
