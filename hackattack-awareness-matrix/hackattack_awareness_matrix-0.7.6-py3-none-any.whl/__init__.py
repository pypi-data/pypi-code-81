import os
from datetime import timedelta

import werkzeug
from flask import Flask
from flask import render_template


def create_app(secret_key, database_storage_location=None, application_logger=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True, template_folder="templates")
    db_location = os.path.join(app.instance_path,
                               'awa_matrix.sqlite') if database_storage_location is None else database_storage_location
    print("Database file located at: " + str(db_location))
    print(
        "If you see an 'Internal Server Error' on the first start, make sure to delete the database file, it will be re-created automatically.")
    app.logger = application_logger
    app.config.from_mapping(
        SECRET_KEY=secret_key,
        DATABASE=db_location,
        PERMANENT_SESSION_LIFETIME=timedelta(hours=2)
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    if not os.path.exists(db_location):
        with app.app_context():
            db.init_db()

    from . import auth
    app.register_blueprint(auth.bp)
    from . import project
    app.register_blueprint(project.bp)
    from . import threat
    app.register_blueprint(threat.bp)
    from . import countermeasures
    app.register_blueprint(countermeasures.bp)
    from . import awarenessmeasures
    app.register_blueprint(awarenessmeasures.bp)
    from . import employee
    app.register_blueprint(employee.bp)

    # a simple page that says hello
    @app.route('/')
    def index():
        database = db.get_db()
        projects = database.execute(
            'SELECT id, name, description, start_date, end_date'
            ' FROM project'
        ).fetchall()
        return render_template('index.html', projects=projects)
    
    # a simple page that says hello
    @app.route('/license')
    def license():
        return render_template('license.html')

    @app.errorhandler(werkzeug.exceptions.BadRequest)
    def handle_bad_request(e):
        app.logger.error("Bad Request Error!")
        app.logger.error(e)
        return render_template("errors/400.html"), 400

    @app.errorhandler(werkzeug.exceptions.Unauthorized)
    def handle_unauthorized_request(e):
        app.logger.error("Unauthorized Error!")
        app.logger.error(e)
        return render_template("errors/401.html"), 401

    @app.errorhandler(werkzeug.exceptions.Forbidden)
    def handle_forbidden_request(e):
        app.logger.error("Forbidden Error!")
        app.logger.error(e)
        return render_template("errors/403.html"), 403

    @app.errorhandler(werkzeug.exceptions.NotFound)
    def handle_not_found_request(e):
        app.logger.error("Not Found Error!")
        app.logger.error(e)
        return render_template("errors/404.html"), 404

    @app.errorhandler(werkzeug.exceptions.InternalServerError)
    def handle_internal_server_error_request(e):
        app.logger.error("Internal Server Error!")
        original = getattr(e, "original_exception", None)

        if original is not None:
            app.logger.error(original)
        else:
            app.logger.error(e)

        return render_template("errors/500.html"), 500

    return app
