import os

def write_requirements():
    with open("requirements.txt", "w") as f:
        reqs_text = '''\
alembic
astroid
bcrypt
blinker
cffi
click
colorama
dnspython
email-validator
Flask
Flask-Bcrypt
Flask-Login
Flask-Mail
Flask-Migrate
Flask-SQLAlchemy
Flask-WTF
idna
isort
itsdangerous
Jinja2
lazy-object-proxy
Mako
MarkupSafe
mccabe
Pillow
pycparser
pylint
python-dateutil
python-editor
six
SQLAlchemy
toml
Werkzeug
wrapt
WTForms
wheel
'''
        f.write(reqs_text)


def create_gitignore():
    with open('.gitignore', 'w') as f:
        ignore_text = """\
venv
**/__pycache__
site.db
migrations/versions/**/*
config.py
"""
        f.write(ignore_text)

def create_app_py(name):
    def wrapper():
        with open('app.py','w') as f:
            app_py_text = f"""\
from {name} import app

if __name__=='__main__':
    app.run(debug=True)            
"""
            f.write(app_py_text)
    return wrapper

def create_config_py():
    with open('config.py', 'w') as f:
        config_py_text = f"""\
class Config:
    SECRET_KEY = {os.urandom(16)}
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../site.db'
    DEBUG = True
    DEVELOPMENT = True
"""
        f.write(config_py_text)

def create_init_py(name):
    def wrapper():
        with open(os.path.join(name, '__init__.py'), 'w') as f:
            init_py_text = """\
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app=Flask(__name__)

app.config.from_object(Config)

db=SQLAlchemy(app)

migrate=Migrate(app, db)
""" 
            f.write(init_py_text)
    return wrapper

def create_static_folders(name):
    def wrapper():
        os.mkdir(os.path.join(name, 'static'))
        os.mkdir(os.path.join(name, 'static', 'js'))
        os.mkdir(os.path.join(name, 'static', 'css'))
        os.mkdir(os.path.join(name, 'static', 'images'))
    return wrapper