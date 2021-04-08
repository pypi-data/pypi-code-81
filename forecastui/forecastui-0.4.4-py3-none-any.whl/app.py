from forecastui.writers import file
from flask import Flask, current_app,jsonify, request, render_template, Response, current_app
from flask_socketio import SocketIO, emit
from flask_restful import Resource, Api, inputs
from signal import signal, SIGINT
from datetime import datetime
from queue import Empty
from engineio.async_drivers import threading
import threading
import time
import pathlib
import logging
import os, sys

from .callbacks import *
from .communication import SerialManager
from .utility import SettingsManager, Paths, Store
from .api import *
from .writers import LogFile, FileWriter



folderpath = pathlib.Path(__file__).resolve().parent # __file__ not good for pyinstaller


class ATLAS:

    def __init__(self, port=5000, first_boot=False, updates=(False, "", "")):

        template_path = folderpath / "./dist_client"
        static_path = folderpath / "./dist_client/static"

        self.__first_boot = first_boot
        self.__has_updated, self.__conf_version, self.__installed_version = updates

        Store.port = port
        Store.preset = Preset()

        self.__app = Flask("app", template_folder = str(template_path.resolve()), static_folder = str(static_path.resolve()))
        self.__app.atlas = self
        self.__app.secret_key = os.urandom(24)
        self.__io = SocketIO(self.__app, cors_allowed_origins="http://127.0.0.1:{}".format(Store.port), async_mode='threading')
        self.__api = Api(self.__app)

        self.settings = SettingsManager()
        if self.__has_updated:
            self.settings.set("App", "version", self.__installed_version)
        self.paths = Paths(self.settings.getAll("Directories"))

        self.refresh_rate = 20
        self.serial = None
        self.history = {}

        self.__app.add_url_rule('/<path:path>', 'catchall', self.index)
        self.__app.add_url_rule('/', 'index', self.index, defaults={'path': ''})

        self.__api.add_resource(Ports, "/api/getports")
        self.__api.add_resource(Connection, "/api/connection")
        self.__api.add_resource(StartConnection, "/api/startconnection")
        self.__api.add_resource(StopConnection, "/api/stopconnection")
        self.__api.add_resource(StartExperiment, "/api/startexperiment")
        self.__api.add_resource(StopExperiment, "/api/stopexperiment")
        self.__api.add_resource(Settings, "/api/settings")
        self.__api.add_resource(PresetsApi, "/api/presets")
        self.__api.add_resource(PathsApi, "/api/filesystem")
        self.__api.add_resource(OpenApi, "/api/open")

        self.__api.add_resource(BoardStatus, "/api/board/status")
        self.__api.add_resource(BoardSendData, "/api/board/send-data")
        self.__api.add_resource(BoardParameter, "/api/board/parameter")

        self.__io.on_event("data-send", self.callback)
        self.__io.on_event("connect", self.__on_connect)

    def start(self, use_webbrowser=True):
        def web():
            import webbrowser
            webbrowser.open("http://127.0.0.1:{}".format(Store.port))
            self.run()

        def qt_app():
            self.ui = pycuteweb.Application(name="Forecast")
            self.window = self.ui.spawn_window("http://127.0.0.1:{}".format(Store.port), title="Forecast", icon= str(folderpath / "assets" / "logo.svg"))
            threading.Thread(target=self.run, daemon=True).start()
            self.ui.start()

        if use_webbrowser:
            web()
        else:
            try:
                import pycuteweb
            except ModuleNotFoundError:
                web()
                return
            qt_app()

    def run(self):
        print("Running on http://127.0.0.1:{}".format(Store.port))
        self.__io.run(self.__app, port=Store.port)

    def index(self, path):
        return render_template("index.html")

    def __on_connect(self):
        import pkg_resources
        version = pkg_resources.get_distribution("forecastui").version

        with self.__app.app_context():
            emit("boot_settings", {"first_boot": self.__first_boot,
                "version": version,
                "updates": {
                    "has_updated": self.__has_updated,
                    "previous_version": self.__conf_version,
                    "current_version": self.__installed_version
                    }
                }, broadcast=True, namespace="/")

    def callback(self, value):
        self.serial.input_value(value)

    def add_api(self, api, route):
        self.__api.add_resource(api, route)

    def reset(self):
        self.history = {}

    def start_serial(self, port, baud):
        """
        The serial handler gets initialized, along with the data request and status
        callback (usefull for debugging the handshake).
        It also starts the logging and websocket workers when the loop starts.
        """
        try:
            self.serial = SerialManager()
            self.reset()
            self.serial.start(port=port, baudrate=baud)
            return (self.serial.is_connected, "Serial initialized")
        except Exception as e:
            print(str(e))
            return (False, str(e))

    def start_experiment(self, index):
        self.__retrieveLogsWorker = threading.Thread(target=self.write_logs, args=tuple([index]), daemon=True)
        self.__retrieveErrorsWorker = threading.Thread(target=self.send_errors, daemon=True)
        self.__broadcastWorker = threading.Thread(target=self.show_logs, daemon=True)
        self.__logCount = 0
        self.__logsBuffer = []
        self.serial.start_experiment(index)
        self.__retrieveLogsWorker.start()
        self.__broadcastWorker.start()
        self.__retrieveErrorsWorker.start()

    def stop_experiment(self):
        self.serial.stop_experiment()
        print("Interrupting logging worker thread... ", end="")
        self.__retrieveLogsWorker.join()
        print("Done!")
        print("Interrupting network worker thread... ", end="")
        self.__broadcastWorker.join()
        print("Done!")
        print("Interrupting error worker thread... ", end="")
        self.__retrieveErrorsWorker.join()
        print("Done!")
        print("Experiment stopped!")
        return True

    def stop_serial(self):
        """
        Gracefully stops the serial by exiting the handler loop and killing the
        workers' threads.
        """
        if self.serial.is_running:
            self.stop_experiment()
        print("Asking the serial handler to stop... ")
        self.history = self.serial.stop()
        print("Done!")
        del self.serial
        print("self.serial stopped!")
        return (True, "Serial connection ended")

    def write_logs(self, index):
        """
        Retrieves the logs from the serial handler object and puts them in a buffer.
        It also writes them to file
        """

        if type(Store.filename) == list:
            filename = Store.filename[index]
        elif type(Store.filename) == str:
            filename = Store.filename

        logfile = LogFile(self.paths.get("logs"), filename=filename)
        with FileWriter(logfile) as writer:
            while self.serial.is_running:
                try:
                    log = self.serial.getLog()
                except Empty as e:
                    continue
                writer.write(log)
                self.__logCount += 1
                self.__logsBuffer.append(log)
        if logfile.size()==0:
            logfile.delete()

    def show_logs(self):
        """
        Retrieves the first n logs from the buffer, where n is the current buffer length,
        by splicing the array between 0:n and n:end.

        The first half gets sent via websocket.
        The second half of the array (which may have changed since the splicing)
        becomes the regular buffer.
        """
        with self.__app.app_context():
            j = 0
            ns = 0
            while self.serial.is_running:
                n = len(self.__logsBuffer)
                to_send = self.__logsBuffer[0:n]
                self.__logsBuffer = self.__logsBuffer[n:]
                j = (j+1)%self.refresh_rate
                if j == 0:
                    ns = self.__logCount
                emit("log", {"logs": to_send, "qsize": ns}, broadcast=True, namespace="/")
                if j == 0:
                    self.__logCount = 0
                time.sleep(1/self.refresh_rate)

    def send_errors(self):
        """
        Retrieves the errors
        """
        with self.__app.app_context():
            while self.serial.is_running:
                try:
                    error_type, stack = self.serial.getError()
                    emit("error", {"type": error_type, "message": stack}, broadcast=True, namespace="/")
                except Empty as e:
                    pass


def detect_os():
    import platform
    return platform.system()


def am_i_root():
    if detect_os() == "Linux":
        return os.geteuid() == 0
    return False

def get_free_port():
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--web", help="Displays the UI using the system installed webbrowser", action="store_true")
    args = parser.parse_args()
    use_webbrowser = args.web

    def sigintHandler(a, b):
        print("Closing application!")
        exit(0)
    signal(SIGINT, sigintHandler)

    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    cli = sys.modules['flask.cli']
    cli.show_server_banner = lambda *x: None

    if am_i_root():
        print("You are currently a super user. Run this script without root privileges :)")
        sys.exit(0)

    from .utility import Doctor
    doc = Doctor()
    first_boot = doc.is_first_start()
    doc.init()
    doc.create_folders()

    has_updated, conf_version, installed_version = doc.just_updated()

    app = ATLAS(port=get_free_port(), first_boot=first_boot or has_updated, updates=(has_updated, conf_version, installed_version))
    app.start(use_webbrowser)
