import pyglet

window = pyglet.window.Window(800, 800)
wall_group = pyglet.graphics.OrderedGroup(0)
car_group = pyglet.graphics.OrderedGroup(1)
text_group = pyglet.graphics.OrderedGroup(2)
segments = []
batch = pyglet.graphics.Batch()
frames_per_second = 60
draw_distance = 10
track = None
car = None
replay_cars = []
replay = False
camera_position = [0, 0]
max_speed = 18

