from flask import current_app as app, request, redirect, flash, url_for
from app.models import MusicasModel

class MusicaController:
    
    def criar_nova_musica():
        nome_musica = str(request.form.get("nome_musica"))
        cantor = str(request.form.get("cantor"))
        cantores = [cantor.strip() for cantor in cantor.split(",")]
        
    
    def capturar_todas_as_musicas():
        pass

    def capturar_musicas_aleatorias_para_exibicao():
        pass
    
    def capturar_musicas_por_nome():
        pass
    
    def capturar_musicas_por_cantor():
        pass
    
    def capturar_musicas_por_categoria():
        pass
    
    def atualizar_musica(id:int):
        pass
    
    def deletar_musica(id:int):
        pass
