# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

"""
A wsgi application that provides an http interface to a filesystem.

See :py:class:`ShareHttpApp`.
"""

import json
import mimetypes
import typing as t
import xml.etree.ElementTree as ET

import werkzeug.exceptions
import werkzeug.routing
import werkzeug.serving
import werkzeug.wrappers.json
import werkzeug.wsgi

import lawwenda.comm
import lawwenda.sharehttpapp.davprop

if t.TYPE_CHECKING:
    import lawwenda.fs


# pylint: disable=no-self-use,unused-argument
class ShareHttpApp:
    """
    A wsgi application that provides an http interface to a filesystem.

    It provides bare http access, and also WebDAV extensions for a more complete interface. It does not provide an own
    user interface or user authentication.
    """

    # TODO ensure (list, get, put) compat with nautilus, dolphin, windows
    # TODO prevent csrf in webdav?! (e.g. use another auth realm name somehow?! but how?!)
    # TODO review all
    # TODO If-Range?

    def __init__(self, filesystem: "lawwenda.fs.Filesystem"):
        self.__filesystem = filesystem

    @property
    def filesystem(self) -> "lawwenda.fs.Filesystem":
        """
        The filesystem used by this ShareHttpApp.
        """
        return self.__filesystem

    def _method_get(self, request: lawwenda.comm.Request, fsnode: "lawwenda.fs.Filesystem.Node",
                    is_head_request: bool = False):
        if fsnode.is_file:
            respdata = b""
            sranges = request.headers.get("Range") or ""
            headers = {"Accept-Ranges": "bytes"}
            status = 200
            rangeend = -1
            rangebegin = -1
            if sranges.startswith("bytes="):
                rangebegin = fsnode.size
                rangeend = -1
                for srange in [r for r in [r.strip() for r in sranges[6:].split(",")] if r]:
                    srangetup = srange.split("-")
                    if len(srangetup) == 2:
                        rangebegin = min(int(srangetup[0]), rangebegin)
                        rangeend = max(int(srangetup[1] or fsnode.size - 1), rangeend)
                if rangeend != -1:
                    headers["Content-Range"] = f"bytes {rangebegin}-{rangeend}/{fsnode.size}"
                    status = 206
            if not is_head_request:
                with fsnode.read_file() as f:
                    if rangeend != -1:
                        f.seek(rangebegin)
                    respdata = f.read((rangeend - rangebegin + 1) if (rangeend != -1) else -1)
            return werkzeug.wrappers.Response(respdata, mimetype=mimetypes.guess_type(fsnode.path)[0],
                                              headers=headers, status=status)
        return werkzeug.exceptions.NotFound()

    def _method_head(self, request: lawwenda.comm.Request, fsnode: "lawwenda.fs.Filesystem.Node"):
        return self._method_get(request, fsnode, is_head_request=True)

    def _method_propfind(self, request: lawwenda.comm.Request, fsnode: "lawwenda.fs.Filesystem.Node"):
        props = []
        depth = request.headers.get("Depth", "infinity")
        if request.data:
            xreq = ET.fromstring(request.data)
            for cxreq in xreq:
                if cxreq.tag == "{DAV:}prop":
                    for ccxreq in cxreq:
                        props.append(ccxreq.tag)
        else:
            props = [prop.davname for prop in lawwenda.sharehttpapp.davprop.all_props]
        def _walker(xresult, walknode, furl, dpt):
            # TODO if not walknode.exists?!
            resp = ET.Element("{DAV:}response")
            resphref = ET.Element("{DAV:}href")
            resphref.text = furl
            resp.append(resphref)
            for prop in props:
                resppropstat = ET.Element("{DAV:}propstat")
                respstatus = ET.Element("{DAV:}status")
                respstatus.text = "HTTP/1.1 200 OK"
                resppropstat.append(respstatus)
                respprop = ET.Element("{DAV:}prop")
                resppropval = ET.Element(prop)
                dprop = lawwenda.sharehttpapp.davprop.get_prop_by_davname(prop)
                if dprop:
                    dpropval = dprop.get_for_node(walknode)
                    if isinstance(dpropval, ET.Element):
                        resppropval.append(dpropval)
                    else:
                        resppropval.text = str(dpropval)
                else:
                    respstatus.text = "HTTP/1.1 404 Not Found"
                respprop.append(resppropval)
                resppropstat.append(respprop)
                resp.append(resppropstat)
            xresult.append(resp)
            if (dpt != "0") and walknode.is_dir:
                for cfn in walknode.child_nodes:  # TODO prevent symlink circles
                    cfurl = f"{furl}{cfn.name}/"
                    _walker(xresult, cfn, cfurl, dpt if (dpt == "infinity") else "0")
        result = ET.Element("{DAV:}multistatus")
        _walker(result, fsnode, "./", depth)
        return werkzeug.wrappers.Response(ET.tostring(result), mimetype="text/xml", status=207)

    def _method_proppatch(self, request: lawwenda.comm.Request, fsnode: "lawwenda.fs.Filesystem.Node"):
        props = []  # TODO dedup
        xreq = ET.fromstring(request.data)
        for cxreq in xreq:
            if cxreq.tag == "{DAV:}prop":
                for cxreqprop in cxreq:
                    props.append(cxreqprop.tag)
        result = ET.Element("{DAV:}multistatus")
        resp = ET.Element("{DAV:}response")
        resphref = ET.Element("{DAV:}href")
        resphref.text = request.url
        resp.append(resphref)
        resppropstat = ET.Element("{DAV:}propstat")
        respstatus = ET.Element("{DAV:}status")
        respstatus.text = "HTTP/1.1 409 Conflict"
        # TODO complete answer instead (this is an incomplete dummy)
        resppropstat.append(respstatus)
        resp.append(resppropstat)
        result.append(resp)
        return werkzeug.wrappers.Response(ET.tostring(result), mimetype="text/xml", status=207)

    def _method_options(self, request: lawwenda.comm.Request, fsnode: "lawwenda.fs.Filesystem.Node"):
        return werkzeug.wrappers.Response(headers={"Allows": ", ".join(self.__allowed_methods), "DAV": "1"})

    def _method_put(self, request: lawwenda.comm.Request, fsnode: "lawwenda.fs.Filesystem.Node"):
        if (not fsnode.parent_node.is_dir) or fsnode.is_dir:
            return werkzeug.exceptions.Conflict()
        fsnode.write_file(request.data)  # TODO noh preserve metadata on overwrite?!
        return werkzeug.wrappers.Response(status=201)

    def _method_delete(self, request: lawwenda.comm.Request, fsnode: "lawwenda.fs.Filesystem.Node"):
        fsnode.delete()
        return werkzeug.wrappers.Response(status=204)

    def _method_mkcol(self, request: lawwenda.comm.Request, fsnode: "lawwenda.fs.Filesystem.Node"):
        fsnode.mkdir()
        return werkzeug.wrappers.Response(status=201)

    def _method_copy(self, request: lawwenda.comm.Request, fsnode: "lawwenda.fs.Filesystem.Node", *,
                     xfermethod: str = "copy_to"):
        if request.headers.get("overwrite") != "F":
            dstfsnode = self.__filesystem.node_by_path(request.headers["Destination"])
            if dstfsnode.exists:
                dstfsnode.delete()
            getattr(fsnode, xfermethod)(dstfsnode.path)

    def _method_move(self, request: lawwenda.comm.Request, fsnode: "lawwenda.fs.Filesystem.Node"):
        return self._method_copy(request, fsnode, xfermethod="move_to")

    @property
    def __allowed_methods(self) -> t.List[str]:
        return [m[8:].upper() for m in dir(self) if m.startswith("_method_")]

    def __call__(self, environ, start_response):
        request = lawwenda.comm.Request(environ)
        fsnode = self.__filesystem.node_by_path(request.path)
        fctmethod = getattr(self, f"_method_{request.method.lower()}")
        if fctmethod:
            response = fctmethod(request, fsnode)
        else:
            response = werkzeug.exceptions.MethodNotAllowed(valid_methods=self.__allowed_methods)
        return response(environ, start_response)
