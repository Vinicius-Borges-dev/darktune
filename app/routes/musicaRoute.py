from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from app.controllers.MusicaController import MusicaController


musica_bp = Blueprint('musica_bp', __name__)

@musica_bp.route('/musica/cadastro', methods=['POST'])
def cadastro_musica():
    return MusicaController.criar_nova_musica()

@musica_bp.route('/musica/editar', methods=['POST'])
def editar_musica():
    pass

@musica_bp.route('/musica/excluir', methods=['POST'])
def excluir_musica():
    pass

@musica_bp.route('/musica/curtir', methods=['POST'])
def curtir_musica():
    pass

@musica_bp.route('/musica/descurtir', methods=['POST'])
def descurtir_musica():
    pass

@musica_bp.route('/musica/buscar', methods=['POST'])
def buscar_musica():
    pass

@musica_bp.route('/musica/listar', methods=['GET'])
def listar_musicas():
    pass

@musica_bp.route('/musica/listar/<str:nome_da_musica>', methods=['GET'])
def listar_musicas_nome(nome_da_musica:str):
    pass

@musica_bp.route('/musica/listar/<str:categoria>', methods=['GET'])
def listar_musicas_por_categoria(categoria:str):
    pass

@musica_bp.route('/musica/listar/<str:cantor>', methods=['GET'])
def listar_musicas_por_cantor(cantor:str):
    pass