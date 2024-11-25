from flask import Blueprint, render_template
from app.controllers.MusicaController import MusicaController
from app.controllers.ContatoController import ContatoController
from app.middlewares.UsuarioMiddleware import UsuarioMiddleware

paginas_bp = Blueprint("paginas", __name__)

@paginas_bp.route('/home')
def home():
    musicas = MusicaController().capturar_musicas_aleatorias_para_exibicao()
    return render_template('index.html', musicas=musicas)

@paginas_bp.route('/contato')
@UsuarioMiddleware.verificar_login
def contato():
    dados_contatos = ContatoController().buscar_contatos()
    return render_template('contato.html', contatos=dados_contatos)

@paginas_bp.route('/musicas')
def musicas():
    return render_template('index.html')

@paginas_bp.route('/musicas/<int:id>')
def musica(id):
    # Buscar a música pelo id
    return render_template('player.html')

@paginas_bp.route('/conta')
@UsuarioMiddleware.verificar_login
def conta():
    # (Usuário) Buscar as músicas curtidas pelo usuário
    # Buscar os contatos do(s) usuario(s)
    # (Admin) Buscar as músicas adicionadas
    return render_template('conta.html')

@paginas_bp.route('/cadastro/musica')
@UsuarioMiddleware.verificar_login
def cadastro_musica():
    return render_template('cadastro_musica.html')