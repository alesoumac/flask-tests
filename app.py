from datetime import datetime

from flask import Flask, render_template, request, sessions
from flask_bootstrap import Bootstrap
from flask_moment import Moment

app = Flask(__name__)
bootst = Bootstrap(app)
moment = Moment(app)

def render_template_anette(html_file, page_title):
    user_agent = request.headers.get('User-Agent')
    return render_template(html_file, page_title=page_title,
        usuario="Alexandre", user_agent=user_agent,
        current_time=datetime.utcnow())

def render_form_anette(html_file, page_title):
    user_agent = request.headers.get('User-Agent')
    return render_template(html_file, page_title=page_title,
        usuario="Alexandre", user_agent=user_agent,
        current_time=datetime.utcnow(), form=form)

def render_error(error_number, error_message):
    return render_template("erro.html", page_title="Erro",
        error_number=str(error_number), error_message=error_message,
        current_time=datetime.utcnow()), error_number

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template_anette('index.html', page_title="Início")

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
