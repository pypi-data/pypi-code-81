""" Initializing flask project """

__version__ = "0.1.0"

from flask import Flask
from .models import db, mail
from .routes import routes
from .auth import login_manager, auth
import os
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from .config import config

# protection against requests to our backend coming from things other than our website
csrf = CSRFProtect()

# initializing application
app = Flask(__name__)

# registering blueprints (extensions of our application - used for routes)
app.register_blueprint(routes)
app.register_blueprint(auth)

# updating configs based on FLASK_ENV specified
app.config.from_object(config[os.environ.get('FLASK_ENV')])

# initializing different services on our application
login_manager.init_app(app)
db.init_app(app)
csrf.init_app(app)
mail.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()