from flask import Flask
from .configs.Database import Database

from flask_sqlalchemy import SQLAlchemy
import os

banco_de_dados = SQLAlchemy()

def create_app()->Flask:
    app = Flask(__name__)
    
    print(app.config['SECRET_KEY'])
    # app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    # app.config['UPLOAD_FOLDER'] = "src/static/uploads"
    app.config.from_pyfile(os.path.join("configs", "settings.py"))
    
    """ engine = Database.criar_conexao(app)
    app.engine = engine
    
    banco_de_dados.init_app(app)
    
    with app.app_context():
        Database.criar_tabelas() """
        
    @app.route("/")
    def index():
        return f"Iniciado com sucesso\n{ app.config.get('SECRET_KEY') }"
        
    return app

