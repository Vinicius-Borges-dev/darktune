from functools import wraps
from flask import request, redirect, session, flash

class UsuarioMiddleware:
    
    def verificar_login(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            usuario_logado = session['usuario']
            
            if not usuario_logado:
                flash("Sessão expirada")
                return redirect('/')
            
            return f(*args, **kwargs)
        return wrapper
    
    def verificar_permissao_admin(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not session['nivel']:
                flash("Você")