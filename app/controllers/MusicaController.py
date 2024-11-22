from flask import current_app as app, request, redirect, flash, url_for, session
from app.models import (
    MusicasModel,
    CantoresMusicasModel,
    CategoriasModel,
    MusicasCategoriasModel,
    UsuariosModel,
    CantoresModel,
)
from werkzeug.utils import secure_filename
import os

class MusicaController:

    def criar_nova_musica():
        nome_musica = str(request.form.get("nome_musica"))
        cantor = str(request.form.get("cantor"))
        cantores = [cantor.strip() for cantor in cantor.split(",")]
        categoria = str(request.form.get("categoria"))
        categorias = [categoria.strip() for categoria in categoria.split(",")]
        imagem = request.files.get("imagem")
        musica = request.files.get("musica")

        if not nome_musica or not cantor or not categoria or not imagem or not musica:
            flash("Preencha todos os campos")
            return redirect(url_for("paginas.cadastro_musica"))

        try:
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

            nova_musica = MusicasModel(
                nome_musica=nome_musica,
                url_imagem=imagem.filename,
                id_usuario=1,
            )
            app.session.add(nova_musica)
            app.session.commit()

            categorias_encontradas = []
            for nome_categoria in categorias:
                categoria = (
                    app.session.query(CategoriasModel)
                    .filter(CategoriasModel.nome_categoria == nome_categoria)
                    .first()
                )
                if not categoria:
                    categoria = CategoriasModel(nome_categoria=nome_categoria)
                    app.session.add(categoria)
                    app.session.commit()
                categorias_encontradas.append(categoria)

            for categoria in categorias_encontradas:
                musica_categoria = MusicasCategoriasModel(
                    id_musica=nova_musica.id_musica,
                    id_categoria=categoria.id_categoria,
                )
                app.session.add(musica_categoria)

            app.session.commit()
            
            imagem_path = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(imagem.filename))
            audio_path = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(musica.filename))
            
            imagem.save(imagem_path)
            musica.save(audio_path)
            
            """ flash("Música cadastrada com sucesso") 
            return redirect(url_for("paginas.cadastro_musica")) """
            return "Deu certo"

        except Exception as erro:
            raise erro

    def capturar_todas_as_musicas():
        pass

    def capturar_musicas_aleatorias_para_exibicao():
        pass

    def capturar_musicas_por_nome():
        pass

    def capturar_musicas_por_cantor():
        pass

    def capturar_musicas_por_categoria():
        pass

    def atualizar_musica(id: int):
        pass

    def deletar_musica(id: int):
        pass
