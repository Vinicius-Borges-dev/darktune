from functools import wraps
from flask import request, redirect, url_for, current_app as app
from app.models import MusicasModel, CantoresMusicasModel, CantoresModel


class MusicaMiddleware:

    @staticmethod
    def checar_existencia_de_musica(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            nome_musica = request.form.get("nome_musica").lower()
            cantor = request.form.get("cantor").lower()
            cantores = [cantor.strip() for cantor in cantor.split(",")]

            musica_existente = (
                app.session.query(MusicasModel)
                .join(
                    CantoresMusicasModel,
                    CantoresMusicasModel.fk_id_musica == MusicasModel.id_musica,
                )
                .join(
                    CantoresModel,
                    CantoresModel.id_cantor == CantoresMusicasModel.fk_id_cantor,
                )
                .filter(
                    MusicasModel.nome_musica == nome_musica,
                    CantoresModel.nome_cantor.in_(cantores),
                )
                .first()
            )

            if musica_existente:
                # flash("Música já cadastrada")
                # return redirect(url_for("paginas.cadastro_musica"))
                return "Música ja cadastrada"
            return f(*args, **kwargs)
        return wrapper
