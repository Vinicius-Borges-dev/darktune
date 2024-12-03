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
                    MusicasModel.id_musica,
                    MusicasModel.url_imagem,
                    CantoresModel.nome_cantor,
                )
                .join(
                    MusicasModel, CurtidasModel.fk_id_musica == MusicasModel.id_musica
                )
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
            
            musicas_dict = {}
            for (
                id,
                nome_musica,
                id_musica,
                imagem,
                cantor
            ) in curtidas:
                if id not in musicas_dict:
                    musicas_dict[id] = {
                        "id":id,
                        "nome_musica":nome_musica,
                        "musica_id":id_musica,
                        "imagem":imagem.split('/')[-1],
                        "cantores":[]
                    }
                musicas_dict[id]['cantores'].append(cantor)
            
            lista_musicas = list(musicas_dict.values())

            return lista_musicas 

        except Exception as erro:
            raise erro

    def criar_nova_curtida(self, musica_id: int):
        try:
            usuario_id = session["usuario"]

            curtida_existente = (
                app.session.query(CurtidasModel)
                .filter(
                    CurtidasModel.fk_id_musica == musica_id,
                    CurtidasModel.fk_id_usuario == usuario_id,
                )
                .first()
            )

            if curtida_existente:
                flash("Música ja foi curtida!")
                return redirect(url_for("paginas.musicas"))
            else:
                nova_curtida = CurtidasModel(id_usuario=usuario_id, id_musica=musica_id)

                app.session.add(nova_curtida)
                app.session.commit()
                flash("Curtida realizada com sucesso!")
                return redirect(url_for("paginas.musicas"))
        except Exception as erro:
            raise erro

    def descurtir(self, id_curtida: int, link:str):
        try:
            curtida = app.session.query(CurtidasModel).filter(CurtidasModel.id_curtida == id_curtida).first()
            app.session.delete(curtida)
            app.session.commit()
            
            flash("Descurtida realizada.")
            return redirect(url_for(f"{link}"))
        except Exception as erro:
            raise erro
