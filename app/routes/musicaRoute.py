from flask import Blueprint, redirect, url_for, request
from app.controllers.MusicaController import MusicaController
from app.controllers.CurtidaController import CurtidaController
from app.middlewares.MusicaMiddleware import MusicaMiddleware
from app.middlewares.UsuarioMiddleware import UsuarioMiddleware

musica_bp = Blueprint("musicas", __name__)


@musica_bp.route("/cadastro", methods=["POST"])
@MusicaMiddleware.checar_existencia_de_musica
@MusicaMiddleware.checar_formato_imagem
@MusicaMiddleware.checar_formato_audio
def cadastro_musica():
    return MusicaController().criar_nova_musica()


@musica_bp.route("/editar/<int:id>", methods=["POST"])
@UsuarioMiddleware.verificar_permissao_admin
def editar_musica(id):
    return MusicaController().atualizar_musica(id)


@musica_bp.route("/excluir/<int:id>", methods=["GET"])
@UsuarioMiddleware.verificar_permissao_admin
def excluir_musica(id):
    return MusicaController().deletar_musica(id)


@musica_bp.route("/curtir/<int:id>", methods=["GET"])
def curtir_musica(id):
    return CurtidaController().criar_nova_curtida(id)


@musica_bp.route("/descurtir/<int:id>/<string:link>", methods=["GET"])
def descurtir_musica(id, link):
    return CurtidaController().descurtir(id, link)


@musica_bp.route("/listar/", methods=["GET"])
def listar_musicas_por_filtro():
    filtro = request.args.get("filtro")
    parametro = request.args.get("parametro")
    if filtro == "nome":
        return MusicaController().capturar_musicas_por_nome(parametro)
    elif filtro == "cantor":
        return MusicaController().capturar_musicas_por_cantor(parametro)
    elif filtro == "genero":
        return MusicaController().capturar_musicas_por_categoria(parametro)
    else:
        return redirect(url_for('paginas.musicas'))