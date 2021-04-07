from ._version import version_info, __version__

from jupyter_server.base.handlers import APIHandler
from tornado.log import app_log
from .integrations import setup_handlers

import json 


def _jupyter_server_extension_paths():
    return [{
        'module': 'jupyterlab_yq_kfidentity'
    }]


def load_jupyter_server_extension(nb_server_app):
    """
    Called when the extension is loaded.

    Args:
        nb_server_app (NotebookWebApplication): handle to the Notebook webserver instance.
    """
    web_app = nb_server_app.web_app
#     host_pattern = '.*$'
#     route_pattern = url_path_join(web_app.settings['base_url'], '/yqid/sync')
#     web_app.add_handlers(host_pattern, [(route_pattern, YqKfIdentity)])
    setup_handlers(web_app)