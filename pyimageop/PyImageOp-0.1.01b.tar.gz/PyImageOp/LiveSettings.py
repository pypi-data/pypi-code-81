import cv2 as cv
import numpy as np
from PyImageOp.HSV import HsvFilter
import logging

log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)


class Settings:
    def __init__(self, needle_img_path=None, method=cv.TM_CCOEFF_NORMED, debug=False):
        """
        Initialize and set class parameters

        Parameters
        ----------
        needle_img_path : string
            path to img to be find if any to be
        method : string
            TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
        debug : boolean
            show debug messages
        """
        if needle_img_path is None:
            self.needle_img = None
        else:
            self.needle_img = cv.imread(needle_img_path, cv.IMREAD_UNCHANGED)
            self.needle_w = self.needle_img.shape[1]
            self.needle_h = self.needle_img.shape[0]

        self.method = method
        self.debug = debug
        self.TRACKBAR_WINDOW = "Trackbars"

    def find(self, haystack_img, threshold=0.5, max_results=10):
        """
        Find the provided image in class on image provided to the method

        Parameters
        ----------
        haystack_img : image
            image to be look on while searching
        threshold : float
            acceptance of probability
        max_results : int
            max results that it can find

        Returns
        -------
        array_like
            position of rectangles around the found item
        """
        if self.needle_img is None:
            raise Exception("You can't use this method without providing image ")
        result = cv.matchTemplate(haystack_img, self.needle_img, self.method)

        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))

        if not locations:
            return np.array([], dtype=np.int32).reshape(0, 4)

        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.needle_w, self.needle_h]
            rectangles.append(rect)
            rectangles.append(rect)

        rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)

        if len(rectangles) > max_results:
            log.warning('Warning: too many results, raise the threshold.')
            rectangles = rectangles[:max_results]

        return rectangles

    @staticmethod
    def get_click_points(rectangles):
        """
        Returns central points of found items

        Parameters
        ----------
        rectangles : array_like
            list of rectangles from find function

        Returns
        -------
        array_like
            list of center points
        """
        points = []

        for (x, y, w, h) in rectangles:
            center_x = x + int(w / 2)
            center_y = y + int(h / 2)
            points.append((center_x - 20, center_y + 50))

        return points

    @staticmethod
    def draw_rectangles(haystack_img, rectangles):
        """
        Draws rectangles on provided coordinates on provided image

        Parameters
        ----------
        haystack_img : image
            image on which to draw
        rectangles : array_like
            list of rectangles coordinates

        Returns
        -------
        image
            image with rectangles drawn on it
        """
        line_color = (0, 255, 0)
        line_type = cv.LINE_4

        for (x, y, w, h) in rectangles:
            top_left = (x, y + 150)
            bottom_right = (x + w, y + h - 50)
            cv.rectangle(haystack_img, top_left, bottom_right, line_color, lineType=line_type)

        return haystack_img

    @staticmethod
    def draw_crosshair(haystack_img, points):
        """
        Draws crosshair on provided coordinates

        Parameters
        ----------
        haystack_img : image
            image to be printed crosshair on
        points : array_like
            list of coordinates where crosshairs have to be printed on

        Returns
        -------
        image
            image with drawn crosshairs
        """
        marker_color = (255, 0, 255)
        marker_type = cv.MARKER_CROSS

        for (center_x, center_y) in points:
            cv.drawMarker(haystack_img, (center_x, center_y), marker_color, marker_type)

        return haystack_img

    @staticmethod
    def draw(haystack_img):
        """
        return image itself without editing

        Parameters
        ----------
        haystack_img : image
            image to draw

        Returns
        -------
        image
            image without editing
        """
        return haystack_img

    def init_control_gui(self):
        """
        Initialize gui of hsv controls for debugging
        """
        cv.namedWindow(self.TRACKBAR_WINDOW, cv.WINDOW_NORMAL)
        cv.resizeWindow(self.TRACKBAR_WINDOW, 350, 700)

        def nothing(fill):
            if self.debug:
                print(fill)
            pass

        cv.createTrackbar('HMin', self.TRACKBAR_WINDOW, 0, 179, nothing)
        cv.createTrackbar('SMin', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VMin', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('HMax', self.TRACKBAR_WINDOW, 0, 179, nothing)
        cv.createTrackbar('SMax', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VMax', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.setTrackbarPos('HMax', self.TRACKBAR_WINDOW, 179)
        cv.setTrackbarPos('SMax', self.TRACKBAR_WINDOW, 255)
        cv.setTrackbarPos('VMax', self.TRACKBAR_WINDOW, 255)

        cv.createTrackbar('SAdd', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('SSub', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VAdd', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VSub', self.TRACKBAR_WINDOW, 0, 255, nothing)

    def get_hsv_filter_from_controls(self):
        """
        Gets data from sliders

        Returns
        -------
        dictionary
            dict of all values from hsv sliders
        """
        hsv_filter = HsvFilter()
        hsv_filter.hMin = cv.getTrackbarPos('HMin', self.TRACKBAR_WINDOW)
        hsv_filter.sMin = cv.getTrackbarPos('SMin', self.TRACKBAR_WINDOW)
        hsv_filter.vMin = cv.getTrackbarPos('VMin', self.TRACKBAR_WINDOW)
        hsv_filter.hMax = cv.getTrackbarPos('HMax', self.TRACKBAR_WINDOW)
        hsv_filter.sMax = cv.getTrackbarPos('SMax', self.TRACKBAR_WINDOW)
        hsv_filter.vMax = cv.getTrackbarPos('VMax', self.TRACKBAR_WINDOW)
        hsv_filter.sAdd = cv.getTrackbarPos('SAdd', self.TRACKBAR_WINDOW)
        hsv_filter.sSub = cv.getTrackbarPos('SSub', self.TRACKBAR_WINDOW)
        hsv_filter.vAdd = cv.getTrackbarPos('VAdd', self.TRACKBAR_WINDOW)
        hsv_filter.vSub = cv.getTrackbarPos('VSub', self.TRACKBAR_WINDOW)
        return hsv_filter

    def apply_hsv_filter(self, original_image, hsv_filter=None):
        """
        Applies provided filter on image if not provided filter it will update from sliders

        Parameters
        ----------
        original_image : image
            image to add filters on
        hsv_filter : Object
            Object HsvFilter to get data from

        Returns
        -------
        image
            image with added filters on
        """
        hsv = cv.cvtColor(original_image, cv.COLOR_BGR2HSV)

        if not hsv_filter:
            hsv_filter = self.get_hsv_filter_from_controls()

        h, s, v = cv.split(hsv)
        s = self._shift_channel(s, hsv_filter.sAdd)
        s = self._shift_channel(s, -hsv_filter.sSub)
        v = self._shift_channel(v, hsv_filter.vAdd)
        v = self._shift_channel(v, -hsv_filter.vSub)
        hsv = cv.merge([h, s, v])

        lower = np.array([hsv_filter.hMin, hsv_filter.sMin, hsv_filter.vMin])
        upper = np.array([hsv_filter.hMax, hsv_filter.sMax, hsv_filter.vMax])

        mask = cv.inRange(hsv, lower, upper)
        result = cv.bitwise_and(hsv, hsv, mask=mask)

        img = cv.cvtColor(result, cv.COLOR_HSV2BGR)
        return img

    @staticmethod
    def _shift_channel(c, amount):
        """
        Helper method
        Makes sure that limit isn't passed

        Parameters
        ----------
        c : value
            current value
        amount : int
            min and max values

        Returns
        -------
        int
            current value to be set
        """
        if amount > 0:
            lim = 255 - amount
            c[c >= lim] = 255
            c[c < lim] += amount
        elif amount < 0:
            amount = -amount
            lim = amount
            c[c <= lim] = 0
            c[c > lim] -= amount
        return c
