import os
from datetime import datetime

from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)
bootst = Bootstrap(APP)
moment = Moment(APP)
APP.config['SECRET_KEY'] = '9JNM%_D8uJF-1@knC,gOp$'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
APP.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(BASE_DIR, 'db','ant.sqlite3')
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB = SQLAlchemy(APP)

print("BaseDir = %r" % BASE_DIR)

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

