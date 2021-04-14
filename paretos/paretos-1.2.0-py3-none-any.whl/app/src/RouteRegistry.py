from dependency_injector.providers import Provider
from flask import Flask

from .CommandHandler.CommandHandler import CommandHandler
from .Container import Container
from .Routes.Index import Index


class RouteRegistry:
    def __init__(self, container: Container):
        self.__routes = {
            "/pithos/v1/projects/get": container.Projects_Get,
            "/pithos/v1/project_meta/get": container.Project_Meta_Get,
            "/pithos/v1/solutions/get": container.Solutions_Get,
            # Pass all other routes to dashboard to let react handle the routing
            "/<path:text>": Index.as_view(name="/catch"),
            "/": Index.as_view(name="/"),
        }

        self.__request_handler = container.RequestHandler()

    def register_routes(self, app: Flask):
        for route_key in self.__routes.keys():
            route = self.__routes[route_key]

            if isinstance(route, Provider):
                route = route()

            if isinstance(route, CommandHandler):
                view_function = self.__request_handler.get_view_function(route)
            else:
                view_function = route

            app.add_url_rule(route_key, view_func=view_function)
