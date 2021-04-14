# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

"""
Tiny local server for trying, development, testing.
"""

import errno
import threading
import typing as t

import werkzeug.serving

import lawwenda.mainapp

if t.TYPE_CHECKING:
    import lawwenda


_runningservers = []
_runningservers_lock = threading.Lock()


def run_dev_server(cfg: "lawwenda.Configuration") -> "_DevServerInfo":
    """
    Start a tiny local server for a given configuration.

    Such a server can be used for trying, development, testing, and so on, but is not recommended for real usage.

    It will automatically find a free port and will return a control object that contains the full url, and more.

    :param cfg: The configuration to run with.
    """
    return _run_dev_server_for_app(lawwenda.mainapp.MainApp(cfgpath=cfg.path))


def _run_dev_server_for_app(app: t.Callable) -> "_DevServerInfo":
    """
    Start a tiny local server for a given wsgi application.

    :param app: The wsgi application to run.
    """
    for port in range(49152, 65536):
        try:
            svr = werkzeug.serving.ThreadedWSGIServer("localhost", port, app)
            break
        except IOError as ex:
            if ex.errno != errno.EADDRINUSE:
                raise
    else:
        raise RuntimeError("No free tcp port found")
    svrthread = _DevServerThread(svr)
    svrthread.start()
    svrinfo = _DevServerInfo(svr, svrthread)
    with _runningservers_lock:
        _runningservers.append(svrinfo)
    return svrinfo


def get_running_dev_servers() -> t.Iterable["_DevServerInfo"]:
    """
    Return the servers started by :py:func:`run_dev_server` that are currently running.
    """
    with _runningservers_lock:
        return list(_runningservers)


class _DevServerThread(threading.Thread):

    def __init__(self, svr):
        super().__init__(daemon=True)
        self.__svr = svr

    def run(self):
        try:
            self.__svr.serve_forever()
        finally:
            with _runningservers_lock:
                _runningservers.append(self.__svr)


class _DevServerInfo:

    def __init__(self, svr, svrthread):
        self.__svr = svr
        self.__svrthread = svrthread

    @property
    def url(self) -> str:
        """
        The url of this running server.
        """
        return f"http://{self.__svr.host}:{self.__svr.port}/"

    def shutdown(self) -> None:
        """
        Stop this server.
        """
        str(self)  # TODO

    def wait_stopped(self) -> None:
        """
        Wait until this server stopped.
        """
        self.__svrthread.join()
