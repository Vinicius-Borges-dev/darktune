from flask import (
    current_app as app,
    request,
    redirect,
    url_for,
    render_template,
    flash,
    session,
)
from app.models import ContatosModel, ContatosUsuariosModel, UsuariosModel
from sqlalchemy import func, literal


class ContatoController:

    def criar_novo_contato(self):
        mensagem = request.form.get("mensagem")

        try:
            novo_contato = ContatosModel(mensagem=mensagem)

            app.session.add(novo_contato)
            app.session.commit()

            novo_contato_usuario = ContatosUsuariosModel(
                id_contato=novo_contato.id_contato, id_usuario=int(session["usuario"])
            )

            app.session.add(novo_contato_usuario)
            app.session.commit()

            flash("Contato criado com sucesso")
            return redirect(url_for("paginas.contato"))

        except Exception as erro:
            app.session.rollback()
            flash(str(erro))
            redirect(url_for("paginas.contato"))

    def meus_contatos(self, id: int):

        try:
            meus_contatos = (
                app.session.query(ContatosModel)
                .join(
                    ContatosUsuariosModel,
                    ContatosUsuariosModel.fk_id_contato == ContatosModel.id_contato,
                )
                .join(
                    UsuariosModel,
                    UsuariosModel.id_usuario == ContatosUsuariosModel.fk_id_usuario,
                )
                .filter(UsuariosModel.id_usuario == id)
                .all()
            )

            if not meus_contatos:
                erro = "Nenhum contato encontrado."
                return render_template("contato.html", erro=erro)

            lista_meus_contatos = [contato.to_dict() for contato in meus_contatos]

            return render_template("contato.html", meus_contatos=lista_meus_contatos)

        except Exception as erro:
            raise erro

    def todos_os_contatos(self):

        try:
            contatos = (
                app.session.query(
                    UsuariosModel.id_usuario,
                    UsuariosModel.nome,
                    ContatosModel.id_contato,
                    ContatosModel.mensagem,
                )
                .join(
                    ContatosUsuariosModel,
                    ContatosUsuariosModel.fk_id_contato == ContatosModel.id_contato,
                )
                .join(
                    UsuariosModel,
                    UsuariosModel.id_usuario == ContatosUsuariosModel.fk_id_usuario,
                )
                .all()
            )
            
            if not contatos:
                erro = "Nenhum contato encontrado."
                return render_template("contato.html", erro=erro)

            lista_contatos = []
            for id_usuario, nome_usuario, id_contato, mensagem in contatos:
                lista_contatos.append(
                    {
                        "id_usuario": id_usuario,
                        "nome_usuario": nome_usuario,
                        "id_contato": id_contato,
                        "mensagem": mensagem,
                    }
                )

            return render_template("contato.html", todos_os_contatos=lista_contatos)

        except Exception as erro:
            raise erro

    def buscar_contatos(self):
        if session.get("nivel") == "admin":
            return self.todos_os_contatos()
        else:
            return self.meus_contatos(session["usuario"])

    def atualizar_contato(self, id: int):
        mensagem = request.form.get("mensagem")

        try:
            meu_contato = (
                app.session.query(ContatosModel)
                .join(
                    ContatosUsuariosModel,
                    ContatosUsuariosModel.fk_id_contato == ContatosModel.id_contato,
                )
                .join(
                    UsuariosModel,
                    UsuariosModel.id_usuario == ContatosUsuariosModel.fk_id_usuario,
                )
                .filter(
                    UsuariosModel.id_usuario == session["usuario"],
                    ContatosModel.id_contato == id,
                )
                .first()
            )

            meu_contato.mensagem = mensagem

            app.session.commit()
            flash("Contato atualizado.")
            return redirect(url_for("paginas.contato"))

        except Exception as erro:
            flash(str(erro))
            redirect(url_for("paginas.contato"))

    def buscar_dados_de_contato(id: int):
        try:
            contato = (
                app.session.query(ContatosModel)
                .join(
                    ContatosUsuariosModel,
                    ContatosUsuariosModel.fk_id_contato == ContatosModel.id_contato,
                )
                .join(
                    UsuariosModel,
                    UsuariosModel.id_usuario == ContatosUsuariosModel.fk_id_usuario,
                )
                .filter(
                    UsuariosModel.id_usuario == session["usuario"],
                    ContatosModel.id_contato == id,
                )
                .first()
            )

            dados = contato.to_dict()

            return dados

        except Exception as erro:
            flash(str(erro))
            # return redirect(url_for("paginas.perfil"))

    def deletar_contato(self, id: int):

        try:
            contato = (
                app.session.query(ContatosModel)
                .join(
                    ContatosUsuariosModel,
                    ContatosUsuariosModel.fk_id_contato == ContatosModel.id_contato,
                )
                .filter(ContatosModel.id_contato == id)
                .first()
            )

            app.session.delete(contato)
            app.session.commit()

            flash("Contato deletado")
            return redirect(url_for("paginas.contato"))

        except Exception as erro:
            app.session.rollback()
            raise erro
