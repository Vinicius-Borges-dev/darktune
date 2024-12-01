from functools import wraps
from flask import request, redirect, url_for, current_app as app, flash
from app.models import MusicasModel, CantoresMusicasModel, CantoresModel
import filetype


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
                flash("Música já cadastrada")
                return redirect(url_for("paginas.cadastro_musica"))
            return f(*args, **kwargs)
        return wrapper


    @staticmethod
    def checar_formato_imagem(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            imagem = request.files.get("imagem")
            if imagem:
                tipo_imagem = filetype.guess(imagem.read())
                imagem.seek(0)
                if tipo_imagem is None or tipo_imagem.mime not in ["image/jpeg", "image/png", "image/gif", "image/jpg"]:
                    flash("Imagem não está em um formato valido")
                    return redirect(url_for("paginas.cadastro_musica"))
            return f(*args, **kwargs)
        return wrapper
    
    @staticmethod
    def checar_formato_audio(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            musica = request.files.get("musica")
            if musica:
                tipo_arquivo = filetype.guess(musica.read())
                musica.seek(0)
                if tipo_arquivo is None or tipo_arquivo.mime not in ["audio/mpeg", "audio/wav", "audio/ogg", "audio/mp3"]:
                    flash("Audio não está em um formato valido")
                    return redirect(url_for("paginas.cadastro_musica"))
            return f(*args, **kwargs)
        return wrapper