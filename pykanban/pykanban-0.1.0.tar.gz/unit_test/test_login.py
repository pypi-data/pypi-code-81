import os
import tempfile
from flask import url_for, request
import pytest

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

def logout(client):
    return client.get('/logout', follow_redirects=True)

@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['FLASK_ENV'] = 'test'
    client = app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])

def test_cant_login_with_invalid_user(client):
    """Testing login with invalid credentials"""
    rv = login(client, True, 'asdf', 'asdfasdfsd')
    assert (b'Invalid username or password' in rv.data)

def test_login_with_invalid_password(client):
    """Testing login with valid user but invalid password"""
    user1 = signup(client, 'username', 'sample-1@todo.com', 'asdfasdf', 'asdfasdf')
    rv = login(client, True, 'username', 'asdfasdf1')
    assert (b'Invalid username or password' in rv.data)

def test_login_with_valid_user(client):
    """Testing with valid user data"""
    user1 = signup(client, 'username', 'sample-1@todo.com', 'asdfasdf', 'asdfasdf')
    rv = login(client, True, 'sample-1@todo.com', 'asdfasdf')
    # if we created the account and logged in we should receive a redirect (302)
    assert (b'Create New Task' in rv.data and b'Todo' in rv.data and b'Doing' in rv.data and b'Done' in rv.data)

def test_login_logout(client):
    """Testing with valid user data"""
    user1 = signup(client, 'username', 'sample-1@todo.com', 'asdfasdf', 'asdfasdf')
    login_ = login(client, True, 'username', 'asdfasdf')
    logout_ = logout(client)
    # if we created the account, logged in, and logged out we should go back to the original page
    assert b'Login to create and manage your Kanban Board.' in logout_.data