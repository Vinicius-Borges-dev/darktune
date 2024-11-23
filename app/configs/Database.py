from flask import Flask, current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from datetime import timedelta

Base = declarative_base()

class Database:
    
    @staticmethod
    def criar_conexao(app:Flask):
        app.config.from_pyfile(os.path.join("configs", "settings.py"))
        nome_banco_de_dados = app.config.get('BANCO_DE_DADOS')
        caminho_da_instance = os.path.join(app.instance_path, f"{nome_banco_de_dados}.sqlite3")
        os.makedirs(app.instance_path, exist_ok=True)
        
        DB_URI = f"sqlite:///{caminho_da_instance}"
        engine = create_engine(DB_URI)
        Session = sessionmaker(bind=engine)
        
        app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
        app.config['UPLOAD_IMAGES_FOLDER'] = "app/static/uploads/imagens"
        app.config['UPLOAD_AUDIOS_FOLDER'] = "app/static/uploads/audios"
        app.config['SESSSION_PERMANENT'] = True
        app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
        app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        app.session = Session()
        
        return engine
    
    def criar_tabelas():
        Base.metadata.create_all(bind=current_app.engine)