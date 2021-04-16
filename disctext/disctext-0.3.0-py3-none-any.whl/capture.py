import os 
import cv2 
import threading 
from eventkit import Event


class Capture(Event):
    """ 
    Read video files and emit image frames:: 

        Capture -> emit(image)
    """
    
    def __init__(self, path):
        Event.__init__(self) 
        path = str(path)
        self.capture = cv2.VideoCapture(path)
        self.filename = os.path.split(path)[-1]
        self.frames = int(self.capture.get(
                            cv2.CAP_PROP_FRAME_COUNT))
        
    def read(self):
        while self.capture.isOpened():
            success, frame = self.capture.read()
            if not success:
                break 
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.emit_threadsafe(image)
        self.capture.release()

    def start(self):
        self.thread = threading.Thread(target = self.read)
        self.thread.start()

    def stop(self):
        if self.capture.isOpened():
            self.capture.release()
        self.thread.join()

