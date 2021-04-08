from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash
from .models import db, User, mail
from flask_login import LoginManager, logout_user, current_user, login_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, Form, BooleanField, validators
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from passlib.hash import pbkdf2_sha256
import jwt, os, json
from datetime import datetime, timedelta
from flask_mail import Message

# auth related routes

# forms and their validations
class LoginForm(FlaskForm):
    email = StringField('Email')
    password = PasswordField('Password')

class ResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(min=6, max=35)])
    email2 = StringField('Confirm Email', validators=[DataRequired(), Length(min=6, max=35), EqualTo('email')])

class ResetPasswordForm(FlaskForm):
    new_password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=200)])
    new_password2 = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8, max=200), EqualTo('new_password')])

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(min=6, max=35)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=200)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

login_manager = LoginManager()
# new application blueprint for routes
auth = Blueprint('auth', __name__, template_folder='templates')

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    # sign up page when receiving get request
    # creating user on DB when receiving post request
    if request.method == 'GET':
        form = RegistrationForm(request.form)
        if current_user and current_user.is_authenticated:
            return redirect(url_for('routes.index'))
        return render_template('signup.html', form=form)
    
    elif request.method == 'POST':
        # form validation
        form = RegistrationForm(request.form)
        if not form.validate_on_submit():
            print("Signup form errors:", form.errors.items())
            return render_template('signup.html', form=form)
        
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data, password=pbkdf2_sha256.hash(form.password.data))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))

def check_password(user_password, password):
    # check if passsord provided by user is the correct one
    return pbkdf2_sha256.verify(password, user_password)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'GET':
        if current_user and current_user.is_authenticated:
            return redirect(url_for('routes.index'))
        return render_template('login.html', form=form)
    else:
        if not form.validate_on_submit():
            print("Login form errors:", form.errors.items())
            return render_template('login.html', form=form)
        
        # Login and validate the user.
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not check_password(user.password, form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user)
        return redirect(url_for('routes.index'))

@auth.route('/reset', methods=['GET', 'POST'])
def reset():
    # user requested password reset route
    form = ResetForm(request.form)
    if request.method == 'GET':
        if current_user and current_user.is_authenticated:
            return redirect(url_for('routes.index'))
        return render_template('reset.html', form=form)
    else:
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            # showing user that email was sent, so no one can use this page to do user enumeration
            flash('Email with instructions to reset your password was sent!')
            return redirect(url_for('auth.reset'))
        # current date and time
        now = str(datetime.now())
        encoded_jwt = jwt.encode({"email": form.email.data, "datetime": now}, os.getenv('SECRET_KEY'), algorithm="HS256")

        # saving reset token on DB
        user.reset_token = encoded_jwt
        db.session.commit()

        msg = Message(
            subject="Password Reset Request", 
            sender="no-reply@kanban.com", 
            recipients=[form.email.data]
        )
        msg.html = render_template("reset_password_email.html", username=user.username, link=request.base_url+"/token/"+encoded_jwt)
        mail.send(msg)
        flash('Email with instructions to reset your password was sent!')
        return redirect(url_for('routes.index'))

@auth.route('/reset/token/<encoded_jwt>', methods=['GET', 'POST'])
def reset_token(encoded_jwt, methods=['GET', 'POST']):
    # user sent new password after requesting password reset
    form = ResetPasswordForm(request.form)
    try:
        # get token data
        user_data = jwt.decode(encoded_jwt, os.getenv('SECRET_KEY'), algorithms=["HS256"])
        user_email = user_data['email']
        user_datetime = user_data['datetime']
        # convert str to datetime
        user_datetime = datetime.strptime(user_datetime, '%Y-%m-%d %H:%M:%S.%f')

        # getting user DB data to check if the token is the same
        user = User.query.filter_by(email=user_email).first()
        # if it's not the same from the DB, the time expired, or we didn't found a user: we have an invalid token
        if user is None or user.reset_token != encoded_jwt or not user_datetime + timedelta(hours=1) > datetime.now():
            flash('Invalid token')
            return redirect(url_for('routes.index'))
    except Exception as e:
        print(e)
        # if there is any exception we return an invalid token as well.
        # if we return the same thing for different errors, attackers won't know why they are getting an error.
        flash('Invalid token')
        return redirect(url_for('routes.index'))
    
    if request.method == 'GET':
        # you can only access this page if you're logged out
        if current_user and current_user.is_authenticated:
            return redirect(url_for('routes.index'))
        return render_template('new_password.html', form=form)
    else:
        if not form.validate_on_submit():
            print("Form errors:", form.errors.items())
            return render_template('new_password.html', form=form)
        
        # updating password and cleaning DB token
        user.password = pbkdf2_sha256.hash(form.new_password.data)
        user.reset_token = ""
        db.session.commit()
        flash('Password updated!')
        return redirect(url_for('auth.login'))

@auth.route('/logout')
def logout():
    # logging user out
    logout_user()
    return redirect(url_for('routes.index'))
