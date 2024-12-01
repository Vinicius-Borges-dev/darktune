from flask import Blueprint
from app.controllers.UsuarioController import UsuarioController

usuario_bp = Blueprint("usuarios", __name__)


@usuario_bp.route("/login", methods=["POST"])
def login_usuario():
    return UsuarioController().logar()


@usuario_bp.route("/logout")
def deslogar_usuario():
    return UsuarioController().deslogar()


@usuario_bp.route("/cadastro", methods=["POST"])
def cadastro_usuario():
    return UsuarioController().criar_novo_usuario()


@usuario_bp.route("/editar", methods=["POST"])
def editar_usuario():
    return UsuarioController().editar_conta()