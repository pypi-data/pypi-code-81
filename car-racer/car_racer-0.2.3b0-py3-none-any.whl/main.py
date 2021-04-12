import json
import math
import traceback
import pyglet
import car_racer.config as config
from os import listdir
from os.path import isdir, isfile, join
from pyglet import clock
from pyglet.window import key
from pyglet.gl import glTranslatef
from car_racer.track import Track
from car_racer.car import Car
from car_racer.tictoc import timed_function, timed_function_statistics, tic_toc


keys = key.KeyStateHandler()
turn = 0
replay_iteration = 0
sleep_counter = 0
label = None


@timed_function()
def on_draw(interval):
    if config.replay:
        global replay_iteration
        for car in config.replay_cars:
            car.do_replay(replay_iteration, car.follow)
        replay_iteration += 1
        config.window.clear()
    else:
        handle_car_stop()
        key_handler()
        config.window.clear()
        if config.car.finish < 0:
            config.car.process_next_frame()
    config.batch.draw()


@timed_function()
def handle_car_stop():
    global sleep_counter, label
    if config.car.stop and sleep_counter < config.frames_per_second * 3:
        if sleep_counter % config.frames_per_second == 0:
            seconds_left = 3 - math.ceil(sleep_counter / config.frames_per_second)
            label.text = str(seconds_left)
            label.x = config.car.car.x
            label.y = config.car.car.y
        sleep_counter += 1
    elif config.car.stop:
        label.text = ""
        sleep_counter = 0
        glTranslatef(config.car.car.x, config.car.car.y, 0)
        config.car = Car(config.track)


def key_handler():
    # exit
    if keys[key.ESCAPE]:
        pyglet.app.exit()
    if not config.replay:
        # acceleration and breaking
        if keys[key.UP] == keys[key.DOWN]:
            config.car.rolling = True
            config.car.accelerate = 0
        elif keys[key.UP]:
            config.car.accelerate = 0.03
            config.car.rolling = False
        elif keys[key.DOWN]:
            config.car.accelerate = -0.1
            config.car.rolling = False
        # turning
        if keys[key.RIGHT] == keys[key.LEFT]:
            config.car.rotate(0)
        elif keys[key.RIGHT]:
            config.car.rotate(1)
        elif keys[key.LEFT]:
            config.car.rotate(-1)
        if keys[key.SPACE]:
            config.car.drifting = True
        else:
            config.car.drifting = False
        # restart
        if keys[key.R] and config.car.finish > 0:
            glTranslatef(config.car.car.x, config.car.car.y, 0)
            config.car = Car(config.track)


def start_game():
    config.window.push_handlers(keys)
    width, height = config.window.get_size()
    glTranslatef((width/2), (height/2), 0)
    clock.schedule_interval(on_draw, 1 / config.frames_per_second)
    pyglet.app.run()


def start_replay(replay_files):
    if isdir(replay_files):
        files = [f for f in listdir(replay_files) if isfile(join(replay_files, f))]
        if len(files) > 0:
            try:
                load_replay_files(replay_files, files)
                start_game()
            except Exception:
                traceback.print_stack()
                raise Exception("replay format not valid")
        else:
            for directory in listdir(replay_files):
                files = [f for f in listdir(f"{replay_files}/{directory}") if isfile(join(replay_files, directory, f))]
                if len(files) > 0:
                    try:
                        load_replay_files(f"{replay_files}/{directory}", files)
                        decide_follow_car()
                        start_game()
                    except Exception:
                        traceback.print_stack()
                        raise Exception("replay format not valid")
                else:
                    raise Exception("no replays available")
    else:
        raise Exception("replay directory doesn't exist or is no directory")


def load_replay_files(replay_files, files):
    track_file = open(f"{replay_files}/{files[0]}", "r")
    track_info = json.load(track_file)
    config.track = Track(track_info["track"]["length"], track_info["track"]["seed"], track_info["track"]["corners"])
    for file in files:
        config.replay_cars.append(Car(config.track))
        config.replay_cars[-1].load_replay(f"{replay_files}/{file}")
    config.replay = True


def decide_follow_car():
    follow_car: Car = None
    for car in config.replay_cars:
        if (follow_car is None or
                car.replay["distance"] > follow_car.replay["distance"] or
                (car.replay["distance"] == follow_car.replay["distance"] and
                 car.replay["time"] < follow_car.replay["time"])):
            follow_car = car
    follow_car.follow = True


def main(mode, length=1, seed=0, chance=30, max_angle=90, replay_folder="replays"):
    global label
    pyglet.gl.glClearColor(1, 0.7, 0.5, 1)
    config.track = Track(length, seed, {"chance": chance, "max_angle": max_angle})

    if mode == 0:
        config.car = Car(config.track)
        label = pyglet.text.Label("",
                                  font_name='Arial',
                                  font_size=36, color=(0, 0, 0, 255),
                                  x=config.car.car.x, y=config.car.car.y, group=config.text_group, batch=config.batch)
        start_game()
    if mode == 1:
        start_replay(replay_folder)


if __name__ == '__main__':
    main(1)
    for k in tic_toc.keys():
        print(f"{k}: {timed_function_statistics(k)}; executions: {len(tic_toc[k])}")
