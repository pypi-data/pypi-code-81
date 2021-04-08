from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash
from .models import Task, db
import json
from flask_login import LoginManager, logout_user, current_user, login_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, Form, BooleanField, validators, RadioField

# new application blueprint for routes
routes = Blueprint('routes', __name__, template_folder='templates')

class CreateTaskForm(FlaskForm):
    title = StringField('Title')
    description = StringField('description')
    status = RadioField('Status', choices=[('todo','todo'), ('doing', 'doing'),('done', 'done')])

# app routes
@routes.route('/')
def index():
    form = CreateTaskForm()
    if current_user and current_user.is_authenticated:
        todo_tasks = Task.query.filter_by(user_id=current_user.id, status="todo")
        doing_tasks = Task.query.filter_by(user_id=current_user.id, status="doing")
        done_tasks = Task.query.filter_by(user_id=current_user.id, status="done")

        return render_template('index.html', form=form, todo_tasks=todo_tasks, doing_tasks=doing_tasks, done_tasks=done_tasks)
    return render_template('home.html')

@routes.route('/create', methods=["GET", "POST"])
def create():
    try:
        # loading json to python dict and getting task data
        title = request.form.get('title')
        description = request.form.get('description')
        status = request.form.get('status')
        # creating task on DB
        db.session.add(Task(title=title, description=description, status=status, user_id=current_user.id))
        db.session.commit()
        return redirect(url_for('routes.index'))
    except Exception as e:
        print(e)
        flash('There was a problem creating your task, please try again.')
        return render_template('home.html')

"""
For every task we need to ensure that the user who created it is the one
that can change its status or delete it.
"""

@routes.route('/send_todo', methods=["GET", "POST"])
def send_todo():
    try:
        if current_user and current_user.is_authenticated:
            id = request.form.get('id')
            task = Task.query.filter_by(id=id, user_id=current_user.id).first()
            task.status = "todo"
            db.session.commit()
            return redirect(url_for('routes.index'))
        return render_template('home.html')
    except Exception as e:
        print(e)
        flash('There was a problem moving your task, please try again.')
        return render_template('home.html')

@routes.route('/send_doing', methods=["GET", "POST"])
def send_doing():
    try:
        if current_user and current_user.is_authenticated:
            id = request.form.get('id')
            task = Task.query.filter_by(id=id, user_id=current_user.id).first()
            task.status = "doing"
            db.session.commit()
            return redirect(url_for('routes.index'))
        return render_template('home.html')
    except Exception as e:
        print(e)
        flash('There was a problem moving your task, please try again.')
        return render_template('home.html')

@routes.route('/send_done', methods=["GET", "POST"])
def send_done():
    try:
        if current_user and current_user.is_authenticated:
            id = request.form.get('id')
            task = Task.query.filter_by(id=id, user_id=current_user.id).first()
            task.status = "done"
            db.session.commit()
            return redirect(url_for('routes.index'))
        return render_template('home.html')
    except Exception as e:
        print(e)
        flash('There was a problem moving your task, please try again.')
        return render_template('home.html')

@routes.route('/delete_task', methods=["GET", "POST"])
def delete_task():
    try:
        if current_user and current_user.is_authenticated:
            id = request.form.get('id')
            Task.query.filter_by(id=id, user_id=current_user.id).delete()
            db.session.commit()
            return redirect(url_for('routes.index'))
        return render_template('home.html')
    except Exception as e:
        print(e)
        flash('There was a problem moving your task, please try again.')
        return render_template('home.html')