# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

"""
A wsgi application that provides a browser based user interface, similar to a desktop file manager.

See :py:class:`FmApp`.
"""

import base64
import hashlib
import html
import io
import json
import mimetypes
import os
import random
import stat
import string
import threading
import time
import typing as t
import zipfile

import werkzeug.exceptions
import werkzeug.routing
import werkzeug.wsgi

import lawwenda.comm
import lawwenda.fs.factory
import lawwenda.search
import lawwenda.sharehttpapp


# pylint: disable=no-self-use,unused-argument
class FmApp:
    """
    A wsgi application that provides a browser based user interface, similar to a desktop file manager.
    """

    URL_INTERNALS_NAME = ".~__lawwenda__int~"

    def __init__(self, share: "lawwenda.Share"):
        """
        :param share: The share to provide by this application.
        """
        self.__mydir = os.path.dirname(__file__)
        self.__share = share
        self.__filesystem = lawwenda.fs.factory.create_filesystem(
            share.path, readonly=share.readonly,
            hide_by_patterns=share.hide_by_patterns, hide_by_tags=share.hide_by_tags,
            include_by_patterns=share.include_by_patterns, include_by_tags=share.include_by_tags,
            exclude_by_patterns=share.exclude_by_patterns, exclude_by_tags=share.exclude_by_tags,
            exclude_hidden=share.exclude_hidden)
        self.__sharehttpapp = lawwenda.sharehttpapp.ShareHttpApp(self.__filesystem)
        self.__authcache = {}
        self.__authlock = threading.Lock()
        self.__url_map = werkzeug.routing.Map([
            werkzeug.routing.Rule("/help", endpoint="help", methods=["GET"]),
            werkzeug.routing.Rule("/static/<path:filepath>", endpoint="static", methods=["GET"]),
            werkzeug.routing.Rule("/api/copy/", endpoint="api_copy", methods=["POST"]),
            werkzeug.routing.Rule("/api/delete/", endpoint="api_delete", methods=["POST"]),
            werkzeug.routing.Rule("/api/details/", endpoint="api_details", methods=["GET"]),
            werkzeug.routing.Rule("/api/dir/", endpoint="api_dir", methods=["GET"]),
            werkzeug.routing.Rule("/api/known_tags/", endpoint="api_known_tags", methods=["GET"]),
            werkzeug.routing.Rule("/api/mkdir/", endpoint="api_mkdir", methods=["POST"]),
            werkzeug.routing.Rule("/api/move/", endpoint="api_move", methods=["POST"]),
            werkzeug.routing.Rule("/api/rename/", endpoint="api_rename", methods=["POST"]),
            werkzeug.routing.Rule("/api/set_comment/", endpoint="api_set_comment", methods=["POST"]),
            werkzeug.routing.Rule("/api/set_geo/", endpoint="api_set_geo", methods=["POST"]),
            werkzeug.routing.Rule("/api/set_rating/", endpoint="api_set_rating", methods=["POST"]),
            werkzeug.routing.Rule("/api/tag_entries/", endpoint="api_tag_entries", methods=["POST"]),
            werkzeug.routing.Rule("/api/thumbnail/", endpoint="api_thumbnail", methods=["GET"]),
            werkzeug.routing.Rule("/api/untag_entries/", endpoint="api_untag_entries", methods=["POST"]),
            werkzeug.routing.Rule("/api/upload/", endpoint="api_upload", methods=["POST"]),
            werkzeug.routing.Rule("/api/zip/", endpoint="api_zip", methods=["POST"]),
            werkzeug.routing.Rule("/api/zip_download/<zipid>/stuff.zip", endpoint="api_zip_download", methods=["GET"]),
        ])

    @property
    def filesystem(self) -> lawwenda.fs.Filesystem:
        """
        The filesystem used by this FmApp.
        """
        return self.__filesystem

    def _on_api_dir(self, request):
        path = request.args["path"]
        configdict = json.loads(request.args["config"])
        hidden_files_visible = configdict.get("hiddenFilesVisible", False)
        search_config = configdict.get("searchConfig")
        sort_column = configdict.get("sortColumn")
        if sort_column not in ["name", "size", "mtime"]:
            sort_column = "name"
        sort_descending = configdict.get("sortDescending", False)
        search = lawwenda.search.create_search(**json.loads(search_config)) if search_config else None
        pathnode = self.__filesystem.node_by_path(path)
        if search:
            nodes = list(search.query(pathnode))
        else:
            nodes = pathnode.child_nodes
        if not hidden_files_visible:
            nodes = [n for n in nodes if not n.is_hidden]
        nodes.sort(key=lambda n: (getattr(n, sort_column), n.name), reverse=sort_descending)
        nodes.sort(key=lambda n: 0 if n.is_dir else 1)
        result = [n.basics_as_dict for n in nodes]
        return lawwenda.comm.JsonedResponse(result)

    def _on_api_details(self, request):
        entry = self.__filesystem.node_by_path(request.args["path"])
        return lawwenda.comm.JsonedResponse(entry.full_as_dict)

    def _on_api_delete(self, request):
        for path in request.json["paths"]:
            self.__filesystem.node_by_path(path).delete()

    def _on_api_mkdir(self, request):
        self.__filesystem.node_by_path(request.json["path"]).mkdir()

    def _on_api_copy(self, request):
        return self.__on_api_copymove(request, "copy")

    def _on_api_move(self, request):
        return self.__on_api_copymove(request, "move")

    def _on_api_rename(self, request):
        path = request.json["path"]
        self.__filesystem.node_by_path(path).move_to(f"{path}/../{request.json['newname']}")

    def _on_api_set_comment(self, request):
        comment = request.json["comment"]
        for path in request.json["paths"]:
            self.__filesystem.node_by_path(path).set_comment(comment)

    def _on_api_set_geo(self, request):
        geo = request.json["geo"]
        for path in request.json["paths"]:
            self.__filesystem.node_by_path(path).set_geo(geo)

    def _on_api_set_rating(self, request):
        rating = request.json["rating"]
        for path in request.json["paths"]:
            self.__filesystem.node_by_path(path).set_rating(rating)

    def _on_api_thumbnail(self, request):
        filepath = request.args["path"]
        entry = self.__filesystem.node_by_path(filepath)
        return werkzeug.wrappers.Response(entry.thumbnail(), mimetype="image/png")

    def _on_api_upload(self, request):
        destpathentry = self.__filesystem.node_by_path(request.form["destpath"])
        for uploadfile in request.files.getlist("upload"):
            destpathentry.child_by_name(uploadfile.filename).write_file(uploadfile)

    def _on_api_known_tags(self, _):
        return lawwenda.comm.JsonedResponse(self.__filesystem.known_tags())

    def _on_api_tag_entries(self, request):
        tag = request.json["tag"]
        for path in request.json["paths"]:
            self.__filesystem.node_by_path(path).add_tag(tag)

    def _on_api_untag_entries(self, request):
        tag = request.json["tag"]
        for path in request.json["paths"]:
            self.__filesystem.node_by_path(path).remove_tag(tag)

    def _on_api_zip(self, request):
        zipid = _TempZips.create_tempzip(self, [self.__filesystem.node_by_path(path) for path in request.json["paths"]])
        return lawwenda.comm.JsonedResponse({"url": f"{self.URL_INTERNALS_NAME}/api/zip_download/{zipid}/stuff.zip"})

    def _on_api_zip_download(self, request, zipid):
        time.sleep(0.1)  # security; so guessing zipids is harder
        btempzip = _TempZips.get_tempzip(self, zipid)
        if btempzip is None:
            return werkzeug.exceptions.NotFound()
        return werkzeug.wrappers.Response(btempzip, mimetype="application/zip")

    def __on_api_copymove(self, request, action):
        destpath = request.json["destpath"]
        for srcpath in request.json["srcpaths"]:
            fsnode = self.__filesystem.node_by_path(srcpath)
            {"copy": fsnode.copy_to, "move": fsnode.move_to}[action](f"{destpath}/{fsnode.name}")

    def _on_static(self, _, filepath):
        fpath = os.path.abspath(f"{self.__mydir}/static/{filepath}")
        if not (f"{fpath}/".startswith(f"{self.__mydir}/") and os.path.exists(fpath)):
            return werkzeug.exceptions.NotFound()
        with open(fpath, "rb") as f:
            return werkzeug.wrappers.Response(f.read(), mimetype=mimetypes.guess_type(filepath)[0],
                                              headers={"Cache-Control": "public, max-age=600"})

    def _on_help(self, _):
        fuipdf = lawwenda.datafiles.find_data_file("ui.pdf")
        if not fuipdf:
            return werkzeug.routing.RequestRedirect(
                "https://pseudopolis.eu/wiki/pino/projs/lawwenda/FULLREADME/UI.html")
        with open(fuipdf, "rb") as f:
            return werkzeug.wrappers.Response(f.read(), mimetype="application/pdf",
                                              headers={"Cache-Control": "public, max-age=600"})

    def __render_template(self, template: str, *, html_head_inner: str = "", path: str = "", headonly: bool = False,
                          url_internals_name: str = URL_INTERNALS_NAME, **kwargs) -> werkzeug.wrappers.Response:
        csrftoken = base64.b64encode(os.urandom(64)).decode()
        respdata = "" if headonly else self.__render_template_text(
            template, **kwargs, html_head_inner=html_head_inner, url_internals_name=url_internals_name, path=path,
            rootname=self.__share.title, accessmode="readwrite" if self.__filesystem.rootnode.is_writable else "read",
            csrftoken=csrftoken)
        result = werkzeug.wrappers.Response(respdata, mimetype=mimetypes.guess_type(template)[0],
                                            headers={"Cache-Control": "public, max-age=600"})
        result.set_cookie("csrftoken", csrftoken)
        return result

    def __render_template_text(self, template: str, *, csrftoken: str, html_head_inner: str, **kwargs) -> str:
        html_body_inner = self.__render_template_text_raw(template, **kwargs)
        return self.__render_template_text_raw("base.html", **kwargs, html_head_inner=html_head_inner,
                                               html_body_inner=html_body_inner, csrftoken=csrftoken)

    def __render_template_text_raw(self, template: str, **kwargs) -> str:
        with open(f"{self.__mydir}/templates/{template}", "r") as f:
            return f.read().format(**{k: _RenderTemplateValue(v) for k, v in kwargs.items()})

    def __auth(self, username: str, password: str) -> bool:
        if not self.__share.password_scrypt:
            return True
        if len(username) > 100 or len(password) > 100:
            return False
        with self.__authlock:
            result = self.__authcache.get((username, password))
            if result is None:
                salt = base64.b64decode(self.__share.password_salt)
                sharescrypt = base64.b64decode(self.__share.password_scrypt)
                pwscrypt = hashlib.scrypt(password.encode(), salt=salt, n=2 ** 14, r=8, p=1)
                result = pwscrypt == sharescrypt
                if len(self.__authcache) > 30:
                    self.__authcache.pop(random.choice(list(self.__authcache.keys())))
                self.__authcache[(username, password)] = result
        return result

    def __ensure_authed(self, request):
        if self.__share.password_scrypt:
            reqauth = request.authorization
            if reqauth:
                if not (reqauth.password and self.__auth(reqauth.username, reqauth.password)):
                    raise werkzeug.exceptions.Forbidden()
            else:
                raise werkzeug.exceptions.Unauthorized(
                    www_authenticate=f'Basic realm="file share: {self.__share.name}"')

    def __dispatch_request(self, request):
        try:
            self.__ensure_authed(request)
        except werkzeug.exceptions.HTTPException as ex:
            return ex
        if f"/{self.URL_INTERNALS_NAME}/" in request.environ["PATH_INFO"]:
            return self.__dispatch_request_internals(request)
        return self.__dispatch_request_normal(request)

    def __dispatch_request_internals(self, request):
        if request.method not in ["GET", "HEAD"]:
            csrftoken1 = request.cookies.get("csrftoken")
            csrftoken2 = request.headers.get("X-CSRFToken")
            if (not csrftoken1) or (csrftoken1 != csrftoken2):
                return werkzeug.exceptions.Forbidden("csrf tokens do not match (cookies disables?)")
        pathsegment = None
        while pathsegment != self.URL_INTERNALS_NAME:
            pathsegment = werkzeug.wsgi.pop_path_info(request.environ)
        adapter = self.__url_map.bind_to_environ(request.environ)
        endpoint, values = adapter.match()
        try:
            return getattr(self, f"_on_{endpoint}")(request, **values) or lawwenda.comm.JsonedResponse(None)
        except werkzeug.exceptions.HTTPException as ex:
            return ex

    def __dispatch_request_normal(self, request):
        fsnode = self.__filesystem.node_by_path(request.path)
        if request.method in ["GET", "HEAD"] and fsnode.is_dir:
            if not request.environ["PATH_INFO"].endswith("/"):
                rurl = request.url
                if not rurl.endswith("/"):
                    rurl = f"{rurl}/"
                return werkzeug.routing.RequestRedirect(rurl)
            return self.__render_template("index.html", path=request.path, html_head_inner=f"""
            <script type="module" src="{self.URL_INTERNALS_NAME}/static/pageresources/index.js"></script>
            <link rel="stylesheet" href="{self.URL_INTERNALS_NAME}/static/pageresources/index.css" type="text/css"/>
                                          """)
        return None

    def __call__(self, environ, start_response):
        request = lawwenda.comm.Request(environ)
        response = self.__dispatch_request(request)
        return (response or self.__sharehttpapp)(environ, start_response)


