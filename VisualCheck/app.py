import os
from datetime import datetime
from random import randint

import pandas as pd
from flask import flash, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash

from config import (APP, BASE_DIR, DB, SESSION_VAR_AVATAR, SESSION_VAR_USUARIO,
                    delete_cookie, get_cookie, global_render_error,
                    global_render_form_template, global_render_template,
                    namefy, route_decode, route_encode)
from forms.form_login import LoginForm
from forms.form_usuario import UsuarioForm

DF = pd.read_csv(os.path.join(BASE_DIR,'db','vv_users.csv'))

def save_dataframe():
    global DF
    global BASE_DIR
    DF.to_csv(os.path.join(BASE_DIR,'db','vv_users.csv'), index=False, encoding='utf-8')

def verifica_acesso(url):
    s_usuario = get_cookie(SESSION_VAR_USUARIO)
    if s_usuario is None:
        return f'/entrando/{route_encode(url)}'
    return None
    
@APP.route('/')
def index():
    s_usuario = get_cookie(SESSION_VAR_USUARIO)
    s_avatar  = get_cookie(SESSION_VAR_AVATAR)
    locdf = DF.loc[DF['usuario'] == s_usuario]
    if len(locdf) > 0:
        s_nome = locdf['nome'].iloc[0]
    else:
        s_nome = None
    print("Sessao = ", session)

    return global_render_template('index.html', page_title="Início",
        s_usuario=s_usuario,
        s_avatar=s_avatar,
        s_nome=s_nome
        )

@APP.route('/entrando', methods=['GET', 'POST'])
def entrando():
    global DF
    loginForm = LoginForm()
    if loginForm.validate_on_submit():
        dicForm = loginForm.fields_as_dict(True)
        dicForm['usuario'] = dicForm['usuario'].lower()
        umUsuario = dicForm['usuario']
        locdf = DF.loc[DF['usuario'] == umUsuario]
        if len(locdf) > 0:
            pwhash = locdf['senha'].iloc[0]
            if check_password_hash(pwhash, dicForm['senha']):
                session[SESSION_VAR_USUARIO] = umUsuario
                session[SESSION_VAR_AVATAR] = int(locdf['avatar'].iloc[0])
                return redirect('/')
        flash(f"Usuário ou senha inválidos")

    return global_render_form_template('login.html', 
        page_title='Acesso',
        form=loginForm,
        **loginForm.fields_as_dict()
        )

@APP.route('/entrando/<new_route>', methods=['GET', 'POST'])
def entrando_com_rota(new_route):
    global DF
    nova_rota = route_decode(new_route)
    print(f'Vai tentar redirecionar para "{nova_rota}"')
    loginForm = LoginForm()
    if loginForm.validate_on_submit():
        dicForm = loginForm.fields_as_dict(True)
        dicForm['usuario'] = dicForm['usuario'].lower()
        umUsuario = dicForm['usuario']
        locdf = DF.loc[DF['usuario'] == umUsuario]
        if len(locdf) > 0:
            pwhash = locdf['senha'].iloc[0]
            if check_password_hash(pwhash, dicForm['senha']):
                session[SESSION_VAR_USUARIO] = umUsuario
                session[SESSION_VAR_AVATAR] = int(locdf['avatar'].iloc[0])
                return redirect(nova_rota)
        flash(f"Usuário ou senha inválidos")

    return global_render_form_template('login.html', 
        page_title='Acesso',
        form=loginForm,
        **loginForm.fields_as_dict()
        )

@APP.route('/saindo')
def saindo():
    delete_cookie(SESSION_VAR_USUARIO)
    delete_cookie(SESSION_VAR_AVATAR)
    return redirect('/')

@APP.route('/usuario/<username>')
def show_user(username):
    return global_render_template('index.html', page_title=f"{username}",
        s_usuario=username,
        s_avatar=randint(1,40)
        )

@APP.route('/cadastro/usuario', methods=['GET', 'POST'])
def cadastro_usuario():
    global DF
    redirectURL = verifica_acesso('/cadastro/usuario')
    if redirectURL:
        return redirect(redirectURL)

    usuarioForm = UsuarioForm()
    if usuarioForm.validate_on_submit():
        dicForm = usuarioForm.fields_as_dict(True)
        dicForm['usuario'] = dicForm['usuario'].lower()
        dicForm['nome'] = namefy(dicForm['nome'])
        umUsuario = dicForm['usuario']
        locdf = DF.loc[DF['usuario'] == umUsuario]
        dicNewDF = {}
        listdf = []
        for campo in DF:
            if campo == 'senha' and campo in dicForm:
                senh = dicForm[campo]
                if len(senh) < 100:
                    dicForm[campo] = generate_password_hash(senh,salt_length=32)
            valor = dicForm[campo] if campo in dicForm else None
            dicNewDF[campo] = [valor]
            listdf += [valor]

        if len(locdf) > 0:
            DF.loc[DF['usuario'] == umUsuario] = listdf
            flash(f"Usuário '{umUsuario}' já cadastrado")
        else:
            DF = DF.append(pd.DataFrame(dicNewDF), ignore_index=True)
            flash(f"Usuário '{umUsuario}' adicionado")
            usuarioForm.clear_fields()

        save_dataframe()
        print(DF)

        return redirect('/cadastro/usuario')

    return global_render_form_template('quickform.html', 
        page_title='Cadastro de Usuário',
        form=usuarioForm,
        **usuarioForm.fields_as_dict()
        )

    # formName = NameForm()

    # if formName.validate_on_submit():
    #     old_name = session.get('name')
    #     if old_name is not None and old_name != formName.name.data:
    #         flash('Looks like you have changed your name! ')
    #     session['name'] = formName.name.data
    #     session['age'] =  formName.age.data
    #     #session['birth_date'] = formName.birth_date.data
    #     return redirect(url_for('index'))

@APP.errorhandler(404)
def pagina_nao_encontrada(e):
    return global_render_error(404, 'Página não encontrada')

@APP.errorhandler(500)
def erro_interno_servidor(e):
    return global_render_error(500, 'Erro interno do servidor')

