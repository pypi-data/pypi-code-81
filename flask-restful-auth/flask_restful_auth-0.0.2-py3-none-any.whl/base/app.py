import os
from flask import Flask, jsonify, request, make_response
from functools import wraps
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('Secret')


class User:
    def __init__(self):
        self.store = 1

    def set_store(self, store):
        self.store = store

    def get_store(self):
        return self.store

    # creating fields for user information
    # email,#phone number(with county code) can be used as primary keys


@app.route('/')
def home():
    return 'This is the home page'


# creating decorator
# can be used for email auth
def token_existence(func):
    @wraps(func)
    def checking(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message':  'Missing token'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'token expired'}), 403
        return func(*args, **kwargs)
    return checking


def sign_up():
    pass
    # create new user
    # add to database
    # token can be formed uniquely


def encode_token():
    # get username
    # username is unique
    user = User.query.filter_by(name=username)  # code for sql database
    token = jwt.encode

    if not user:
        return make_response('Could not verify', 401)
    else:
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow() +
                datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})


if __name__ == '__main__':
    app.run(debug=True)
