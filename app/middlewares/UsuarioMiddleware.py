from functools import wraps
from flask import request, redirect, session, flash

class UsuarioMiddleware:
    
    def verificar_login(f): 
        @wraps(f) 
        def wrapper(*args, **kwargs): 
            usuario = session.get('usuario') 
            print(usuario) 
            if not usuario: 
                flash("Sessão expirada") 
                return redirect('/') 
            return f(*args, **kwargs) 
        return wrapper
    
    def verificar_permissao_admin(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            nivel = session.get('nivel')
            if nivel != 'admin':
                flash("Permissão negada")
                return redirect('/')
            return f(*args, **kwargs)
        return wrapper