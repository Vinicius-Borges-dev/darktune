from app.models import UsuariosModel
from flask import (
    current_app as app,
    request,
    redirect,
    url_for,
    flash,
    session,
)
import bcrypt
import os
from werkzeug.utils import secure_filename

class UsuarioController:

    def criar_novo_usuario(self):
        nome = str(request.form.get("nome"))
        email = str(request.form.get("email"))
        senha = str(request.form.get("senha"))

        try:
            usuario = app.session.query(UsuariosModel).filter_by(email=email).first()
            if usuario:
                flash("Usuário já cadastrado")
                return redirect("/")
            else:
                salt = bcrypt.gensalt()
                senha_hash = bcrypt.hashpw(senha.encode("utf-8"), salt)
                novo_usuario = UsuariosModel(
                    nome=nome,
                    email=email,
                    senha=senha_hash,
                    nivel="usuario",
                    url_perfil="",
                )
                app.session.add(novo_usuario)
                app.session.commit()
                flash("Usuário criado com sucesso!")

                return redirect("/")
        except Exception as erro:
            raise erro

    def logar(self):
        email = request.form.get("email")
        senha = request.form.get("senha")

        try:
            usuario = app.session.query(UsuariosModel).filter_by(email=email).first()

            if not usuario:
                flash("Tente com outras credenciais")
                return redirect("/")
            else:
                senhas_combinam = bcrypt.checkpw(senha.encode("utf-8"), usuario.senha)
                if senhas_combinam:
                    session["usuario"] = usuario.id_usuario
                    session["nivel"] = usuario.nivel
                    session["nome"] = usuario.nome
                    flash("Login efetuado com sucesso")
                    return redirect(url_for("paginas.home"))
                else:
                    flash("Email ou senha incorreto")
                    return redirect("/")
        except Exception as erro:
            app.session.rollback()
            flash(str(erro))
            return redirect("/")

    def deslogar(self):
        session.clear()
        return redirect("/")

    def editar_conta(self):
        novo_nome = request.form.get("nome")
        novo_email = request.form.get("email")
        nova_foto_perfil = request.files.get("foto")

        try:
            id_session = session["usuario"]
            usuario = app.session.query(UsuariosModel).get(id_session)
            
            if nova_foto_perfil:
                foto_tratada = secure_filename(nova_foto_perfil.filename)
                caminho_foto = os.path.join(app.config['UPLOADS_IMAGES_FOLDER'], foto_tratada.replace("\\","/"))
                if caminho_foto != usuario.url_foto_perfil:
                    nova_foto_perfil.save(caminho_foto)
                    usuario.url_foto_perfil = caminho_foto
                    

            usuario.nome = novo_nome
            usuario.email = novo_email

            app.session.commit()
            flash("Usuário atualizado com sucesso")
            return redirect(url_for('paginas.conta'))

        except Exception as erro:
            app.session.rollback()
            raise erro

    def deletar_conta(self):
        try:
            id_usuario = session["usuario"]

            usuario = (
                app.session.query(UsuariosModel)
                .filter_by(id_usuario=id_usuario)
                .first()
            )

            app.session.delete(usuario)
            app.session.commit()

        except Exception as erro:
            app.session.rollback()
            flash(str(erro))
            redirect()

    def capturar_dados_do_usuario(self):
        try:
            id_usuario = session["usuario"]

            usuario = (
                app.session.query(UsuariosModel)
                .filter_by(id_usuario=id_usuario)
                .first()
            )

            usuario = usuario.to_dict()

            return usuario

        except Exception as erro:
            raise erro
