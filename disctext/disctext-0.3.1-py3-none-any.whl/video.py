from __future__ import annotations
import numpy as np
import threading
import cv2
import os
import re
import sys

from eventkit import Event, Op


PIXELS = [' ', '.', ':', '-', '=', '+', '*', '#', '%', '@']
NUM_PIXELS = len(PIXELS)


def maximize(video: Video):
    h, w, c, a = (video.height,  video.width,
                  video.columns, video.area)

    sh = np.zeros(4)
    for mc in range(c.min, c.max):
        mw = w/mc
        mh = mw * 2
        mr = h/mh
        ta = mr * mc
        if ta > a.max:
            break
        sh = np.array([mh, mw, mr, mc], "i")
    return sh


class Video(object):

    def __init__(self, settings):
        self.settings = settings
        self.capture = cv2.VideoCapture(settings.media)
        #self.seek(0)

    @property
    def frames(self):
        return int(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))

    @property
    def fps(self):
        return int(self.capture.get(cv2.CAP_PROP_FPS))

    @property
    def position(self):
        return int(self.capture.get(cv2.CAP_PROP_POS_FRAMES))

    @position.setter
    def position(self, num: int):
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, int(num))

    @property
    def remaining(self):
        return self.frames - self.position

    @property
    def elapsed(self):
        return self.capture.get(cv2.CAP_PROP_POS_MSEC)

    @property
    def duration(self):
        return round(self.frames/self.fps, 2)

    @property
    def height(self):
        return int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    @property
    def width(self):
        return int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))

    @property
    def shape(self):
        return maximize(self)

    @property
    def rate(self):
        return self.settings.rate

    @property
    def area(self):
        return self.settings.area

    @property
    def columns(self):
        return self.settings.cols

    @property
    def filepath(self):
        return self.settings.media

    @property
    def filename(self):
        return os.path.split(self.filepath)[-1]

    @property
    def inverted(self):
        return bool(self.settings.inverted)

    @property
    def syntax(self):
        return str(self.settings.highlight)

    @property
    def pixels(self):
        return PIXELS.reverse() if self.inverted else PIXELS

    @property
    def opened(self):
        return self.capture.isOpened()

    def seek(self, position: int):
        return self.capture.set(
            cv2.CAP_PROP_POS_AVI_RATIO, int(position))

    def close(self):
        if self.opened:
            self.capture.release()

    def _read(self):
        if self.opened:
            return self.capture.read()
        else:
            return False, np.array([])


class Capture(Event):

    def __init__(self, video: Video):
        Event.__init__(self)
        self.video = video
        self.thread = None

    def read(self):
        while self.video.opened:
            success, frame = self.video._read()
            if not success:
                break
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.emit_threadsafe(image)
        self.video.close()

    def start(self):
        self.thread = threading.Thread(target=self.read)
        self.thread.start()


class Canvas(Op):

    def __init__(self, video: Video, source: Event = None):
        Op.__init__(self, source)
        self.video = video
        self.wspace = video.pixels.index(" ")
        self.minimum = video.area.min

    def on_source(self, image):
        ih, iw = image.shape
        mh, mw, mr, mc = self.video.shape

        mat = np.zeros((mr, mc), int)
        for x in range(mr):
            for y in range(mc):
                hx = x * mh
                wx = y * mw
                hy = min((x + 1) * mh, ih)
                wy = min((y + 1) * mw, iw)
                m = np.mean(image[hx:hy, wx:wy])
                idx = min(m * NUM_PIXELS/255, NUM_PIXELS - 1)
                mat[x][y] = int(idx)

        unique, inverse, count = np.unique(mat, False, True, True)
        if self.minimum > 0:
            if self.wspace in unique:
                i, *_ = np.where(unique == self.wspace)
                if (mr * mc) - count[i[0]] < self.minimum:
                    return

        frame = np.array([self.video.pixels[x] for x in unique])[
            inverse].reshape((mr, mc))
        block = self.pack(frame)
        if len(block) <= 2000:
            self.emit(block)
        del block

    def pack(self, frame):
        text = ["".join(row) for row in frame.tolist()]
        return "\n".join(['```' + self.video.syntax, *text, '```'])


class Progress(Op):

    def __init__(self, video: Video, width: int = 50, source=None):
        Op.__init__(self, source)
        self.connect(self.display)
        self.count = 0
        self.width = width
        self.total = video.frames
        self.format = re.sub(r"(?P<name>%\(.+?\))d",
                             r"\g<name>%dd" % len(str(self.total)),
                             "%s [%d/%d, %3d%%]")

    def display(self):
        count, total, width = self.count, self.total, self.width
        ratio = count/total
        size = int(width * ratio)
        progress = "   |" + "█" * size + " " * (width - size) + "|"
        print("\r" + self.format % (
            progress, count, total, ratio * 100), file=sys.stderr, end="")

    def on_source(self, *args):
        self.count += 1
        self.emit()
    
    def on_source_done(self, source):
        self.count = self.total
        self.emit()
        print("", file=sys.stderr)
        print("\n\n=> Finished reading source")

