from PygFW.Image import ImageGallery, ImageObject
from PygFW.Volatile import VolatileObject
from PygFW.Event import Eventifies


class Entity():

    def __init__(self, scene_surface, sprites: [ImageObject, ], spawn: [int, int], rotate_sprites=False,
                 coordinate_offset: [int, int] = (0, 0)):

        # VolatileObject.__init__(self)

        self.scene = scene_surface

        self.sprites = ImageGallery()

        if sprites:

            for sprite in sprites:

                self.sprites.add(sprite)

        self.rotate_sprites = rotate_sprites
        self.sprite_index = 0

        self.x = spawn[0]
        self.y = spawn[1]
        self.x_offset = coordinate_offset[0]
        self.y_offset = coordinate_offset[1]

        self._radius_history_x = self.x
        self._radius_history_y = self.y
        self._radius_history = []

    @property
    def absolute_position(self):

        return self.x, self.y

    @property
    def relative_x(self):

        return self.x + self.x_offset

    @property
    def relative_y(self):

        return self.y + self.y_offset

    @property
    def relative_position(self):

        return self.relative_x, self.relative_y

    @property
    def sprite(self):

        return self.sprites[self.sprite_index]

    @property
    def rect(self):

        return self.sprite.pygame_rect

    @property
    def radius(self):

        appearing_coords = []

        if self.x != self._radius_history_x or self.y != self._radius_history_y or len(self._radius_history) < 1:

            for x in range(int(self.x), int(self.x + self.sprite.width)):

                for y in range(int(self.y), int(self.y + self.sprite.height)):
                    appearing_coords.append((x, y))

        else:

            appearing_coords = self._radius_history

        return appearing_coords

    def collides_with(self, other_radius_list):

        collides = False

        for xy in other_radius_list:

            if xy in self.radius:

                collides = True

        return collides

    def draw(self):

        self.sprites[self.sprite_index].draw(self.scene.engine_surface.pygame_surface, self.relative_position)

        if self.rotate_sprites:
            self.sprites.rotate(1)

    def tick(self):

        self.update()
        self.gravity()

    def update(self):

        pass

    def gravity(self):

        pass

    def hover(self, scene, event):

        pass

    def un_hover(self, scene, event):

        pass

    def click(self, scene, event):

        pass

    def left_click(self, scene, event):

        pass

    def right_click(self, scene, event):

        pass

    def un_click(self, scene, event):

        pass

    def un_left_click(self, scene, event):

        pass

    def un_right_click(self, scene, event):

        pass

    def go_towards(self, coordinates, drift_velocity=1, step_velocity=1, collision_check=False):

        target_x, target_y = coordinates

        if (collision_check and True not in [self.collides_with(other_entity.radius) for other_entity in
                                            self.scene.entities._list_]) or not collision_check:

            if target_x < self.x:

                self.x -= step_velocity

            elif target_x > self.x:

                self.x += step_velocity

            if target_y < self.y:

                self.y -= drift_velocity

            elif target_y > self.y:

                self.y += drift_velocity