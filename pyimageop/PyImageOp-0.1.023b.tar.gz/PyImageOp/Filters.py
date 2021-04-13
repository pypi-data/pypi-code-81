import cv2 as cv
import numpy as np
from scipy.interpolate import UnivariateSpline


class Filters:
    @staticmethod
    def grayscale(haystack_img):
        """
        Turns provided image into grayscale

        Parameters
        ----------
        haystack_img : image
            image to be turned to grayscale

        Returns
        -------
        image
            image gray scaled
        """
        return cv.cvtColor(haystack_img, cv.COLOR_BGR2GRAY)

    @staticmethod
    def vintage_filter(haystack_img):
        """
        Adds vintage filter into image

        Parameters
        ----------
        haystack_img : image
            image to be edited

        Returns
        -------
        image
            image with applied filter
        """
        gray = cv.cvtColor(haystack_img, cv.COLOR_BGR2GRAY)
        normalized_gray = np.array(gray, np.float32) / 255
        sepia = np.ones(haystack_img.shape)
        sepia[:, :, 0] *= 176  # B
        sepia[:, :, 1] *= 235  # G
        sepia[:, :, 2] *= 255  # R
        sepia[:, :, 0] *= normalized_gray  # B
        sepia[:, :, 1] *= normalized_gray  # G
        sepia[:, :, 2] *= normalized_gray  # R
        return np.array(sepia, np.uint8)

    @staticmethod
    def blurred_filter(haystack_img):
        """
        Adds GaussianBlur filter on image

        Parameters
        ----------
        haystack_img : image
            image to be edited

        Returns
        -------
        image
            image with applied filter
        """
        return cv.GaussianBlur(haystack_img, (35, 35), 0)

    @staticmethod
    def emboss_filter(haystack_img):
        """
        Adds emboss filter on image

        Parameters
        ----------
        haystack_img : image
            image to be edited

        Returns
        -------
        image
            image with applied filter
        """
        kernel = np.array([[0, -1, -1],
                           [1, 0, -1],
                           [1, 1, 0]])
        return cv.filter2D(haystack_img, -1, kernel)

    @staticmethod
    def sharpen_filter(haystack_img):
        """
        Adds sharpen filter on image

        Parameters
        ----------
        haystack_img : image
            image to be edited

        Returns
        -------
        image
            image with applied filter
        """
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        return cv.filter2D(haystack_img, -1, kernel)

    @staticmethod
    def bilateral_filter(haystack_img):
        """
        Adds bilateral filter on image

        Parameters
        ----------
        haystack_img : image
            image to be edited

        Returns
        -------
        image
            image with applied filter
        """
        return cv.bilateralFilter(haystack_img, 9, 75, 75)

    @staticmethod
    def brightness_control(haystack_img, level=20):
        """
        Change the brightness level of image

        Parameters
        ----------
        haystack_img : image
            image to be edited
        level : int
            int to how much bright up the image

        Returns
        -------
        image
            image with applied filter
        """
        return cv.convertScaleAbs(haystack_img, beta=level)

    @staticmethod
    def _spread_lookup_table(x, y):
        """
        Helper function for cold and worm image

        Parameters
        ----------
        x : array_like
        y : array_like

        Returns
        -------
        array_like
        """
        spline = UnivariateSpline(x, y)
        return spline(range(256))

    @staticmethod
    def cold_image(image):
        """
        Make image colder

        Parameters
        ----------
        image : image
            image to be edited

        Returns
        -------
        image
            image with applied filter
        """
        increaseLookupTable = Filters._spread_lookup_table([0, 64, 128, 256], [0, 80, 160, 256])
        decreaseLookupTable = Filters._spread_lookup_table([0, 64, 128, 256], [0, 50, 100, 256])
        red_channel, green_channel, blue_channel = cv.split(image)
        red_channel = cv.LUT(red_channel, increaseLookupTable).astype(np.uint8)
        blue_channel = cv.LUT(blue_channel, decreaseLookupTable).astype(np.uint8)
        return cv.merge((red_channel, green_channel, blue_channel))

    @staticmethod
    def warm_image(image):
        """
        Make image warmer

        Parameters
        ----------
        image : image
            image to be edited

        Returns
        -------
        image
            image with applied filter
        """
        increaseLookupTable = Filters._spread_lookup_table([0, 64, 128, 256], [0, 80, 160, 256])
        decreaseLookupTable = Filters._spread_lookup_table([0, 64, 128, 256], [0, 50, 100, 256])
        red_channel, green_channel, blue_channel = cv.split(image)
        red_channel = cv.LUT(red_channel, decreaseLookupTable).astype(np.uint8)
        blue_channel = cv.LUT(blue_channel, increaseLookupTable).astype(np.uint8)
        return cv.merge((red_channel, green_channel, blue_channel))

    @staticmethod
    def edges_draw(image, threshold1=10, threshold2=20):
        """
        Detect and draw edges on image

        Parameters
        ----------
        image : image
            image to detect edges from
        threshold1 : int
             min value of probability to draw edge
        threshold2 : int
             max value of probability to draw edge

        Returns
        -------
        image
            image of detected edges
        """
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        edges = cv.Canny(gray, threshold1, threshold2)
        lines = cv.HoughLinesP(edges, 1, np.pi / 180, 30, maxLineGap=250)
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv.line(image, (x1, y1), (x2, y2), (0, 0, 128), 1)
        return edges

    @staticmethod
    def circles_draw(image, min_radius=5, max_radius=30):
        """
        Detect and draw circles on image

        Parameters
        ----------
        image : image
            image to detect circles from
        min_radius : int
            min radius for circle to be drawn
        max_radius : int
            max radius for circle to be drawn

        Returns
        -------
        image
            image of detected circles
        """
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        # Blur the image to reduce noise
        img_blur = cv.medianBlur(gray, 5)
        # Apply hough transform on the image
        circles = cv.HoughCircles(img_blur, cv.HOUGH_GRADIENT, 1, image.shape[0] / 40, param1=300, param2=15,
                                  minRadius=min_radius, maxRadius=max_radius)
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                cv.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 2)
                cv.circle(image, (i[0], i[1]), 2, (0, 0, 255), 3)
        return image

    @staticmethod
    def resize_image(image, percentage=50, height=None, width=None):
        """
        Resize the provided image

        Parameters
        ----------
        image : image
            image to be edited
        percentage : int
            percentage that the image has to be its size
        height : int
            height of image
        width : int
            width of image

        Returns
        -------
        image
            resized image
        """
        # TODO test all parameters

        if height is None and width is None:
            image = cv.resize(image, (0, 0), fx=(percentage / 100), fy=(percentage / 100))
        else:
            if height is None:
                scale = int(image.shape[1]) / int(image.shape[0])
                image = cv.resize(image, (0, 0), fx=width, fy=(width * scale))
            if width is None:
                scale = int(image.shape[1]) / int(image.shape[0])
                image = cv.resize(image, (0, 0), fx=(height * scale), fy=height)
            else:
                image = cv.resize(image, (0, 0), fx=width, fy=height)
        return image

    @staticmethod
    def invert_image(image):
        """
        Inverts colors on image

        Parameters
        ----------
        image : image
            image to be edited

        Returns
        -------
        image
            image with inverted colors
        """
        return cv.bitwise_not(image)

    @staticmethod
    def only_color(image, color):
        """
        Display only one color detected

        Parameters
        ----------
        image : image
            image to be edited
        color : string
            str which color to be shown possible [white, red, green, blue, yellow, purple, orange, gray]

        Returns
        -------
        image
            image with only one color displayed
        """
        hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        color_l = color.lower()
        color_dict_HSV = {
                          'white': [[180, 18, 255], [0, 0, 231]],
                          'red1': [[180, 255, 255], [159, 50, 70]],
                          'red2': [[9, 255, 255], [0, 50, 70]],
                          'green': [[89, 255, 255], [36, 50, 70]],
                          'blue': [[128, 255, 255], [90, 50, 70]],
                          'yellow': [[35, 255, 255], [25, 50, 70]],
                          'purple': [[158, 255, 255], [129, 50, 70]],
                          'orange': [[24, 255, 255], [10, 50, 70]],
                          'gray': [[180, 18, 230], [0, 0, 40]]
                         }

        if color_l not in color_dict_HSV and color_l != 'red':
            raise TypeError('Provided values for color can be only {}'.format([i for i in color_dict_HSV]))
        if color_l == 'red':
            mask = cv.inRange(hsv, np.array(color_dict_HSV['red2'][1]), np.array(color_dict_HSV['red2'][0]))
            mask2 = cv.inRange(hsv, np.array(color_dict_HSV['red1'][1]), np.array(color_dict_HSV['red1'][0]))
            mask = mask + mask2
            res = cv.bitwise_and(image, image, mask=mask)
            return res
        else:
            mask = cv.inRange(hsv, np.array(color_dict_HSV[color_l][1]), np.array(color_dict_HSV[color_l][0]))
            res = cv.bitwise_and(image, image, mask=mask)
            return res

    @staticmethod
    def noise(image, noise_type):
        """
        Adds noise on image

        Parameters
        ----------
        image : image
            image on which add noise
        noise_type : string
            str what noise to add possible: [gauss, s&p, speckle]

        Returns
        -------
        image
            image with applied noise
        """
        if noise_type != 'gauss' and noise_type != 's&p' and noise_type != 'speckle':
            raise TypeError("Noises types allowed: [gauss, s&p, speckle]")
        if noise_type == 'gauss':
            gauss = np.random.normal(0, 1, image.size)
            gauss = gauss.reshape(image.shape[0], image.shape[1], image.shape[2]).astype('uint8')
            return cv.add(image, gauss)

        if noise_type == "s&p":
            s_vs_p = 0.5
            amount = 0.004
            out = np.copy(image)
            # Salt mode
            num_salt = np.ceil(amount * image.size * s_vs_p)
            coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape]
            out[coords] = 1

            # Pepper mode
            num_pepper = np.ceil(amount * image.size * (1. - s_vs_p))
            coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape]
            out[coords] = 0
            return out

        if noise_type == "speckle":
            row, col, ch = image.shape
            gauss = np.random.randn(row, col, ch)
            gauss = gauss.reshape(row, col, ch)
            noisy = image + image * gauss
            return noisy

    @staticmethod
    def inverted_edge(image, threshold1=10, threshold2=20):
        """
        Detects edges and inverts its colors

        Parameters
        ----------
        image : image
            image to be edited
        threshold1 : int
            min value of probability to draw edge
        threshold2 : int
            max value of probability to draw edge

        Returns
        -------
        image
            image with applied invert filter on edge draw
        """
        return Filters.invert_image(Filters.edges_draw(image, threshold1, threshold2))
