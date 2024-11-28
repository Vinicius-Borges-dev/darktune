from app.models import (
    CurtidasModel,
    MusicasModel,
    UsuariosModel,
    CantoresModel,
    CantoresMusicasModel,
    CategoriasModel,
)
from flask import redirect, url_for, session, flash, current_app as app


class CurtidaController:

    def buscar_minhas_curtidas(self):
        try:
            id_usuario = session["usuario"]

            curtidas = (
                app.session.query(
                    CurtidasModel.id_curtida,
                    MusicasModel.nome_musica,
                    CantoresModel.nome_cantor,
                )
                .join(MusicasModel, CurtidasModel.fk_id_musica == MusicasModel.id_musica)
                .join(
                    CantoresMusicasModel,
                    CantoresMusicasModel.fk_id_musica == MusicasModel.id_musica,
                )
                .join(
                    CantoresModel,
                    CantoresModel.id_cantor == CantoresMusicasModel.fk_id_cantor,
                )
                .filter(CurtidasModel.fk_id_usuario == id_usuario)
                .all()
            )

            return curtidas

        except Exception as erro:
            raise erro

    def criar_nova_curtida(self, id_musica: int):
        try:
            id_usuario = session["usuario"]

            nova_curtida = CurtidasModel(
                id_usuario == id_usuario, id_musica == id_musica
            )

            app.session.add(nova_curtida)
            app.session.commit()

            flash("Curtida realizada com sucesso!")
            return redirect(url_for("paginas.musicas"))
        except Exception as erro:
            raise erro

    def descurtir(self, id_curtida: int):
        curtida = CurtidasModel.query.get(id_curtida)

        app.session.delete(curtida)
        app.session.commit()
