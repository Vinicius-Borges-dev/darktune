from flask import Blueprint, render_template
from app.controllers.ContatoController import ContatoController
from app.controllers.MusicaController import MusicaController
from app.controllers.UsuarioController import UsuarioController

formulario_bp = Blueprint("formularios", __name__)

@formulario_bp.route("/editar/contato/<int:id>",  methods=["GET"])
def form_editar_contato(id):
    dados = ContatoController().buscar_dados_de_contato(id)
    return render_template("editar_contato.html", contato=dados)

@formulario_bp.route("/editar/musica/<int:id>",  methods=["GET"])
def form_editar_musica(id):
    dados = None
    return render_template("editar_musica.html")