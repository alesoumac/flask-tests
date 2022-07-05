import os
from datetime import datetime
from re import S

from flask import Flask, render_template, request, session
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from requests import delete

SESSION_VAR_USUARIO      = 's_usuario'
SESSION_VAR_AVATAR       = 's_avatar'

TAMANHO_CAMPO_USUARIO    = 16
TAMANHO_CAMPO_EMAIL      = 80

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
APP = Flask(__name__)
BOOTSTRAP = Bootstrap(APP)
APP.config['SECRET_KEY'] = '9JNM%_D8uJF-1@knC,gOp$'
APP.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(BASE_DIR, 'db','vv.sqlite3')
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB = SQLAlchemy(APP)

#print("BaseDir = %r" % BASE_DIR)

def int_def(s, default=None):
    try:
        return int(s)
    except:
        return default

def namefy(nome):
    if ' ' not in nome:
        n = nome.lower()
        if n in ['de','da','do','das','dos','e']: return n
        p = n.split('\'')
        n = '\''.join([m.capitalize() for m in p])
        return n
    p = nome.split(' ')
    p = [namefy(n) for n in p if n != '']
    n = ' '.join(p)
    return n

def get_cookie(cookieName, default=None):
    if cookieName in session:
        return session[cookieName]
    else:
        return default

def delete_from_dic(dic,key):
    if key in dic:
        del(dic[key])

def delete_cookie(cookieName):
    delete_from_dic(session, cookieName)

def global_render_template(html_file, page_title, **pre_args):
    other_args = {}
    for arg in pre_args:
        other_args[arg] = pre_args[arg]
    user_agent = request.headers.get('User-Agent')
    if "s_usuario" not in other_args:
        other_args["s_usuario"] = get_cookie(SESSION_VAR_USUARIO)
    
    avatar = None
    num_avatar = None
    if 's_avatar' in other_args:
        num_avatar = int_def(other_args['s_avatar'])
    if num_avatar is None:
        num_avatar = int_def(get_cookie(SESSION_VAR_AVATAR))

    if num_avatar is not None:
        avatar = f"/static/avatar/{num_avatar:02d}.png"
        other_args['s_avatar'] = avatar
    else:
        delete_from_dic(other_args,'s_avatar')

    current_time = datetime.now()
    current_time_string = current_time.strftime('%d/%m/%Y')
    return render_template(html_file, page_title=page_title,
        user_agent=user_agent, current_time=current_time_string, **other_args)

def global_render_form_template(html_file, page_title, form, **form_fields):
    return global_render_template(html_file, page_title=page_title,
        form=form, **form_fields)

def global_render_error(error_number, error_message):
    return global_render_template("erro.html", page_title="Erro",
        error_number=str(error_number), error_message=error_message), error_number
