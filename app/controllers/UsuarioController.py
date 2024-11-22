from app.models import UsuariosModel
from flask import (
    current_app as app,
    request,
    render_template,
    redirect,
    url_for,
    flash,
    session,
)
import bcrypt


class UsuarioController:

    def criar_novo_usuario():
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
                    nome=nome, email=email, senha=senha_hash, nivel="usuario"
                )
                app.session.add(novo_usuario)
                app.session.commit()
                flash("Usuário criado com sucesso!")

                return redirect("/")
        except Exception as erro:
            flash(str(erro))
            redirect("/")

    def logar():
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
                    session["nivel"] = usuario.id_usuario
                    flash("Login efetuado com sucesso")
                    return redirect("/")
                else:
                    flash("Email ou senha incorreto")
                    return redirect("/")
        except Exception as erro:
            app.session.rollback()
            flash(str(erro))
            return redirect("/")

    def deslogar():
        session.clear()
        return redirect("/")

    def editar_conta():
        novo_nome = request.form.get("novo_")
        novo_email = request.form.get("email")

        try:
            id_session = session["usuario"]
            usuario = app.session.query(UsuariosModel).filter_by(id_usuario=id_session)

            usuario.nome = novo_nome
            usuario.email = novo_email

            app.session.commit()
            flash("Usuário atualizado com sucesso")
            return redirect()

        except Exception as erro:
            app.session.rollback()
            flash(str(erro))
            return redirect()

    def deletar_conta():
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

    def capturar_dados_do_usuario():
        try:
            id_usuario = session["usuario"]

            usuario = (
                app.session.query(UsuariosModel)
                .filter_by(id_usuario=id_usuario)
                .first()
            )

            return render_template()
        
        except Exception as erro:
            app.session.rollback()
            flash(str(erro))
            redirect()
    