from datetime import datetime
from random import randint
from flask import flash, redirect, session, url_for

from config import (APP, DB, BASE_DIR, global_render_template, global_render_form_template, global_render_error)

@APP.route('/')
def index():
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
        usuario="Alexandre",
        avatar=randint(1,40)
        #birth_date = session.get('birth_date')
        )

# @APP.route('/estagiarios/')
# def estagiarios():
#     return render_template_anette("user.html", page_title="Estagiários")

# @APP.route('/empresas/')
# def empresas():
#     return render_template_anette("user.html", page_title="Empresas")

# #@app.route('/empresa/<username>')
# #def greet(username):
# #    return f"Hi, {username}"

@APP.errorhandler(404)
def pagina_nao_encontrada(e):
    return global_render_error(404, 'Página não encontrada')

@APP.errorhandler(500)
def erro_interno_servidor(e):
    return global_render_error(500, 'Erro interno do servidor')

