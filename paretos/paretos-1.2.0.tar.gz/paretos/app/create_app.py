from flask import Flask
from flask_cors import CORS
from werkzeug.exceptions import InternalServerError

from .src.Container import Container
from .src.RouteRegistry import RouteRegistry


def create_app(data_source_name: str) -> Flask:
    container = Container()
    container.config.from_dict({"data_source_name": data_source_name})

    app = container.App()
    app.config["JSON_SORT_KEYS"] = False

    CORS(app, origins="*", supports_credentials=True)

    @app.before_request
    def before_request():
        container.Request_Id_Provider().update()

    @app.errorhandler(InternalServerError)
    def handle_error(exception: InternalServerError):
        error_handler = container.ErrorHandler()
        return error_handler.handle_error(exception)

    route_registry = RouteRegistry(container)
    route_registry.register_routes(app)

    return app
