from flask import Blueprint, request, render_template, redirect, url_for, flash, session
import bcrypt
from app.models import UsuariosModel
from flask import current_app as app

usuario_bp = Blueprint("usuarios", __name__)


@usuario_bp.route("/login", methods=["POST"])
def login_usuario():
    pass


@usuario_bp.route("/logout")
def logout_usuario():
    pass


@usuario_bp.route("/cadastro", methods=["POST"])
def cadastro_usuario():
    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha")

    usuario = app.session.query(UsuariosModel).filter_by(email=email).first()
    if usuario:
        flash("Usuário já cadastrado")
        return redirect("/")
    else:
        novo_usuario = UsuariosModel(nome=nome, email=email, senha=senha)
        app.session.add(novo_usuario)
        app.session.commit()

        return redirect("/")


@usuario_bp.route("/perfil")
def perfil_usuario():
    pass


@usuario_bp.route("/perfil/editar", methods=["POST"])
def editar_perfil_usuario():
    pass


@usuario_bp.route("/perfil/excluir", methods=["POST"])
def excluir_perfil_usuario():
    pass
