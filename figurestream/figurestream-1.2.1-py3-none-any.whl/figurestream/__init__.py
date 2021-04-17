import sys
import time
import threading
import logging
from io import BytesIO
from queue import Queue
from threading import Thread

from matplotlib.figure import Figure
from flask import Flask, Response, request, render_template_string


########################################################################
class StreamEvent:
    """An Event-like class that signals all active clients when a new frame is
    available.
    """

    # ----------------------------------------------------------------------
    def __init__(self):
        self.events = {}
        logging.debug(f'Instantiate {self!r}')

    # ----------------------------------------------------------------------
    def wait(self):
        """Invoked from each client's thread to wait for the next frame."""
        ident = threading.get_ident()
        if ident not in self.events:
            # this is a new client
            # add an entry for it in the self.events dict
            # each entry has two elements, a threading.Event() and a timestamp
            self.events[ident] = [threading.Event(), time.time()]
        return self.events[ident][0].wait()

    # ----------------------------------------------------------------------
    def set(self):
        """Invoked by the stream thread when a new frame is available."""

        now = time.time()
        to_remove = []
        for ident, event in self.events.items():
            if not event[0].isSet():
                # if this client's event is not set, then set it
                # also update the last set timestamp to now
                event[0].set()
                event[1] = now
            else:
                # if the client's event is already set, it means the client
                # did not process a previous frame
                # if the event stays set for more than 60 seconds, then assume
                # the client is gone and remove it
                if now - event[1] > 60:
                    logging.warning(f"Removing client {ident}")
                    to_remove.append(ident)

        for remove in to_remove:
            del self.events[remove]

    # ----------------------------------------------------------------------
    def clear(self):
        """Invoked from each client's thread after a frame was processed."""
        self.events[threading.get_ident()][0].clear()


########################################################################
class FigureStream(Figure):

    __class_attr = {
        'thread': None,  # background thread that reads frames from stream
        'frame': None,  # current frame is stored here by background thread
        'last_access': 0,  # time of last client access to the source,
        # 'keep_alive': time.time(),
        'event': StreamEvent(),
    }

    # ----------------------------------------------------------------------
    def __init__(self, host='localhost', port='5000', endpoint='', *args, **kwargs):
        """Start the background stream thread if it isn't running yet."""
        # logging.debug(f'Instantiate {self!r}')
        super().__init__(*args, **kwargs)
        self.__output = BytesIO()
        self.__buffer = Queue(maxsize=60)

        self.boundary = False
        self.subsample = None
        self.size = 'auto'
        # self.tight_layout(rect=[0, 0.03, 1, 0.95])

        if endpoint in ['figure.jpeg', 'mode', 'feed']:
            logging.error(
                f'The endpoint {endpoint} is already taken for internal use.')
            return

        self.app = Flask(__name__)
        self.app.add_url_rule(f'/figure.jpeg', view_func=self._video_feed)
        self.app.add_url_rule(f'/{endpoint}', view_func=self.figure_template)
        self.app.add_url_rule('/mode', view_func=self._mode)
        self.app.add_url_rule('/feed', view_func=self._feed)

        if len(sys.argv) > 1:
            port = sys.argv[1]
        else:
            port = port

        Thread(
            target=self.app.run,
            kwargs={'host': host, 'port': port, 'threaded': True},
        ).start()

    # ----------------------------------------------------------------------
    def figure_template(self):
        """"""
        if background := request.values.get('background', None):
            style = f'background-color: #{background};'
        else:
            style = ''
        get = '&'.join([f'{k}={v}' for k, v in request.values.items()])
        html = f"""

        <html>
          <body style='margin: 0;
                       background-image: url("/figure.jpeg?{get}");
                       background-repeat: no-repeat;
                       background-size: cover;
                       {style}
                       '>
          </body>
        </html>
        """

        return Response(render_template_string(html))

    # ----------------------------------------------------------------------
    def _feed(self):
        """"""
        self.feed()

    # ----------------------------------------------------------------------
    def _mode(self):
        """"""
        return 'visualization'

    # ----------------------------------------------------------------------
    def _get_frames(self):
        """Return the current stream frame."""

        while True:
            self.__class_attr['last_access'] = time.time()
            self.__class_attr['event'].wait()
            self.__class_attr['event'].clear()
            frame = self.__class_attr['frame']
            yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
            )

    # ----------------------------------------------------------------------
    def _thread(self):
        """stream background thread."""
        logging.info('Starting stream thread.')
        # frames_iterator = self.frames()
        # for frame in frames_iterator:
        while True:

            try:
                # frame = self.__buffer.get(timeout=5)
                frame = self.__buffer.get()
            except:
                break

            self.__class_attr['frame'] = frame
            self.__class_attr['event'].set()  # send signal to clients
            # time.sleep(0)

            # # if there hasn't been any clients asking for frames in
            # # the last 60 seconds then stop the thread
            # if time.time() - self.__class_attr['last_access'] > 60:
                # frames_iterator.close()
                # logging.info('Stopping stream thread due to inactivity.')
                # break

        self.__class_attr['thread'] = None

    # ----------------------------------------------------------------------
    def _video_feed(self):
        """"""
        if self.size == 'auto':
            width = request.values.get('width', None)
            height = request.values.get('height', None)
            if (
                width and
                height and
                width.replace('.', '').isdigit() and
                height.replace('.', '').isdigit()
            ):
                self.set_size_inches(float(width), float(height))

            dpi = request.values.get('dpi', None)
            if dpi and dpi.replace('.', '').isdigit():
                self.set_dpi(float(dpi))

        else:
            self.set_size_inches(*self.size)
            dpi = request.values.get('dpi', None)
            if dpi and dpi.replace('.', '').isdigit():
                self.set_dpi(float(dpi))

        if self.__class_attr['thread'] is None:
            self.__class_attr['last_access'] = time.time()
            # self.__class_attr['keep_alive'] = time.time()

            # start background frame thread
            self.__class_attr['thread'] = Thread(target=self._thread)
            self.__class_attr['thread'].start()

            # wait until frames are available
            while self._get_frames() is None:
                time.sleep(0.1)

        # self.feed()
        return Response(
            self._get_frames(),
            mimetype='multipart/x-mixed-replace; boundary=frame',
        )

    # ----------------------------------------------------------------------
    def feed(self):
        """"""
        self.__output.truncate(0)
        self.__output.seek(0)
        self.canvas.print_figure(
            self.__output, format='jpeg', dpi=self.get_dpi()
        )

        return self.__buffer.put(self.__output.getvalue())

    # # ----------------------------------------------------------------------
    # def show(self, *args, **kwargs):
        # """"""
        # self.feed()

