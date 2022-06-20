import os
from datetime import datetime

from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from hello import NameForm

app = Flask(__name__)
bootst = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = '9JNM%_D8uJF-1@knC,gOp$'

basedir = os.path.abspath(os.path.dirname(__file__))
print("BaseDir = %r" % basedir)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'db','ant.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

def render_template_anette(html_file, page_title, **other_args):
    user_agent = request.headers.get('User-Agent')
    return render_template(html_file, page_title=page_title,
        usuario="Alexandre", user_agent=user_agent,
        current_time=datetime.utcnow(), **other_args)

def render_form_anette(html_file, page_title, form, **form_fields):
    return render_template_anette(html_file, page_title=page_title,
        form=form, **form_fields)

def render_error(error_number, error_message):
    return render_template("erro.html", page_title="Erro",
        error_number=str(error_number), error_message=error_message,
        current_time=datetime.utcnow()), error_number

@app.route('/', methods=['GET', 'POST'])
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

@app.route('/estagiarios/')
def estagiarios():
    return render_template_anette("user.html", page_title="Estagiários")

@app.route('/empresas/')
def empresas():
    return render_template_anette("user.html", page_title="Empresas")

#@app.route('/empresa/<username>')
#def greet(username):
#    return f"Hi, {username}"

@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_error(404, 'Página não encontrada')

@app.errorhandler(500)
def erro_interno_servidor(e):
    return render_error(500, 'Erro interno do servidor')
