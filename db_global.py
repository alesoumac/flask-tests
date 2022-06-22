import os
from flask_sqlalchemy import SQLAlchemy

DB = None
BASE_DIR = ""

def initializeDatabase(app):
    global BASE_DIR
    global DB
    
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    print("BaseDir = %r" % BASE_DIR)
    app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(BASE_DIR, 'db','ant.sqlite3')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB = SQLAlchemy(app)
