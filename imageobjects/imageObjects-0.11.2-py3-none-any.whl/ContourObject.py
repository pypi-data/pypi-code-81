from vectorObjects.DefinedVectors import Vector2D
from shapely.geometry import Polygon
import numpy as np
import cv2


class ContourObject:
    def __init__(self, contour):
        """
        cv2 contours are produced as np.int32 numpy.ndarrays rather than objects that have a set of attributes. Whilst
        this is over kill for simple processes, it can be useful for more complex processes to re-use logic so this
        class constructs an object that contains those processes and attributes

        :param contour: A contour from open cv python
        :type contour: numpy.ndarray
        """
        self.contour = contour

    def __repr__(self):
        """
        Return for debugging
        """
        return f"{self.area}"

    def __str__(self):
        """
        Print return for code readability
        """
        return f"Area: {self.area}, Left: {self.left}, Right {self.right}, Top, {self.top}, Bottom {self.bottom}"

    @property
    def x_list(self):
        """
        All x coordinates from each point in the list of points that made up the contour
        """
        return [cord.x for cord in self.xy_list]

    @property
    def y_list(self):
        """
        All y coordinates from each point in the list of points that made up the contour
        """
        return [cord.y for cord in self.xy_list]

    @property
    def min_x(self):
        """
        Min x position found in all coordinates
        """
        return min(self.x_list)

    @property
    def max_x(self):
        """
        Max x position found in all coordinates
        """
        return max(self.x_list)

    @property
    def min_y(self):
        """
        Min y position found in all coordinates
        """
        return min(self.y_list)

    @property
    def max_y(self):
        """
        Max y position found in all coordinates
        """
        return max(self.y_list)

    @property
    def left(self):
        """
        Left most point
        """
        return Vector2D(self.min_x, np.mean([cord.y for cord in self.xy_list if cord.x == self.min_x]))

    @property
    def right(self):
        """
        Right most point
        """
        return Vector2D(self.max_x, np.mean([cord.y for cord in self.xy_list if cord.x == self.max_x]))

    @property
    def top(self):
        """
        Top most point
        """
        return Vector2D(np.mean([cord.x for cord in self.xy_list if cord.y == self.min_y]), self.min_y)

    @property
    def bottom(self):
        """
        Bottom most point
        """
        return Vector2D(np.mean([cord.x for cord in self.xy_list if cord.y == self.max_y]), self.max_y)

    @property
    def width(self):
        """
        The width of a contour calculated as max X minus min X coordinate position
        """
        return self.max_x - self.min_x

    @property
    def height(self):
        """
        The height of a contour calculated as max X minus min X coordinate position
        """
        return self.max_y - self.min_y

    @property
    def moments(self):
        """
        The cv2 moments of a given contour
        """
        return cv2.moments(self.contour)

    @property
    def area(self):
        """
        The area of a contour
        """
        return cv2.contourArea(self.contour)

    @property
    def gradient(self):
        """
        The gradient of a contour
        """
        return [(self.max_y - self.min_y) / self.max_x - self.min_x]

    @property
    def xy_list(self):
        """
        A list of points from the contour in list[Point] type
        """
        return [Vector2D(x, y) for cord in self.contour for (x, y) in cord]

    @property
    def bounding_box_points(self):
        """
        Extract the bounding box from a given contour and then return these points as a list, as well as the min and max
        of the x and y points.

        :return: Bounding box points
        :rtype: list
        """
        x_list = [point[0] for point in cv2.boxPoints(cv2.minAreaRect(self.contour))]
        y_list = [point[1] for point in cv2.boxPoints(cv2.minAreaRect(self.contour))]
        return [[x, y] for x, y in zip(x_list, y_list)]

    def as_polygon(self):
        """
        If working with geo-spatial images, we may wish to return a contour as a polygon. This will return a Shapely
        Polygon class from the current ContourObject

        :return: A shapely Polygon
        :rtype: Polygon
        """
        xy_list = self.xy_list
        assert len(xy_list) > 3, f"A polygon Requires a minimum of three points yet was passed {len(xy_list)}"
        return Polygon([cord.x, cord.y] for cord in xy_list)

    @property
    def centroid(self):
        """
        The centroid of the contour in terms of [x, y]
        """
        return Vector2D(int(self.moments['m10'] / self.moments['m00']), int(self.moments['m01'] / self.moments['m00']))

    def scale(self, scale):
        """
        To scale a contour, translate it to the origin by subtracting the centroid and then multiply all positions by a
        scalar. Then just move it back to its original position by adding the distance that was taken away. This is then
        returned as a standard np.int32

        :param scale: float scalar to multiplier the contour by
        :type scale: float

        :return: A scaled contour
        :rtype :numpy.ndarray
        """
        return (((self.contour - self.centroid) * scale).astype(np.int32) + self.centroid).astype(np.int32)

    def draw_contour(self, image, bgr_colour=(180, 180, 180), width=-1):
        """
        Draw the current contour on an image
        """
        if isinstance(image, np.ndarray):
            cv2.drawContours(image, [self.contour], 0, bgr_colour, width)
        else:
            cv2.drawContours(image.image, [self.contour], 0, bgr_colour, width)

    def draw_line_of_best_fit(self, image, colour=(180, 180, 180), width=1):
        """
        Draw a line of best fit on the image

        Adapted from: https://stackoverflow.com/questions/14184147/detect-lines-opencv-in-object
        """
        [vx, vy, x, y] = cv2.fitLine(self.contour, cv2.DIST_L2, 0, 0.1, 0.01)
        y_min = int((-x * vy / vx) + y)
        y_max = int(((image.width - x) * vy / vx) + y)

        try:
            cv2.line(image.image, (0, y_min), (image.width - 1, y_max), colour, width)
        except OverflowError:
            print("draw_line_of_best_fit ran into an infinity problem - unable to process")
