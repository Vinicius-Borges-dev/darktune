from flask import Blueprint
from app.controllers.ContatoController import ContatoController

contatos_bp = Blueprint("contatos", __name__)

@contatos_bp.route("/criar", methods=["POST"])
def criar_contato():
    return ContatoController().criar_novo_contato()

@contatos_bp.route("/editar/<int:id>", methods=["POST"])
def editar_contato(id):
    return ContatoController().atualizar_contato(id)

@contatos_bp.route("/deletar/<int:id>", methods=["GET"])
def deletar_contato(id):
    pass

