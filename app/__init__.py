from flask import Flask
from .configs.Database import Database
from flask_sqlalchemy import SQLAlchemy
import os
from app.models import CantoresModel,CantoresMusicasModel,MusicasModel,CategoriasModel,UsuariosModel,CurtidasModel,MusicasCategoriasModel

banco_de_dados = SQLAlchemy()

def create_app()->Flask:
    app = Flask(__name__)
    
    app.config.from_pyfile(os.path.join("configs", "settings.py"))
    print(app.config['SECRET_KEY'])
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['UPLOAD_FOLDER'] = "src/static/uploads"
    
    engine = Database.criar_conexao(app)
    app.engine = engine
    
    banco_de_dados.init_app(app)
    
    with app.app_context():
        Database.criar_tabelas()
        
    from app.routes.mainRoute import main_bp
    app.register_blueprint(main_bp)
        
    return app