class _TempZips:
    """
    Handler for temporary zip files.

    Allows to create zip files containing some nodes and automatically cleans them up after some time.

    This is a static class, potentially used by many applications in parallel.
    """

    class _TempZip:
        """
        A temporary zip file.
        """

        @staticmethod
        def __is_executable(node: "lawwenda.fs.Filesystem.Node") -> bool:
            fullpath = node.try_get_fullpath(writable=False)
            return fullpath and (os.stat(fullpath).st_mode & stat.S_IXUSR) == stat.S_IXUSR

        def __putnode(self, node: "lawwenda.fs.Filesystem.Node", zipf: zipfile.ZipFile) -> None:
            for cnode, fzn in node.traverse_dir(param_path=node.name, raise_on_circle=False):
                zfzn = fzn[1:]
                zdata = b""
                if cnode.is_dir:
                    zfzn = f"{zfzn}/"
                    zattr = 0o755 << 16
                    zattr |= 1 << 14 << 16  # unix directory flag
                    zattr |= 0x10  # MS-DOS directory flag
                else:
                    with cnode.read_file() as f:
                        zdata = f.read()
                    zattr = 0o644 << 16
                    zattr |= 1 << 15 << 16  # unix file flag
                    if self.__is_executable(cnode):
                        zattr |= 0o111 << 16
                zipinfo = zipfile.ZipInfo(zfzn, cnode.mtime.timetuple()[:6])
                zipinfo.external_attr = zattr
                zipf.writestr(zipinfo, zdata)

        def __init__(self, nodes: t.List["lawwenda.fs.Filesystem.Node"]):
            self.zipid = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(512))
            zipstream = io.BytesIO()
            with zipfile.ZipFile(zipstream, "w", zipfile.ZIP_DEFLATED) as zipf:
                for node in nodes:
                    self.__putnode(node, zipf)
            self.__bytes = zipstream.getvalue()

        @property
        def bytes(self):
            """
            The binary representation of this temporary zip archive.
            """
            return self.__bytes

    _zips = {}
    _cleanup_thread = None
    _lock = threading.Lock()

    @classmethod
    def create_tempzip(cls, owner: object, nodes: t.List["lawwenda.fs.Filesystem.Node"]) -> str:
        """
        Create a temporary zip archive from some nodes in memory and return an identifier.

        See also :py:meth:`get_tempzip`.

        :param owner: Request owner. Can be an arbitrary object (but must be equal for all calls that belong together).
        :param nodes: The nodes to include in the zip archive.
        """
        retention_time_secs = 60 * 10
        with cls._lock:
            if not cls._cleanup_thread:
                cls._cleanup_thread = threading.Thread(target=cls.__cleanup_loop, daemon=True)
                cls._cleanup_thread.start()
            tempzip = cls._TempZip(nodes)
            cls._zips[(owner, tempzip.zipid)] = (tempzip, time.time() + retention_time_secs)
            return tempzip.zipid

    @classmethod
    def get_tempzip(cls, owner: object, zipid: str) -> t.Optional[bytes]:
        """
        Return the binary content of a zip archive that was created before by :py:meth:`create_tempzip`.

        :param owner: Request owner. Can be an arbitrary object (but must be equal for all calls that belong together).
        :param zipid: The identifier returned by `create_tempzip`.
        """
        with cls._lock:
            tempzip, _ = cls._zips.get((owner, zipid)) or (None, None)
            return tempzip.bytes if tempzip else None

    @classmethod
    def __cleanup_loop(cls):
        while True:
            tnow = time.time()
            with cls._lock:
                for key, (_, keep_until) in list(cls._zips.items()):
                    if keep_until < tnow:
                        cls._zips.pop(key)
            time.sleep(60)


class _RenderTemplateValue:
    """
    String representation for usage in template rendering.

    Usually an html escaped variant of the input string, but with an option to also get the unescaped string.
    """

    def __init__(self, s):
        self.__s = str(s)
        self.__htmlescaped_s = html.escape(self.__s)

    def __str__(self):
        return self.__htmlescaped_s

    @property
    def unescaped(self):
        """
        The unescaped string.
        """
        return self.__s
