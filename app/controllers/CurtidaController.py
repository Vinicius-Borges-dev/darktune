from app.models import CurtidasModel, MusicasModel, UsuariosModel, CantoresModel
from flask import redirect, url_for, session, flash, current_app as app


class CurtidaController:

    def buscar_minhas_curtidas(self):
        id_usuario = session["usuario"]

        curtidas = (
            app.session.query(
                CurtidasModel.id_curtida,
                MusicasModel.nome_musica,
            )
            .join(MusicasModel, CurtidasModel.fk_id_musica == MusicasModel.id_musica)
            .filter(CurtidasModel.fk_id_usuario == id_usuario)
            .all()
        )
        
        for curtida in curtidas:
            cantores = (
                app.session.query(CantoresModel)
                .join(MusicasModel, CantoresModel.id_cantor == MusicasModel.fk_id_cantor)
                .filter(MusicasModel.nome_musica == curtida.nome_musica)
                .all()
            )
            
            lista_cantores = [cantor.nome_cantor for cantor in cantores]
            curtida["cantores"] = lista_cantores
        
        return curtidas

    def criar_nova_curtida(self, id_musica: int):
        pass

    def descurtir(self, id_curtida: int):
        curtida = CurtidasModel.query.get(id_curtida)

        app.session.delete(curtida)
        app.session.commit()
