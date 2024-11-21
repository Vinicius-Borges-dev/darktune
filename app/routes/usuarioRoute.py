from flask import Blueprint, request, render_template, redirect, url_for, flash, session

usuario_bp = Blueprint('usuario_bp', __name__)

@usuario_bp.route('/login', methods=['POST'])
def login_usuario():
    pass

@usuario_bp.route('/logout')
def logout_usuario():
    pass

@usuario_bp.route('/cadastro', methods=['POST'])
def cadastro_usuario():
    pass

@usuario_bp.route('/perfil')
def perfil_usuario():
    pass

@usuario_bp.route('/perfil/editar', methods=['POST'])
def editar_perfil_usuario():
    pass

@usuario_bp.route('/perfil/excluir', methods=['POST'])
def excluir_perfil_usuario():
    pass