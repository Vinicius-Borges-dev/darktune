from flask import Blueprint, render_template
from app.controllers.MusicaController import MusicaController
from app.controllers.ContatoController import ContatoController
from app.middlewares.UsuarioMiddleware import UsuarioMiddleware
from app.controllers.UsuarioController import UsuarioController
from app.controllers.CurtidaController import CurtidaController

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
    musicas = MusicaController().capturar_todas_as_musicas()
    return render_template('musicas.html', musicas=musicas)

@paginas_bp.route('/musica/<int:id>')
def musica(id):
    # Buscar a música pelo id
    musica = None
    return render_template('player.html', musica=musica)

@paginas_bp.route('/conta')
@UsuarioMiddleware.verificar_login
def conta():
    dados_usuario = UsuarioController().capturar_dados_do_usuario()

    curtidas = CurtidaController().buscar_minhas_curtidas()

    musicas_adicionadas = None

    return render_template('conta.html', dados=dados_usuario, curtidas=curtidas, musicas_adicionadas=musicas_adicionadas)

@paginas_bp.route('/cadastro/musica')
@UsuarioMiddleware.verificar_login
def cadastro_musica():
    return render_template('cadastro_musica.html')