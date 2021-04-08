# Example taken from:
# http://flask.pocoo.org/docs/1.0/testing/
# and suitably modified.
import os
import tempfile

import pytest

from web import app, db

def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def signup(client, username, email, password, password2):
    return client.post('/signup', data=dict(
        username=username,
        email=email,
        password=password,
        password2=password2
    ), follow_redirects=True)

@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['FLASK_ENV'] = 'test'
    client = app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])

def test_can_signup(client):
    """Testing sign up with valid data"""
    user1 = signup(client, 'username0', 'sample-0@todo.com', 'asdfasdf', 'asdfasdf')
    # if it succesfully signs up there is a redirect (status code 302)
    assert b'Login' in user1.data

def test_wrong_email_and_password(client):
    """Testing with wrong email and short password"""
    rv = signup(client, 'asdf', 'asdf', 'asdf', 'asdf')
    assert (b'Invalid email address.' in rv.data and b'Field must be between 8 and 200 characters long.' in rv.data)

def test_wrong_password(client):
    """Testing sign up with short password"""
    rv = signup(client, 'asdf', 'lucca@gmail.com', 'asdf', 'asdf')
    assert (b'Field must be between 8 and 200 characters long.' in rv.data)

def test_wrong_email(client):
    """Testing sign up with invalid email"""
    rv = signup(client, 'asdf', 'lsdjfl- asdf', 'asdfasdfsdf', 'asdfasdfsdf')
    assert (b'Invalid email address.' in rv.data)

def test_wrong_password_confirmation(client):
    """Testing sign up with wrong set of passwords"""
    rv = signup(client, 'asdf', 'lsdjfl- asdf', 'asdfasdf', 'asdfasdf1')
    assert (b'Field must be equal to password.' in rv.data)

def test_cant_create_user_with_same_username(client):
    """Testing sign up with used username"""
    user1 = signup(client, 'username', 'sample-1@todo.com', 'asdfasdf', 'asdfasdf')
    user2 = signup(client, 'username', 'sample-2@todo.com', 'asdfasdf', 'asdfasdf')
    assert (b'Please use a different username.' in user2.data)

def test_cant_create_user_with_same_email(client):
    """Testing sign up with used email"""
    user1 = signup(client, 'username', 'sample-1@todo.com', 'asdfasdf', 'asdfasdf')
    user2 = signup(client, 'username-2', 'sample-1@todo.com', 'asdfasdf', 'asdfasdf')
    assert (b'Please use a different email address.' in user2.data)