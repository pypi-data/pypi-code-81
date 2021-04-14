from PygFW.Entity import Entity
from PygFW.Image import ImageGallery, ImageObject
from PygFW.Volatile import default_clock

class BackgroundEntity(Entity):

    def __init__(self, game_surface, background_sprites: ImageGallery, scroll: bool = True, scroll_velocity: int = -1, millisecond_scroll_interval: int=1):

        Entity.__init__(self, game_surface, background_sprites, (0, 0))

        self.scroll = scroll
        self.scroll_velocity = scroll_velocity
        self.millisecond_scroll_interval = millisecond_scroll_interval

    def draw(self):

        if self.scroll:

            if default_clock.fmilliseconds % self.millisecond_scroll_interval == 0:

                self.x_offset += self.scroll_velocity

            if self.scroll_velocity < 0:

                if self.x_offset + self.sprite.width < self.sprite.width/2:

                    self.x_offset = 0

            elif self.scroll_velocity > 0:

                if self.x_offset - self.sprite.width / 2 == 0:

                    self.x_offset = 0

            self.sprite.draw(self.scene.engine_surface.pygame_surface, self.relative_position, self.x_offset)
            self.sprite.draw(self.scene.engine_surface.pygame_surface, self.relative_position, self.x_offset + self.sprite.width)
            self.sprite.draw(self.scene.engine_surface.pygame_surface, self.relative_position, self.x_offset - self.sprite.width)

        else:

            Entity.draw(self)