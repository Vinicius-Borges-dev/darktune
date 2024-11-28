from flask import Blueprint
from app.controllers.MusicaController import MusicaController
from app.middlewares.MusicaMiddleware import MusicaMiddleware
from app.controllers.CurtidaController import CurtidaController

musica_bp = Blueprint('musicas', __name__)


@musica_bp.route('/cadastro', methods=['POST'])
@MusicaMiddleware.checar_existencia_de_musica
def cadastro_musica():
    return MusicaController().criar_nova_musica()

@musica_bp.route('/editar', methods=['POST'])
def editar_musica():
    pass

@musica_bp.route('/excluir/<int:id>', methods=['GET'])
def excluir_musica(id):
    return MusicaController().deletar_musica(id)

@musica_bp.route('/curtir/<int:id>', methods=['GET'])
def curtir_musica(id):
    return CurtidaController().criar_nova_curtida(id)

@musica_bp.route('/descurtir/<int:id>', methods=['GET'])
def descurtir_musica(id):
    pass

@musica_bp.route('/listar', methods=['GET'])
def listar_musicas():
    return MusicaController().capturar_musicas_aleatorias_para_exibicao()

@musica_bp.route('/listar/nome/<string:nome_da_musica>', methods=['GET'])
def listar_musicas_nome(nome_da_musica: str):
    pass

@musica_bp.route('/listar/categoria/<string:categoria>', methods=['GET'])
def listar_musicas_por_categoria(categoria: str):
    pass

@musica_bp.route('/listar/cantor/<string:cantor>', methods=['GET'])
def listar_musicas_por_cantor(cantor: str):
    pass
