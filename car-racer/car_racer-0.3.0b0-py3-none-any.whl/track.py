import math
import random
import pyglet
import car_racer.config as config
from shapely.geometry import LineString
from pyglet import shapes

factors = [1, -1]


class Coordinate:
    def __init__(self, x, y, angle, wall_lines, segment_group):
        self.x = x
        self.y = y
        self.angle = angle
        radian_angle_left = math.radians(angle - 90)
        radian_angle_right = math.radians(angle + 90)
        self.left_x = x + (80 * math.cos(radian_angle_left))
        self.left_y = y + (80 * math.sin(radian_angle_left))
        self.right_x = x + (80 * math.cos(radian_angle_right))
        self.right_y = y + (80 * math.sin(radian_angle_right))
        self.drawing = shapes.Rectangle(x=self.left_x, y=self.left_y, width=2, height=160,
                                        group=segment_group, batch=config.batch)
        self.left_wall = shapes.Rectangle(x=self.left_x, y=self.left_y, width=1, height=2,
                                          color=(100, 100, 100), group=segment_group, batch=config.batch)
        self.right_wall = shapes.Rectangle(x=self.right_x, y=self.right_y, width=1, height=2,
                                           color=(100, 100, 100), group=segment_group, batch=config.batch)
        wall_lines.append(LineString([(self.left_x, self.left_y), (self.left_x, self.left_y)]))
        wall_lines.append(LineString([(self.right_x, self.right_y), (self.right_x, self.right_y)]))
        self.drawing.rotation = -angle


class Segment:
    def __init__(self, number, corners, segment=None):
        self.id = number
        self.coordinates = []
        self.wall_lines = []
        self.group = pyglet.graphics.Group(parent=config.wall_group)
        self.start = None
        self.end = None
        self.corners = corners
        if segment is None:
            self.angle = 0
            if random.randint(0, 100) > 100 - self.corners["chance"]:
                self.angle = random.uniform(0, self.corners["max_angle"])
        else:
            additional_angle = 0
            if random.randint(0, 100) > 100 - self.corners["chance"]:
                additional_angle = random.uniform(0, self.corners["max_angle"])
            self.angle = segment.angle + (additional_angle * factors[random.randint(0, 1)])

        self.length = random.randint(100, 200)

        if segment is None:
            self.angle_delta = self.angle / self.length
            self.set_coordinates(0, Coordinate(0, 0, 0, self.wall_lines, self.group))
        else:
            self.angle_delta = (self.angle - segment.angle) / self.length
            self.set_coordinates(segment.angle, segment.coordinates[-1])

    def set_coordinates(self, start_angle, start_coordinate):
        self.coordinates.append(start_coordinate)
        current_angle = start_angle
        for i in range(0, self.length):
            current_angle += self.angle_delta
            self.coordinates.append(self.calculate_next_coordinate(current_angle))

    def calculate_next_coordinate(self, angle):
        radian_angle = math.radians(angle)
        x = self.coordinates[-1].x + math.cos(radian_angle)
        y = self.coordinates[-1].y + math.sin(radian_angle)

        start = self.coordinates[0]
        end = self.coordinates[-1]
        self.start = LineString([(start.left_x, start.left_y), (start.right_x, start.right_y)])
        self.end = LineString([(end.left_x, end.left_y), (end.right_x, end.right_y)])

        return Coordinate(x, y, angle, self.wall_lines, self.group)


class Track:
    def __init__(self, length, seed, corners):
        self.segments = []
        self.length = 0
        self.corners = corners
        self.seed = seed
        random.seed(seed)
        number = 0
        while self.length < length:
            self.add_segment(number)
            number += 1

    def add_segment(self, number):
        if len(self.segments) == 0:
            segment = Segment(number, self.corners)
        else:
            segment = Segment(number, self.corners, self.segments[-1])
        self.segments.append(segment)
        self.length += segment.length
