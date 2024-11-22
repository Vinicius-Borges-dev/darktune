from flask import current_app as app, request, redirect, url_for, render_template, flash


class ContatoController:
    
    def criar_novo_contato():
        email = request.form.get("email")
        mensagem = request.form.get("mensagem")
        
        try:
            pass
        except Exception as erro:
            app.session.rollback()
            flash(str(erro))
            redirect()
    
    def meus_contatos(id:int):
        
        try:
            pass
        except Exception as erro:
            flash(str(erro))
            redirect()
    
    def todos_os_contatos():
        
        try:
            pass
        except Exception as erro:
            flash(str(erro))
            redirect()
    
    def atualizar_contato(id:int):
        mensagem = request.form.get("mensagem")
        
        try:
            pass
        except Exception as erro:
            flash(str(erro))
            redirect()
    
    def deletar_contato(id:int):
        
        try:
            pass
        except Exception as erro:
            flash(str(erro))
            redirect()