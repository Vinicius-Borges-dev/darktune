from sqlalchemy import Column, Integer, String, ForeignKey
from app.configs.Database import Base
from typing import Dict
from sqlalchemy.orm import relationship


class ContatosUsuariosModel(Base):

    __tablename__ = "contatos_usuarios"

    id_contato_usuario = Column(Integer, primary_key=True)
    fk_id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    fk_id_contato = Column(Integer, ForeignKey("contatos.id_contato"), nullable=False)
    
    usuario = relationship('UsuariosModel', back_populates='contatos_usuarios')
    contato = relationship('ContatosModel', back_populates='contatos_usuarios')

    def __init__(self, id_usuario: int, id_contato: int) -> None:
        self.fk_id_usuario = id_usuario
        self.fk_id_contato = id_contato

    def __repr__(self) -> str:
        return f"<ContatoUsuario: {self.id_contato_usuario}>"

    def to_dict(self) -> Dict[str, int]:
        return {
            "id": self.id_contato_usuario,
            "id_usuario": self.fk_id_usuario,
            "id_contato": self.fk_id_contato,
        }
