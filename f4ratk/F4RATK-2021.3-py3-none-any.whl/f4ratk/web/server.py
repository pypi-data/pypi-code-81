##############################################################################
# Copyright (C) 2020 - 2021 Tobias Röttger <dev@roettger-it.de>
#
# This file is part of F4RATK.
#
# F4RATK is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License version 3
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
##############################################################################

from click import group
from flask import Flask, jsonify
from flask.cli import FlaskGroup

# noinspection PyPackageRequirements
from werkzeug.exceptions import HTTPException, NotFound

from f4ratk.infrastructure import configure_logging, instantiate_dependencies
from f4ratk.ticker.api import NoTickerData
from f4ratk.web.infrastructure import server_cache


def create_app() -> Flask:
    configure_logging(verbose=False, server=True)
    instantiate_dependencies()

    app = Flask('f4ratk-server', static_folder=None)

    server_cache.init_app(app)

    @app.errorhandler(HTTPException)
    def error_500(exception: HTTPException):
        return (
            jsonify({"error": exception.description}),
            exception.code,
            {'Content-Type': 'application/json'},
        )

    @app.errorhandler(NoTickerData)
    def error_symbol_unknown(exception: NoTickerData):
        return (
            jsonify({"error": str(exception)}),
            NotFound.code,
            {'Content-Type': 'application/json'},
        )

    with app.app_context():
        # noinspection PyUnresolvedReferences
        from f4ratk.web import controller  # noqa: F401

    return app


@group(cls=FlaskGroup, create_app=create_app)
def server_main():
    pass
