from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from app.controllers.MusicaController import MusicaController

musica_bp = Blueprint('musicas', __name__)

@musica_bp.route('/cadastro', methods=['POST'])
def cadastro_musica():
    return MusicaController.criar_nova_musica()

@musica_bp.route('/editar', methods=['POST'])
def editar_musica():
    pass

@musica_bp.route('/excluir', methods=['POST'])
def excluir_musica():
    pass

@musica_bp.route('/curtir', methods=['POST'])
def curtir_musica():
    pass

@musica_bp.route('/descurtir', methods=['POST'])
def descurtir_musica():
    pass

@musica_bp.route('/buscar', methods=['POST'])
def buscar_musica():
    pass

@musica_bp.route('/listar', methods=['GET'])
def listar_musicas():
    pass

@musica_bp.route('/listar/nome/<string:nome_da_musica>', methods=['GET'])
def listar_musicas_nome(nome_da_musica: str):
    pass

@musica_bp.route('/listar/categoria/<string:categoria>', methods=['GET'])
def listar_musicas_por_categoria(categoria: str):
    pass

@musica_bp.route('/listar/cantor/<string:cantor>', methods=['GET'])
def listar_musicas_por_cantor(cantor: str):
    pass
