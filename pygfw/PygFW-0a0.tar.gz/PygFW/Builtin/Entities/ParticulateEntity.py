from PygFW.Entity import Entity
from random import randint
from PygFW import Eventifies

class ParticulateEntity(Entity):

    def __init__(self, scene, sprites, spawn, fall_velocity: [int, int] = (0, 0), wind_velocity: [0, 0] = (0, 0) , justify_existence: bool = True, spawn_radius: [int, int, int, int]=(0, 50, 0, 50), rumble: [int, int]= (-2, 2), spawn_scale: [int, int, int, int] = None, random_scale: [int, int]=(1, 1)):

        Entity.__init__(self, scene, sprites, spawn)

        self.fall_velocity = fall_velocity
        self.wind_velocity = wind_velocity

        self.justify_existence = justify_existence
        self.random_scale = random_scale

        self.a_radical_rumble = rumble[0]
        self.radical_rumble = rumble[1]

        self.a_radical_x = spawn_radius[0]
        self.radical_x = spawn_radius[1]

        self.a_radical_y = spawn_radius[2]
        self.radical_y = spawn_radius[3]

        if spawn_scale:

            self.sprite.change_scale(spawn_scale)

        self.x, self.y = self.calculate_random_spawn()

    def calculate_random_spawn(self):

        return randint(self.a_radical_x, self.radical_x), randint(self.a_radical_y, self.radical_y)

    def rumble(self, a_radical_rumble, radical_rumble):

        self.sprite.change_rotation(randint(a_radical_rumble, radical_rumble))

    def tick(self):

        self.rumble(self.a_radical_rumble, self.radical_rumble)
        self.gravity()
        self.update()

        if self.random_scale:

            self.rescale()

    def gravity(self):

        self.y += randint(*self.fall_velocity)
        self.x += randint(*self.wind_velocity)

    def update(self):

        if self.justify_existence:

            if not 0 < self.y < self.scene.engine_surface.window_height or not 0 < self.x < self.scene.engine_surface.window_width:

                @Eventifies(scene=self.scene, listener=None)
                def remove_self(scene, event):
                    scene.entities.remove(scene.entities.get_tag(self), True)

                self.scene.engine_surface.single_events.add(remove_self)

    def rescale(self):

        self.sprite.change_scale((randint(self.random_scale[0], self.random_scale[1]), randint(self.random_scale[2], self.random_scale[3])))

