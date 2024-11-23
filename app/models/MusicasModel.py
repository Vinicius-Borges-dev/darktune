from sqlalchemy import Column, Integer, String, ForeignKey
from app.configs.Database import Base
from sqlalchemy.orm import relationship
from typing import Dict


class MusicasModel(Base):

    __tablename__ = "musicas"

    id_musica = Column(Integer, primary_key=True)
    nome_musica = Column(String(150), nullable=False)
    url_imagem = Column(String(255), nullable=False)
    fk_id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)

    usuario = relationship("UsuariosModel", back_populates="musicas")
    musicas_categorias = relationship("MusicasCategoriasModel", back_populates="musica")
    curtida = relationship("CurtidasModel")
    cantor_musica = relationship("CantoresMusicasModel")

    def __init__(self, nome_musica: str, url_imagem: str, id_usuario: int) -> None:
        self.nome_musica = nome_musica
        self.url_imagem = url_imagem
        self.fk_id_usuario = id_usuario

    def __repr__(self) -> str:
        return f"<Musica: {self.id_musica}>"

    def to_dict(self) -> Dict[str, int]:
        return {
            "id": self.id_musica,
            "nome": self.nome_musica,
            "url_imagem": self.url_imagem,
            "id_usuario": self.fk_id_usuario,
        }
