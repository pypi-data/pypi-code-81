import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash

from hackattack_awa_matrix.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

def get_user(user_id):
    db = get_db()
    user = db.execute(
        'SELECT * FROM user WHERE id = ?', (user_id,)
    ).fetchone()
    return user

@bp.route('/register', methods=('GET', 'POST'))
@login_required
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.index'))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/index', methods=['GET'])
@login_required
def index():
    db = get_db()

    users = db.execute(
        'SELECT * FROM user'
    ).fetchall()

    return render_template('auth/index.html', users=users)


@bp.route('/delete', methods=['POST'])
@login_required
def delete():
    if 'deletion_object_id' not in request.form:
        current_app.logger.error("The requested user deletion returned an error because the parameter 'deletion_object_id' was not set in the request")
        error = "Die zu löschende ID wurde nicht gefunden."
        flash(error)
        return redirect(url_for('auth.index'))

    user_id = request.form['deletion_object_id']

    if user_id is None or user_id == "":
        current_app.logger.error("The requested user deletion returned an error because the parameter 'deletion_object_id' contained an invalid value: '" + str(user_id) + "'")
        error = "Die zu löschende ID wurde nicht gefunden."
        flash(error)
        return redirect(url_for('auth.index'))

    current_app.logger.info("User deletion requested for user with id: " + str(user_id))

    user = get_user(user_id)

    if user is None:
        current_app.logger.error(
            "The requested user with id '" + str(user_id) + "' was not found in the database")
        error = "Die zu löschende ID wurde nicht gefunden."
        flash(error)
        return redirect(url_for('auth.index'))

    current_app.logger.info("User was found and has the name '" + str(user['username']) + "'")
    current_app.logger.info("Deletion of User '" + str(user['username']) + "' starts now!")

    db = get_db()
    db.execute(
        'DELETE FROM user WHERE id = ?', (user['id'],))
    db.commit()

    return redirect(url_for('auth.index'))


@bp.route('/change_pw', methods=('GET', 'POST'))
@login_required
def change_pw():
    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        new_password2 = request.form['new_password2']
        db = get_db()
        error = None

        user = db.execute(
            'SELECT * FROM user WHERE id = ?', (session['user_id'],)
        ).fetchone()

        if not old_password:
            error = 'Old Password is required.'
        elif user is None:
            error = 'An internal error occured!'
        elif not check_password_hash(user['password'], old_password):
            error = 'Old Password is wrong!'
        elif not new_password:
            error = 'New Password is required.'
        elif not new_password2:
            error = 'New Password is required twice.'
        elif new_password != new_password2:
            error = 'The new passwords do not match!'

        if error is None:
            db.execute(
                'UPDATE user SET password = ?',
                (generate_password_hash(new_password), )
            )
            db.commit()
            return redirect(url_for('project.index'))

        flash(error)

    return render_template('auth/change_pw.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect credentials.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect credentials.'

        if error is None:
            #After Verify the validity of username and password
            session.permanent = True
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('index'))
