import copy
import json
import os
import re

import requests
import tornado.gen as gen
from notebook.base.handlers import APIHandler
from notebook.utils import url_escape
from notebook.utils import url_path_join
from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPError
from tornado.httpclient import HTTPRequest
from tornado.httputil import url_concat
from tornado.web import RequestHandler
from traitlets import Bool
from traitlets import Unicode
from traitlets.config import SingletonConfigurable

link_regex = re.compile(r'<([^>]*)>;\s*rel="([\w]*)\"')


class GitHubConfig(SingletonConfigurable):

    """
    Allows configuration of access to the GitHub api.
    Modified to use SingletonConfigurable to work better with CC Labs.
    """

    allow_client_side_access_token = Bool(
        False,
        config=True,
        help=(
            "If True the access token specified in the JupyterLab settings "
            "will take precedence. If False the token specified in JupyterLab "
            "will be ignored. Storing your access token in the client can "
            "present a security risk so be careful if enabling this setting."
        ),
    )
    api_url = Unicode(
        "https://api.github.com", config=True, help="The url for the GitHub api"
    )
    access_token = Unicode("", config=True, help="A personal access token for GitHub.")
    validate_cert = Bool(
        True,
        config=True,
        help=(
            "Whether to validate the servers' SSL certificate on requests "
            "made to the GitHub api. In general this is a bad idea so only "
            "disable SSL validation if you know what you are doing!"
        ),
    )


class AuthHandler(RequestHandler):

    """
    Handles the GitHub OAuth callback (CC Labs specific).
    """

    @gen.coroutine
    def get(self, path=""):
        query = self.request.query_arguments
        params = {key: query[key][0].decode() for key in query}
        headers = {"Accept": "application/json"}
        data = {
            "client_id": os.environ.get("GITHUB_CLIENT_ID"),
            "client_secret": os.environ.get("GITHUB_CLIENT_SECRET"),
            "code": params["code"],
        }
        res = requests.post(
            "https://github.com/login/oauth/access_token", json=data, headers=headers
        )
        access_token = res.json()["access_token"]
        headers["Authorization"] = "token {}".format(access_token)

        res = requests.get("https://api.github.com/user", headers=headers)
        user = res.json()["login"]

        c = GitHubConfig.instance()
        c.access_token = access_token

        self.finish(
            "<script>window.opener.postMessage('{0}','*')</script>".format(user)
        )


class GetClientIDHandler(APIHandler):
    """
    Used to get the GitHub Oauth ClientID (CC Labs Specific).
    """

    @gen.coroutine
    def get(self, path=""):
        self.finish(json.dumps({"client_id": os.environ.get("GITHUB_CLIENT_ID")}))


class GistShareHandler(APIHandler):
    """
    Creates GitHub gists for a given file (CC Labs Specific).
    """

    @gen.coroutine
    def post(self, path=""):

        gist = {
            "description": "Created on Skills Network Labs",
            "public": True,
            "files": {},
        }
        print(json.loads(self.request.body))

        with open(
            "{}/{}".format(os.getcwd(), json.loads(self.request.body)["path"])
        ) as f:
            gist["files"][os.path.basename(f.name)] = {"content": f.read()}

        # Get access to the notebook config object
        c = GitHubConfig.instance()
        if not c.access_token:
            self.finish(json.dumps({"error": "unauthenticated"}))
        else:
            headers = {"Authorization": "token {}".format(c.access_token)}
            res = requests.post(
                "https://api.github.com/gists", json=gist, headers=headers
            )
            self.finish(json.dumps(res.json()))


def _jupyter_server_extension_points():
    return [{"module": "sn_jupyterlab_github"}]


def _load_jupyter_server_extension(nb_server_app):
    """
    Called when the extension is loaded.

    Args:
        nb_server_app (NotebookWebApplication): handle to the Notebook webserver instance.
    """
    web_app = nb_server_app.web_app
    base_url = web_app.settings["base_url"]
    endpoint = url_path_join(base_url, "github")
    handlers = [
        (url_path_join(endpoint, "auth") + "(.*)", AuthHandler),
        (url_path_join(endpoint, "client-id") + "(.*)", GetClientIDHandler),
        (url_path_join(endpoint, "share-gist") + "(.*)", GistShareHandler),
    ]
    web_app.add_handlers(".*$", handlers)


# backwards compatibility with jupyterlab 2.0
load_jupyter_server_extension = _load_jupyter_server_extension
_jupyter_server_extension_paths = _jupyter_server_extension_points
