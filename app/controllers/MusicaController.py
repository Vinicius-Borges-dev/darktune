from flask import current_app as app, request, redirect, flash, url_for
from app.models import MusicasModel, CantoresMusicasModel, CategoriasModel, MusicasCategoriasModel, UsuariosModel


class MusicaController:
    
    def criar_nova_musica():
        nome_musica = str(request.form.get("nome_musica"))
        cantor = str(request.form.get("cantor"))
        cantores = [cantor.strip() for cantor in cantor.split(",")]
        categoria = str(request.form.get("categoria"))
        categorias = [categoria.strip() for categoria in categoria.split(",")]
        imagem = request.files.get("imagem")
        musica = request.files.get("musica")

        if not nome_musica or not cantor or not categoria or not imagem or not musica:
            flash("Preencha todos os campos")
            return redirect(url_for("paginas.cadastro_musica"))

        try:
            categorias = (
                app.session.query(CategoriasModel)
                .join(MusicasCategoriasModel)
                
            )
            
                
                
        except Exception as error:
            app.session.rollback()
            flash(str(error))
            return redirect(url_for("paginas.cadastro_musica"))  

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
