from flask import (
    current_app as app,
    request,
    redirect,
    flash,
    url_for,
    session,
    render_template,
)
from app.models import (
    MusicasModel,
    CantoresMusicasModel,
    CategoriasModel,
    MusicasCategoriasModel,
    CantoresModel,
    CurtidasModel,
)
from werkzeug.utils import secure_filename
import os


class MusicaController:

    def criar_nova_musica(self):
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
            caminho_imagem = os.path.join(
                app.config["UPLOAD_IMAGES_FOLDER"], secure_filename(imagem.filename)
            ).replace("\\", "/")

            caminho_audio = os.path.join(
                app.config["UPLOAD_AUDIOS_FOLDER"], secure_filename(musica.filename)
            ).replace("\\", "/")

            nova_musica = MusicasModel(
                nome_musica=nome_musica.lower(),
                url_imagem=caminho_imagem,
                url_audio=caminho_audio,
                id_usuario=1,
            )

            app.session.add(nova_musica)
            app.session.commit()

            categorias_encontradas = self.encontrar_categorias(categorias)

            for categoria in categorias_encontradas:
                musica_categoria = MusicasCategoriasModel(
                    id_musica=nova_musica.id_musica,
                    id_categoria=categoria.id_categoria,
                )
                app.session.add(musica_categoria)

            cantores_encontrados = self.encontrar_cantores(cantores)

            for cantor in cantores_encontrados:
                cantores_musicas = CantoresMusicasModel(
                    id_musica=nova_musica.id_musica,
                    id_cantor=cantor.id_cantor,
                )
                app.session.add(cantores_musicas)

            app.session.commit()

            imagem.save(caminho_imagem)
            musica.save(caminho_audio)

            flash("Música cadastrada com sucesso")
            return redirect(url_for("paginas.cadastro_musica"))

        except Exception as erro:
            raise erro

    def capturar_todas_as_musicas(self):
        usuario_id = session.get("usuario")
        try:
            musicas = app.session.query(MusicasModel).all()

            if not musicas:
                return "Nenhuma música encontrada.", False

            lista_musicas = []
            for musica in musicas:
                musica_dict = musica.to_dict()

                curtida = (
                    app.session.query(CurtidasModel)
                    .filter(
                        CurtidasModel.fk_id_usuario == usuario_id,
                        CurtidasModel.fk_id_musica == musica.id_musica,
                    )
                    .first()
                )

                if not curtida:
                    musica_dict["curtida_usuario"] = 0
                else:
                    musica_dict["curtida_usuario"] = 1
                    musica_dict["id_curtida"] = curtida.id_curtida

                nome_cantores = (
                    app.session.query(CantoresModel.nome_cantor)
                    .join(
                        CantoresMusicasModel,
                        CantoresMusicasModel.fk_id_cantor == CantoresModel.id_cantor,
                    )
                    .join(
                        MusicasModel,
                        MusicasModel.id_musica == CantoresMusicasModel.fk_id_musica,
                    )
                    .filter(MusicasModel.id_musica == musica.id_musica)
                    .all()
                )
                
                nome_categorias = (
                    app.session.query(CategoriasModel.nome_categoria)
                    .join(
                        MusicasCategoriasModel,
                        MusicasCategoriasModel.fk_id_categoria == CategoriasModel.id_categoria,
                    )
                    .join(
                        MusicasModel,
                        MusicasModel.id_musica == MusicasCategoriasModel.fk_id_musica,
                    ).filter(MusicasModel.id_musica == musica.id_musica)
                    .all()
                )

                musica_dict["cantores"] = [cantor[0] for cantor in nome_cantores]
                musica_dict["categorias"] = [categoria[0] for categoria in nome_categorias]
                musica_dict["url_imagem"] = musica_dict["url_imagem"].split("/")[-1]
                lista_musicas.append(musica_dict)

            return lista_musicas, True
        except Exception as erro:
            raise erro

    def capturar_musicas_aleatorias_para_exibicao(self):
        try:
            musicas = app.session.query(MusicasModel).limit(6)
            lista_musicas = [musica.to_dict() for musica in musicas]
            for musica in lista_musicas:
                nome_cantores = (
                    app.session.query(CantoresModel.nome_cantor)
                    .join(
                        CantoresMusicasModel,
                        CantoresMusicasModel.fk_id_cantor == CantoresModel.id_cantor,
                    )
                    .join(
                        MusicasModel,
                        MusicasModel.id_musica == CantoresMusicasModel.fk_id_musica,
                    )
                    .filter(MusicasModel.id_musica == musica["id"])
                    .all()
                )

                musica["cantores"] = [cantor[0] for cantor in nome_cantores]
                musica["url_imagem"] = musica["url_imagem"].split("/")[-1]

            return lista_musicas
        except Exception as erro:
            raise erro

    def capturar_musicas_por_nome(self, nome: str):
        try:
            musicas = (
                app.session.query(MusicasModel)
                .filter(MusicasModel.nome_musica.like(f"%{nome.lower()}%"))
                .all()
            )

            if not musicas:
                flash("Música não encontrada.")
                return redirect(url_for("paginas.musicas"))

            lista_musicas = [musica.to_dict() for musica in musicas]
            for musica in lista_musicas:

                curtida = (
                    app.session.query(CurtidasModel)
                    .filter(
                        CurtidasModel.fk_id_usuario == session.get("usuario"),
                        CurtidasModel.fk_id_musica == musica.get("id_musica"),
                    )
                    .first()
                )

                if not curtida:
                    musica["curtida_usuario"] = 0
                else:
                    musica["curtida_usuario"] = 1
                    musica["id_curtida"] = curtida.id_curtida

                nome_cantores = (
                    app.session.query(CantoresModel.nome_cantor)
                    .join(
                        CantoresMusicasModel,
                        CantoresMusicasModel.fk_id_cantor == CantoresModel.id_cantor,
                    )
                    .join(
                        MusicasModel,
                        MusicasModel.id_musica == CantoresMusicasModel.fk_id_musica,
                    )
                    .filter(MusicasModel.id_musica == musica["id"])
                    .all()
                )

                musica["cantores"] = [cantor[0] for cantor in nome_cantores]
                musica["url_imagem"] = musica["url_imagem"].split("/")[-1]

            return render_template("musicas.html", musicas=(lista_musicas, True))

        except Exception as erro:
            raise erro

    def capturar_musicas_por_cantor(self, cantor: str):
        try:
            musicas = (
                app.session.query(MusicasModel)
                .join(
                    CantoresMusicasModel,
                    CantoresMusicasModel.fk_id_musica == MusicasModel.id_musica,
                )
                .join(
                    CantoresModel,
                    CantoresModel.id_cantor == CantoresMusicasModel.fk_id_cantor,
                )
                .filter(CantoresModel.nome_cantor.like(f"%{cantor.lower()}%"))
                .all()
            )

            if not musicas:
                flash("Música não encontrada.")
                return redirect(url_for("paginas.musicas"))

            lista_musicas = [musica.to_dict() for musica in musicas]
            for musica in lista_musicas:

                curtida = (
                    app.session.query(CurtidasModel)
                    .filter(
                        CurtidasModel.fk_id_usuario == session.get("usuario"),
                        CurtidasModel.fk_id_musica == musica.get("id_musica"),
                    )
                    .first()
                )

                if not curtida:
                    musica["curtida_usuario"] = 0
                else:
                    musica["curtida_usuario"] = 1
                    musica["id_curtida"] = curtida.id_curtida

                nome_cantores = (
                    app.session.query(CantoresModel.nome_cantor)
                    .join(
                        CantoresMusicasModel,
                        CantoresMusicasModel.fk_id_cantor == CantoresModel.id_cantor,
                    )
                    .join(
                        MusicasModel,
                        MusicasModel.id_musica == CantoresMusicasModel.fk_id_musica,
                    )
                    .filter(MusicasModel.id_musica == musica["id"])
                    .all()
                )

                musica["cantores"] = [cantor[0] for cantor in nome_cantores]
                musica["url_imagem"] = musica["url_imagem"].split("/")[-1]

            return render_template("musicas.html", musicas=(lista_musicas, True))

        except Exception as erro:
            raise erro

    def capturar_musicas_por_categoria(self, categoria: str):
        try:
            musicas = (
                app.session.query(MusicasModel)
                .join(
                    MusicasCategoriasModel,
                    MusicasCategoriasModel.fk_id_musica == MusicasModel.id_musica,
                )
                .join(
                    CategoriasModel,
                    CategoriasModel.id_categoria
                    == MusicasCategoriasModel.fk_id_categoria,
                )
                .filter(CategoriasModel.nome_categoria.like(f"%{categoria.lower()}%"))
                .all()
            )

            if not musicas:
                flash("Música não encontrada.")
                return redirect(url_for("paginas.musicas"))

            lista_musicas = [musica.to_dict() for musica in musicas]
            for musica in lista_musicas:

                curtida = (
                    app.session.query(CurtidasModel)
                    .filter(
                        CurtidasModel.fk_id_usuario == session.get("usuario"),
                        CurtidasModel.fk_id_musica == musica.get("id_musica"),
                    )
                    .first()
                )

                if not curtida:
                    musica["curtida_usuario"] = 0
                else:
                    musica["curtida_usuario"] = 1
                    musica["id_curtida"] = curtida.id_curtida

                nome_cantores = (
                    app.session.query(CantoresModel.nome_cantor)
                    .join(
                        CantoresMusicasModel,
                        CantoresMusicasModel.fk_id_cantor == CantoresModel.id_cantor,
                    )
                    .join(
                        MusicasModel,
                        MusicasModel.id_musica == CantoresMusicasModel.fk_id_musica,
                    )
                    .filter(MusicasModel.id_musica == musica["id"])
                    .all()
                )

                musica["cantores"] = [cantor[0] for cantor in nome_cantores]
                musica["url_imagem"] = musica["url_imagem"].split("/")[-1]

            return render_template("musicas.html", musicas=(lista_musicas, True))

        except Exception as erro:
            raise erro

    def buscar_dados_da_musica(self, id: int):
        try:
            musica = (
                app.session.query(MusicasModel)
                .filter(MusicasModel.id_musica == id)
                .first()
            )

            if not musica:
                return "Nenhuma música encontrada."

            musica = musica.to_dict()

            nome_cantores = (
                app.session.query(CantoresModel.nome_cantor)
                .join(
                    CantoresMusicasModel,
                    CantoresMusicasModel.fk_id_cantor == CantoresModel.id_cantor,
                )
                .join(
                    MusicasModel,
                    MusicasModel.id_musica == CantoresMusicasModel.fk_id_musica,
                )
                .filter(MusicasModel.id_musica == musica["id"])
                .all()
            )

            curtida = (
                app.session.query(CurtidasModel)
                .filter(
                    CurtidasModel.fk_id_usuario == session.get("usuario"),
                    CurtidasModel.fk_id_musica == musica.get("id_musica"),
                )
                .first()
            )

            if not curtida:
                musica["curtida_usuario"] = 0
            else:
                musica["curtida_usuario"] = 1
                musica["id_curtida"] = curtida.id_curtida

            nome_categorias = (
                app.session.query(CategoriasModel.nome_categoria)
                .join(
                    MusicasCategoriasModel,
                    MusicasCategoriasModel.fk_id_categoria
                    == CategoriasModel.id_categoria,
                )
                .join(
                    MusicasModel,
                    MusicasModel.id_musica == MusicasCategoriasModel.fk_id_musica,
                )
                .filter(MusicasModel.id_musica == musica["id"])
                .all()
            )

            musica["cantores"] = [cantor[0] for cantor in nome_cantores]
            musica["categorias"] = [categoria[0] for categoria in nome_categorias]
            musica["url_imagem"] = musica["url_imagem"].split("/")[-1]
            musica["url_audio"] = musica["url_audio"].split("/")[-1]

            return musica

        except Exception as erro:
            raise erro

    def atualizar_musica(self, id: int):
        nome_musica = str(request.form.get("nome_musica"))
        cantor = str(request.form.get("cantor"))
        cantores = [cantor.strip() for cantor in cantor.split(",")]
        categoria = str(request.form.get("categoria"))
        categorias = [categoria.strip() for categoria in categoria.split(",")]
        imagem = request.files.get("imagem")
        musica = request.files.get("musica")

        try:
            musica_atual = app.session.query(MusicasModel).get(id)
            if not musica_atual:
                flash("Música não encontrada")
                return redirect(url_for("formularios.form_editar_musica", id=id))

            musica_atual.nome_musica = nome_musica.lower()

            if imagem:
                caminho_imagem_atual = os.path.join(
                    app.config["UPLOAD_IMAGES_FOLDER"], secure_filename(imagem.filename)
                ).replace("\\", "/")
                if caminho_imagem_atual != musica_atual.url_imagem:
                    imagem.save(caminho_imagem_atual)
                    musica_atual.url_imagem = caminho_imagem_atual

            if musica:
                caminho_audio_atual = os.path.join(
                    app.config["UPLOAD_AUDIOS_FOLDER"], secure_filename(musica.filename)
                ).replace("\\", "/")
                if caminho_audio_atual != musica_atual.url_audio:
                    musica.save(caminho_audio_atual)
                    musica_atual.url_audio = caminho_audio_atual

            categorias_encontradas = self.encontrar_categorias(categorias)
            musica_atual.categorias = categorias_encontradas

            cantores_encontrados = self.encontrar_cantores(cantores)
            musica_atual.cantores = cantores_encontrados

            app.session.commit()

            flash("Música atualizada com sucesso")
            return redirect(url_for("paginas.conta"))

        except Exception as erro:
            app.session.rollback()
            flash(f"Erro ao atualizar música: {erro}")
            return redirect(url_for("formularios.form_editar_musica", id=id))

    def deletar_musica(self, id: int):
        try:
            musica = (
                app.session.query(MusicasModel)
                .filter(MusicasModel.id_musica == id)
                .first()
            )

            imagem = musica.url_imagem
            audio = musica.url_audio

            os.remove(imagem)
            os.remove(audio)

            app.session.delete(musica)
            app.session.commit()

            flash("Musica deletada.")
            return redirect(url_for("paginas.conta"))

        except Exception as erro:
            raise erro

    def encontrar_categorias(self, categorias: list[str]):
        categorias_encontradas = []
        for nome_categoria in categorias:
            categoria = (
                app.session.query(CategoriasModel)
                .filter(CategoriasModel.nome_categoria == nome_categoria.lower())
                .first()
            )
            if not categoria:
                categoria = CategoriasModel(nome_categoria=nome_categoria.lower())
                app.session.add(categoria)
                app.session.commit()
            categorias_encontradas.append(categoria)
        return categorias_encontradas

    def encontrar_cantores(self, cantores: list[str]):
        cantores_encontrados = []
        for nome_cantor in cantores:
            cantor = (
                app.session.query(CantoresModel)
                .filter(CantoresModel.nome_cantor == nome_cantor.lower())
                .first()
            )
            if not cantor:
                cantor = CantoresModel(nome_cantor=nome_cantor.lower())
                app.session.add(cantor)
                app.session.commit()
            cantores_encontrados.append(cantor)
        return cantores_encontrados
