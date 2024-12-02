from flask import Blueprint, render_template, session, redirect, url_for
from app.controllers.MusicaController import MusicaController
from app.controllers.ContatoController import ContatoController
from app.middlewares.UsuarioMiddleware import UsuarioMiddleware
from app.controllers.UsuarioController import UsuarioController
from app.controllers.CurtidaController import CurtidaController

paginas_bp = Blueprint("paginas", __name__)


@paginas_bp.route("/home")
def home():
    musicas = MusicaController().capturar_musicas_aleatorias_para_exibicao()
    return render_template("index.html", musicas=musicas)


@paginas_bp.route("/contato")
@UsuarioMiddleware.verificar_login
def contato():
    return ContatoController().buscar_contatos()


@paginas_bp.route("/musicas")
def musicas():
    musicas = MusicaController().capturar_todas_as_musicas()
    return render_template("musicas.html", musicas=musicas)


@paginas_bp.route("/musica/<int:id>")
def musica(id):
    musica = MusicaController().buscar_dados_da_musica(id)
    if musica == "Nenhuma música encontrada.":
        return redirect(url_for("paginas.musicas"))
    return render_template("player.html", musica=musica)


@paginas_bp.route("/conta")
@UsuarioMiddleware.verificar_login
def conta():
    dados_usuario = UsuarioController().capturar_dados_do_usuario()

    curtidas = CurtidaController().buscar_minhas_curtidas()

    if session.get("nivel") != "admin":
        return render_template("conta.html", dados=dados_usuario, curtidas=curtidas)
    else:
        musicas_adicionadas = MusicaController().capturar_todas_as_musicas()

        if not musicas_adicionadas[1]:
            return render_template(
                "conta.html",
                dados=dados_usuario,
                curtidas=curtidas,
                erro=musicas_adicionadas,
            )

        return render_template(
            "conta.html",
            dados=dados_usuario,
            curtidas=curtidas,
            musicas_adicionadas=musicas_adicionadas,
        )


@paginas_bp.route("/cadastro/musica")
@UsuarioMiddleware.verificar_login
def cadastro_musica():
    return render_template("cadastro_de_musicas.html")
