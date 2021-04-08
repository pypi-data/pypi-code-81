import os
import tempfile
from flask import url_for, request
import pytest
import unittest
from unittest import mock
from flask_login import LoginManager, logout_user, current_user, login_user
from web.models import User, Task

from web import app, db

"""Mocking endpoints for testing"""
def login(client, redirect, email, password):
    return client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=redirect)

def signup(client, username, email, password, password2):
    return client.post('/signup', data=dict(
        username=username,
        email=email,
        password=password,
        password2=password2
    ))

def create(client, title, description, status):
    return client.post('/create', data=dict(
        title=title,
        description=description,
        status=status,
    ), follow_redirects=True)

def send_todo(client, id):
    return client.post('/send_todo', data=dict(
        id=id,
    ), follow_redirects=True)

def send_doing(client, id):
    return client.post('/send_doing', data=dict(
        id=id,
    ), follow_redirects=True)

def send_done(client, id):
    return client.post('/send_done', data=dict(
        id=id,
    ), follow_redirects=True)

def delete_task(client, id):
    return client.post('/delete_task', data=dict(
        id=id,
    ), follow_redirects=True)

@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['FLASK_ENV'] = 'test'
    ctx = app.app_context()
    ctx.push()
    client = app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])

def test_homepage(client):
    """Homepage loads and the main words are there"""
    rv = client.get('/')
    assert b'Kanban Board' in rv.data

"""Following tests are testing login and creating a task."""
def test_can_login_and_create_todo(client):
    user1 = signup(client, 'username123', 'sample-09@todo.com', 'asdfasdf', 'asdfasdf')
    rv = login(client, True, 'sample-09@todo.com', 'asdfasdf')
    task_1 = create(client, 'title1', 'description1', 'todo')
    assert b'title1' in task_1.data

def test_can_login_and_create_doing(client):
    user1 = signup(client, 'username123', 'sample-09@todo.com', 'asdfasdf', 'asdfasdf')
    rv = login(client, True, 'sample-09@todo.com', 'asdfasdf')
    task_1 = create(client, 'title2', 'description1', 'doing')
    assert b'title1' in task_1.data

def test_can_login_and_create_done(client):
    user1 = signup(client, 'username123', 'sample-09@todo.com', 'asdfasdf', 'asdfasdf')
    rv = login(client, True, 'sample-09@todo.com', 'asdfasdf')
    task_1 = create(client, 'title-create', 'description1', 'done')
    assert b'title1' in task_1.data

"""Following tests are testing if it can create a task and change its status"""
def test_send_task_from_todo_to_done(client):
    user1 = signup(client, 'username1234', 'sample-10@todo.com', 'asdfasdf', 'asdfasdf')
    rv = login(client, True, 'sample-10@todo.com', 'asdfasdf')
    create(client, 'title-todo-1', 'description1', 'todo')
    # getting task and sending it to 'done' status
    user = User.query.filter_by(email='sample-10@todo.com',).first()
    task = Task.query.filter_by(user_id=user.id, title='title-todo-1').first()
    send_done(client, task.id)
    assert task.status == 'done'

def test_send_task_from_todo_to_doing(client):
    user1 = signup(client, 'username1234', 'sample-10@todo.com', 'asdfasdf', 'asdfasdf')
    rv = login(client, True, 'sample-10@todo.com', 'asdfasdf')
    create(client, 'title-todo-2', 'description2', 'todo')
    # getting task and sending it to 'doing' status
    user = User.query.filter_by(email='sample-10@todo.com',).first()
    task = Task.query.filter_by(user_id=user.id, title='title-todo-2').first()
    send_doing(client, task.id)
    assert task.status == 'doing'

def test_send_task_from_doing_to_todo(client):
    user1 = signup(client, 'username1234', 'sample-10@todo.com', 'asdfasdf', 'asdfasdf')
    rv = login(client, True, 'sample-10@todo.com', 'asdfasdf')
    create(client, 'title-doing-1', 'description1', 'doing')
    # getting task and sending it to 'todo' status
    user = User.query.filter_by(email='sample-10@todo.com',).first()
    task = Task.query.filter_by(user_id=user.id, title='title-doing-1').first()
    send_todo(client, task.id)
    assert task.status == 'todo'

def test_send_task_from_doing_to_done(client):
    user1 = signup(client, 'username1234', 'sample-10@todo.com', 'asdfasdf', 'asdfasdf')
    rv = login(client, True, 'sample-10@todo.com', 'asdfasdf')
    create(client, 'title-doing-2', 'description2', 'doing')
    # getting task and sending it to 'done' status
    user = User.query.filter_by(email='sample-10@todo.com',).first()
    task = Task.query.filter_by(user_id=user.id, title='title-doing-2').first()
    send_done(client, task.id)
    assert task.status == 'done'

def test_send_task_from_done_to_todo(client):
    user1 = signup(client, 'username1234', 'sample-10@todo.com', 'asdfasdf', 'asdfasdf')
    rv = login(client, True, 'sample-10@todo.com', 'asdfasdf')
    create(client, 'title-done-1', 'description1', 'done')
    # getting task and sending it to 'todo' status
    user = User.query.filter_by(email='sample-10@todo.com',).first()
    task = Task.query.filter_by(user_id=user.id, title='title-done-1').first()
    send_todo(client, task.id)
    assert task.status == 'todo'

def test_send_task_from_done_to_doing(client):
    user1 = signup(client, 'username1234', 'sample-10@todo.com', 'asdfasdf', 'asdfasdf')
    rv = login(client, True, 'sample-10@todo.com', 'asdfasdf')
    create(client, 'title-done-2', 'description2', 'done')
    # getting task and sending it to 'doing' status
    user = User.query.filter_by(email='sample-10@todo.com',).first()
    task = Task.query.filter_by(user_id=user.id, title='title-done-2').first()
    send_doing(client, task.id)
    assert task.status == 'doing'
    