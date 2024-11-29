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
                return "Nenhum contato encontrado!"

            lista_meus_contatos = [contato.to_dict() for contato in meus_contatos]

            return lista_meus_contatos

        except Exception as erro:
            flash(str(erro))
            redirect()

    def todos_os_contatos(self):

        try:
            contatos = (
                app.session.query(ContatosModel, UsuariosModel.nome_usuario)
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
                return "Nenhum contato encontrado"

            lista_contatos = []
            for contato, nome_usuario in contatos:
                contato_dict = contato.to_dict()
                contato_dict["nome_usuario"] = nome_usuario
                lista_contatos.append(contato_dict)

            return lista_contatos

        except Exception as erro:
            flash(str(erro))
            redirect()

    def buscar_contatos(self):
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
            
            flash('Contato deletado')
            return redirect(url_for('paginas.contato'))

        except Exception as erro:
            app.session.rollback()
            raise erro
