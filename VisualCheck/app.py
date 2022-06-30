from datetime import datetime
from random import randint

from flask import flash, redirect, session, url_for

from config import (APP, BASE_DIR, DB, SESSION_VAR_AVATAR, SESSION_VAR_USUARIO,
                    global_render_error, global_render_form_template,
                    global_render_template)


@APP.route('/')
def index():
    usuario = session[SESSION_VAR_USUARIO] \
              if SESSION_VAR_USUARIO in session else \
              None
    avatar  = session[SESSION_VAR_AVATAR] \
              if 's_avatar' in session else \
              None
    print("Sessao = ", session)
    # formName = NameForm()

    # if formName.validate_on_submit():
    #     old_name = session.get('name')
    #     if old_name is not None and old_name != formName.name.data:
    #         flash('Looks like you have changed your name! ')
    #     session['name'] = formName.name.data
    #     session['age'] =  formName.age.data
    #     #session['birth_date'] = formName.birth_date.data
    #     return redirect(url_for('index'))

    return global_render_template('index.html', page_title="Início",
        usuario=usuario,
        avatar=avatar,
        )

@APP.route('/entrando')
def entrando():
    usuarios=['Alexandre','Jussara','Leticia','Hugo']
    usuario_id = randint(0,len(usuarios)-1)
    usuario = usuarios[usuario_id]
    avatar = randint(1, 40)
    session[SESSION_VAR_USUARIO] = usuario
    session[SESSION_VAR_AVATAR] = avatar
    return redirect('/')

@APP.route('/saindo')
def saindo():
    del(session[SESSION_VAR_USUARIO])
    del(session[SESSION_VAR_AVATAR])
    return redirect('/')

@APP.route('/usuario/<username>')
def show_user(username):
    return global_render_template('index.html', page_title=f"{username}",
        usuario=username,
        avatar=randint(1,40)
        )

@APP.route('/cadastro/usuario')
def cadastro_usuario():
    usuarioForm = UsuarioForm()
    return global_render_form_template('quickform.html', 'Cadastro de Usuário',)
@APP.errorhandler(404)
def pagina_nao_encontrada(e):
    return global_render_error(404, 'Página não encontrada')

@APP.errorhandler(500)
def erro_interno_servidor(e):
    return global_render_error(500, 'Erro interno do servidor')

