#from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request, sessions

app = Flask(__name__)
bootst = Bootstrap(app)

@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    usuario = 'Alexandre'
    return render_template('index.html', titulo_pagina="Início", usuario=usuario, user_agent=user_agent)

@app.route('/estagiario/')
def estagiarios():
    user_agent = request.headers.get('User-Agent')
    return render_template("user.html", titulo_pagina="Estagiários", usuario="Alexandre", user_agent=user_agent)

@app.route('/empresas/')
def empresas():
    user_agent = request.headers.get('User-Agent')
    return render_template("user.html", titulo_pagina="Empresas", usuario="empresas", user_agent=user_agent)

#@app.route('/empresa/<username>')
#def greet(username):
#    return f"Hi, {username}"

def render_error(error_number, error_message):
    return render_template("erro.html", titulo_pagina="Erro", error_number=str(error_number), error_message=error_message), error_number

@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_error(404, 'Página não encontrada')

@app.errorhandler(500)
def erro_interno_servidor(e):
    return render_error(500, 'Erro interno do servidor')