from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()

# ORM mapping

# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.String(200))
    status = db.Column(db.String(200))
    # foreign key, 1 user can have many tasks
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True)
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))
    reset_token = db.Column(db.String(200))
    task = db.relationship("Task")
