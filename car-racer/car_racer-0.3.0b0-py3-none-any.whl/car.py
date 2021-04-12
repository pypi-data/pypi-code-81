import json
import math
import time
import pyglet
import dotmap
import car_racer.config as config
from os import mkdir
from shapely.geometry import Polygon
from pyglet.gl import glTranslatef
from car_racer.tictoc import timed_function
from os.path import join, dirname, isdir


class Car:
    def __init__(self, track):
        script_dir = dirname(__file__)
        path = join(script_dir, 'car.png')
        car_image = pyglet.image.load(path)
        car_image.anchor_x = int(car_image.width / 2)
        car_image.anchor_y = int(car_image.height / 2)
        self.track = track
        self.car = pyglet.sprite.Sprite(car_image, group=config.car_group, batch=config.batch, x=car_image.width)
        self.car.rotation = track.segments[0].coordinates[0].angle + 90
        self.accelerate = 0
        self.previous_direction = [dotmap.DotMap(x=0, y=0, rotation=self.car.rotation)]
        self.rolling = True
        self.drifting = False
        self.speed = 0
        self.speed_factor = 1
        self.speed_label = pyglet.text.Label(f"{round(self.speed * 21.6, 2)} km/h",
                                             font_name='Arial',
                                             font_size=12, color=(0, 0, 0, 255),
                                             x=self.car.x + config.window.width//2 - 50,
                                             y=self.car.y - config.window.height//2 + 100,
                                             anchor_x='right', anchor_y='bottom',
                                             group=config.text_group, batch=config.batch)
        self.finish_label = pyglet.text.Label("",
                                              font_name='Arial',
                                              font_size=12, color=(0, 0, 0, 255),
                                              x=self.car.x, y=self.car.y,
                                              anchor_x='center', anchor_y='center',
                                              group=config.text_group, batch=config.batch)
        self.steer = 0
        self.segment = 0
        self.distance = 0
        self.checkpoints = []
        self.finish = -1
        self.stop = False
        self.started = False
        self.follow = False
        self.timer = time.monotonic()
        self.replay = {"track": {"length": self.track.length,
                                 "seed": self.track.seed,
                                 "corners": self.track.corners},
                       "frames": [],
                       "distance": 0,
                       "time": -1}

    def __del__(self):
        self.car.delete()
        self.speed_label.delete()
        self.finish_label.delete()

    @timed_function()
    def process_next_frame(self):
        if not self.stop:
            self.calculate_speed()
            self.calculate_position()
            if self.started:
                self.replay["frames"].append((self.car.x, self.car.y, self.car.rotation))

    @timed_function()
    def rotate(self, factor):
        if self.stop or self.finish > 0:
            return
        if factor == 0:
            self.steer = 0
            self.speed_factor = 1
        else:
            self.speed_factor = 0.9
            self.steer += (1 / config.frames_per_second) * factor

        if abs(self.steer) > 1:
            self.steer = 1 * factor

        if self.drifting:
            self.speed_factor = 0.8
            self.car.rotation += factor + (self.steer * 3)
        else:
            self.car.rotation += factor + self.steer

    @timed_function()
    def calculate_speed(self):
        if self.rolling and self.speed != 0:
            self.speed += (abs(self.speed) / self.speed) / -50
            if self.speed < 0.05:
                self.speed = 0
                self.accelerate = 0
        elif not self.rolling:
            if not self.started:
                self.timer = time.monotonic()
                self.started = True
            self.speed += self.accelerate
            if self.speed >= config.max_speed * self.speed_factor:
                if self.speed_factor < 1:
                    self.speed -= self.accelerate * 1.5
                else:
                    self.speed = config.max_speed
            elif self.speed <= -2:
                self.speed = -2

        self.speed_label.text = f"{round(self.speed * 21.6, 2)} km/h"

    @timed_function()
    def calculate_position(self):
        if self.speed == 0:
            return
        y = self.speed * math.cos(math.radians(self.car.rotation))
        x = self.speed * math.sin(math.radians(self.car.rotation))

        for i in range(len(self.previous_direction)):
            direction = self.previous_direction[i]
            self.car.x += (direction.x * (i + 1) / 30)
            self.car.y += (direction.y * (i + 1) / 30)
        self.car.x += (x * 0.5)
        self.car.y += (y * 0.5)

        self.previous_direction.append(dotmap.DotMap(x=x, y=y, rotation=self.car.rotation))
        if len(self.previous_direction) > 5:
            self.previous_direction.pop(0)

        config.camera_position[0] -= x
        config.camera_position[1] -= y
        glTranslatef(-x, -y, 0)
        self.speed_label.x += x
        self.speed_label.y += y
        self.calculate_checkpoint()
        self.set_segments_visible()
        if self.calculate_collision():
            self.speed = 0
            self.stop = True
            self.replay["distance"] = self.segment
            self.handle_stop()

    @timed_function()
    def calculate_checkpoint(self):
        if len(self.track.segments) > self.segment + 1:
            segment = self.track.segments[self.segment + 1]
            if self.rect_distance(segment.start, Polygon(self.get_car_boundaries())) == 0:
                self.segment += 1
                self.checkpoints.append(time.monotonic() - self.timer)
        else:
            segment = self.track.segments[self.segment]
            if self.rect_distance(segment.end, Polygon(self.get_car_boundaries())) == 0:
                self.finish = time.monotonic() - self.timer
                self.finish_label.text = f"you finished in {round(self.finish, 2)} seconds - press R to restart"
                self.replay["distance"] = self.segment
                self.finish_label.x = self.car.x
                self.finish_label.y = self.car.y
                self.handle_stop()

    @timed_function()
    def set_segments_visible(self):
        for segment in self.track.segments:
            if segment.id < self.segment + config.draw_distance:
                segment.group.visible = True
            else:
                segment.group.visible = False

    @timed_function()
    def calculate_collision(self):
        segment = self.track.segments[self.segment]
        car_boundaries = self.get_car_boundaries()
        car_polygon = Polygon(car_boundaries)
        for wall in segment.wall_lines:
            if self.rect_distance(wall, car_polygon) == 0:
                return True
        return False

    @timed_function()
    def rect_distance(self, obj, car_polygon):
        return car_polygon.distance(obj)

    @timed_function()
    def get_car_boundaries(self):
        rotation_radians = math.radians(self.car.rotation)
        img = self.car._texture
        x1 = -img.anchor_x
        y1 = -img.anchor_y
        x2 = x1 + img.width
        y2 = y1 + img.height
        x = self.car._x
        y = self.car._y
        cos_rotation = math.cos(rotation_radians)
        sin_rotation = math.sin(rotation_radians)
        ax = x1 * cos_rotation - y1 * sin_rotation + x
        ay = x1 * sin_rotation + y1 * cos_rotation + y
        bx = x2 * cos_rotation - y1 * sin_rotation + x
        by = x2 * sin_rotation + y1 * cos_rotation + y
        cx = x2 * cos_rotation - y2 * sin_rotation + x
        cy = x2 * sin_rotation + y2 * cos_rotation + y
        dx = x1 * cos_rotation - y2 * sin_rotation + x
        dy = x1 * sin_rotation + y2 * cos_rotation + y

        return [(ax, ay), (bx, by), (cx, cy), (dx, dy)]

    @timed_function()
    def handle_stop(self):
        self.replay["time"] = time.monotonic() - self.timer
        if not isdir("replays"):
            mkdir("replays")
        track_name = f"{self.track.length}_{self.track.seed}_{self.track.corners['chance']}_{self.track.corners['max_angle']}"
        if not isdir(f"replays/{track_name}"):
            mkdir(f"replays/{track_name}")
        file_name = f"replays/{track_name}/car_replay_{time.time()}.json"
        f = open(file_name, "w")
        json.dump(self.replay, f)
        f.close()

    @timed_function()
    def load_replay(self, replay_file):
        f = open(replay_file, "r")
        replay = json.load(f)
        track = replay["track"]
        if self.track.length == track["length"] and self.track.seed == track["seed"] and self.track.corners == track["corners"]:
            self.replay = replay
            self.speed_label.text = ""

    @timed_function()
    def do_replay(self, iteration, follow=False):
        if len(self.replay["frames"]) > iteration:
            x = self.replay["frames"][iteration][0]
            y = self.replay["frames"][iteration][1]
            if follow:
                glTranslatef(self.car.x - x, self.car.y - y, 0)
            self.car.x = x
            self.car.y = y
            self.car.rotation = self.replay["frames"][iteration][2]
