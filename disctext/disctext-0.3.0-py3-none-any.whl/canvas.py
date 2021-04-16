import numpy as np 
from eventkit import Op

from . import settings

pixels = " .:-=+*#%@"

class Draw(Op):
    """ 
    Generate text frames from images::

        Draw(image) -> emit(frame)
    """
    def __init__(self, source = None):
        Op.__init__(self, source)
        self.resized = None 
        self.pixels = pixels[::-1] if settings.REVERSE else pixels
        self.max_a, self.min_a = settings.MAX_AREA, settings.MIN_AREA
        self.max_c, self.min_c = settings.MAX_COLS, settings.MIN_COLS

    def on_source(self, image):
        ih, iw = image.shape

        #TODO: make this part flow better
        if self.resized is None:
            self.maximize(ih, iw)
        th, tw, tr, tc = self.resized

        # find the mean pixel value by calculating the mean along both axis of the image array
        grid = np.zeros((tr, tc), int)
        for r in range(tr):
            for c in range(tc):
                # compute region of interest
                hx = r * th 
                wx = c * tw 
                hy = min((r + 1) * th, ih)
                wy = min((c + 1) * tw, iw)
                # average region
                roi = np.mean(image[hx:hy, wx:wy])    
                # assign pixel index 
                idx = min(roi * len(pixels)/255, len(pixels) - 1) 
                grid[r][c] = int(idx)
        
 
        unique, inverse, count = np.unique(grid, False, True, True)
        # index of whitespace
        ws = self.pixels.index(" ")
        if ws in unique:
            index, *_ = np.where(unique == ws)
            # number of non-whitespace
            if (tr * tc) - count[index[0]] > self.min_a:
                frame = np.array([self.pixels[x] for x in unique])[inverse].reshape((tr, tc))
                self.emit(frame)


    def maximize(self, h, w):
        """ 
        Maximize the area of a text frame and return its shape.  
        """
        im = np.zeros(4)
        for tc in range(self.min_c, self.max_c):
            tw = w/tc
            th = tw * 2
            tr = h/th
            ta = tr * tc 

            if ta > self.max_a:
                break 
            im = np.array([th, tw, tr, tc], "i") 
        self.resized = im  



class Pack(Op):
    """
    Format text frames into code blocks::

        Pack(frame) -> emit(block)
    """
    def __init__(self, source = None):
        Op.__init__(self, source)
        self.pixels = pixels[::-1] if settings.REVERSE else pixels
        self.syntax = settings.SYNTAX

    def on_source(self, frame):
        textframes = ["".join(row) for row in frame.tolist()]
        textblock = "\n".join(['```' + self.syntax, *textframes, '```'])
        
        if len(textblock) <= 2000:
            self.emit(textblock)