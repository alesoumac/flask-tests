from datetime import datetime

from flask import flash, redirect, session, url_for

from db_global import (APP, DB, render_error, render_form_anette,
                       render_template_anette)
from hello import NameForm


@APP.route('/', methods=['GET', 'POST'])
def index():
    formName = NameForm()

    if formName.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != formName.name.data:
            flash('Looks like you have changed your name! ')
        session['name'] = formName.name.data
        session['age'] =  formName.age.data
        #session['birth_date'] = formName.birth_date.data
        return redirect(url_for('index'))

    return render_form_anette('index.html', page_title="Início",
        form       = formName,
        name       = session.get('name'),
        age        = session.get('age')
        #birth_date = session.get('birth_date')
        )

@APP.route('/estagiarios/')
def estagiarios():
    return render_template_anette("user.html", page_title="Estagiários")

@APP.route('/empresas/')
def empresas():
    return render_template_anette("user.html", page_title="Empresas")

#@app.route('/empresa/<username>')
#def greet(username):
#    return f"Hi, {username}"

@APP.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_error(404, 'Página não encontrada')

@APP.errorhandler(500)
def erro_interno_servidor(e):
    return render_error(500, 'Erro interno do servidor')

