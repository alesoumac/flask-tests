#from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request

app = Flask(__name__)
bootst = Bootstrap(app)
@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    usuario = 'Alexandre'
    return render_template('user.html', titulo_pagina="Início", usuario=usuario, user_agent=user_agent)

@app.route('/hi/')
def who():
    return "Who are You?"

@app.route('/hi/<username>')
def greet(username):
    return f"Hi, {username}"
