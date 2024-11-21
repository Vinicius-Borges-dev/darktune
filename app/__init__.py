from flask import Flask, render_template
from .configs.Database import Database
from flask_sqlalchemy import SQLAlchemy
from app.models import CantoresModel,CantoresMusicasModel,MusicasModel,CategoriasModel,UsuariosModel,CurtidasModel,MusicasCategoriasModel

banco_de_dados = SQLAlchemy()

def create_app()->Flask:
    app = Flask(__name__)
    app.config.from_pyfile(os.path.join("configs", "settings.py"))
    
    app.config['SECRET_KEY'] = app.config.get("SECRET_KEY")
    app.config['UPLOAD_FOLDER'] = "src/static/uploads"
    
    engine = Database.criar_conexao(app)
    app.engine = engine
    
    banco_de_dados.init_app(app)
    
    with app.app_context():
        Database.criar_tabelas()
        
    @app.route("/")
    def index():
        return render_template('login.html')
    
    from app.routes.paginasRoute import paginas_bp
    app.register_blueprint(paginas_bp, url_prefix='/paginas')
    
    from app.routes.usuarioRoute import usuario_bp
    app.register_blueprint(usuario_bp, url_prefix='/usuario')
        
    return app

