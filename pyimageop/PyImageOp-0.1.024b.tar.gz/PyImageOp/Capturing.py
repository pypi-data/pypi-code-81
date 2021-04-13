import cv2 as cv
import numpy as np
from mss import mss


class Capture:

    def __init__(self, window_name=None, border_pixels=8, title_bar_pixels=30):
        """
        Initialize parameters of Class

        Parameters
        ----------
        window_name : string
            name of window to be captured
        border_pixels : int
            border pixels except top to cut
        title_bar_pixels : int
            top of window pixels to cut
        """

        try:
            import win32gui
            import win32ui
            import win32con
            self.wincan = True

            if window_name is None:
                self.hwnd = win32gui.GetDesktopWindow()
            else:
                self.hwnd = win32gui.FindWindow(None, window_name)
                if not self.hwnd:
                    self.list_window_names()
                    raise Exception('Window not found: {}'.format(window_name))

            window_rect = win32gui.GetWindowRect(self.hwnd)
            self.width = window_rect[2] - window_rect[0]
            self.height = window_rect[3] - window_rect[1]

            self.border_pixels = border_pixels
            self.title_bar_pixels = title_bar_pixels
            self.width = self.width - (self.border_pixels * 2)
            self.height = self.height - self.title_bar_pixels - self.border_pixels
            self.cropped_x = self.border_pixels
            self.cropped_y = self.title_bar_pixels

            self.offset_x = window_rect[0] + self.cropped_x
            self.offset_y = window_rect[1] + self.cropped_y
        except ImportError:
            self.wincan = False

    def get_screenshot(self):
        """
        Creates screenshot of provided window

        Returns
        -------
        image
        """
        if self.wincan:
            import win32gui
            import win32ui
            import win32con
            wdc = win32gui.GetWindowDC(self.hwnd)
            dc_obj = win32ui.CreateDCFromHandle(wdc)
            cdc = dc_obj.CreateCompatibleDC()
            dataBitMap = win32ui.CreateBitmap()
            dataBitMap.CreateCompatibleBitmap(dc_obj, self.width, self.height)
            cdc.SelectObject(dataBitMap)
            cdc.BitBlt((0, 0), (self.width, self.height), dc_obj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)

            signedIntsArray = dataBitMap.GetBitmapBits(True)
            img = np.fromstring(signedIntsArray, dtype='uint8')
            img.shape = (self.height, self.width, 4)

            dc_obj.DeleteDC()
            cdc.DeleteDC()
            win32gui.ReleaseDC(self.hwnd, wdc)
            win32gui.DeleteObject(dataBitMap.GetHandle())

            img = img[..., :3]

            img = np.ascontiguousarray(img)

            return img
        else:
            raise ImportError("Can't use this function on this system, no pywin32 installed")

    @staticmethod
    def scr_convert(image):
        """
        Helper Function
        Converts image taken by mss().grab() to be possible for other function to work on later

        Parameters
        ----------
        image : image
            Takes mss image to get it possible to work with opencv

        Returns
        -------
        image
            Converted image to work properly with opencv
        """
        return cv.cvtColor(cv.cvtColor(np.array(image), cv.COLOR_RGB2BGR), cv.COLOR_BGR2RGB)

    def screenshot(self, region=None):
        """
        Creates screenshot with mss

        Parameters
        ----------
        region : dict
            region of capturing on screen {top, left, width, height} values represent pixels
            e.g. {'top': 160, 'left': 160, 'width': 200, 'height': 200}

        Returns
        -------
        image
            image screenshot using mss
        """
        if region is None:
            return self.scr_convert(mss().grab(mss().monitors[0]))
        if not isinstance(region, dict):
            return self.scr_convert(mss().grab(mss().monitors[0]))
        return self.scr_convert(mss().grab(region))

    def list_window_names(self):
        """
        Lists all windows that can be used
        """
        if self.wincan:
            import win32gui
            import win32ui
            import win32con

            def win_enum_handler(hwnd):
                if win32gui.IsWindowVisible(hwnd):
                    print(hex(hwnd), win32gui.GetWindowText(hwnd))
            win32gui.EnumWindows(win_enum_handler, None)
        else:
            raise ImportError("Can't use this function on this system, no pywin32 installed")
