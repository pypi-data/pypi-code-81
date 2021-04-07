# Copyright 2020 Cognite AS
import numpy as np

from .index import Position2


class Box2(np.ndarray):
    """Box 2D, left upper and right bottom
    """

    def __new__(cls, lower_left_x, lower_left_y=None, upper_right_x=None, upper_right_y=None):
        if isinstance(lower_left_x, (list, np.ndarray)):
            if len(lower_left_x) != 4:
                raise Exception("Box can cantain only 4 values")
            input_array = np.array(lower_left_x, dtype=np.float32)
        elif upper_right_x is None and upper_right_y is None:
            input_array = np.array([lower_left_x, lower_left_y], dtype=np.float32).flatten()
        else:
            input_array = np.array([lower_left_x, lower_left_y, upper_right_x, upper_right_y], dtype=np.float32)

        if input_array[0] > input_array[2]:
            # change X value
            input_array[0], input_array[2] = input_array[2], input_array[0]
        if input_array[1] > input_array[3]:
            # change Y value
            input_array[1], input_array[3] = input_array[3], input_array[1]

        return np.asarray(input_array, dtype=np.float32).view(cls)

    @property
    def lower_left(self):
        return Position2(self[0:2])

    @property
    def lower_right(self):
        return Position2(self[2], self[1])

    @property
    def upper_left(self):
        return Position2(self[0], self[3])

    @property
    def upper_right(self):
        return Position2(self[2:4])

    def contains(self, pos):
        point = Position2(pos)
        return (
            point.x >= self.lower_left.x
            and point.x <= self.upper_right.x
            and point.y >= self.lower_left.y
            and point.y <= self.upper_right.y
        )

    def __str__(self):
        return self.lower_left + ", " + self.upper_right
