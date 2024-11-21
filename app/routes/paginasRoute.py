from flask import Blueprint, render_template

paginas_bp = Blueprint("paginas", __name__)

@paginas_bp.route('/home')
def home():
    # Buscar outras 6 músicas aletórias para exibir na home
    return render_template('home.html')

@paginas_bp.route('/contato')
def contato():
    return render_template('contato.html')

@paginas_bp.route('/musicas')
def musicas():
    # Listar todas as músicas
    return render_template('musicas.html')

@paginas_bp.route('/musicas/<int:id>')
def musica(id):
    # Buscar a música pelo id
    return render_template('player.html')

@paginas_bp.route('/conta/<int:id>')
def conta(id:int):
    # Buscar a conta do usuário pelo id
    # Buscar as músicas curtidas pelo usuário
    return render_template('conta.html')