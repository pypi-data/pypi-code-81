from PygFW.Entity import Entity
from PygFW.Event import Eventifies
from PygFW.Image import ImageGallery, ImageObject
from PygFW.Volatile import default_clock
import pygame

class ButtonEntity(Entity):

    def __init__(self, scene_surface, static_sprite, spawn, highlight_sprite=None, click_sprite=None):

        Entity.__init__(self, scene_surface, ImageGallery(), spawn)

        self.static_sprite = static_sprite
        self.highlight_sprite = highlight_sprite if highlight_sprite else static_sprite
        self.click_sprite = click_sprite if click_sprite else static_sprite

        self.operating_sprite = self.static_sprite

        self.clicked = False

    @property
    def sprite(self):

        return self.operating_sprite

    def draw(self):

        self.operating_sprite.draw(self.scene.engine_surface.pygame_surface, self.relative_position)

    def tick(self):

        self.update()

    def update(self):

        mouse = pygame.mouse.get_pos()

        if self.collides_with([mouse]) and not self.clicked:

            self.operating_sprite = self.highlight_sprite

        elif self.clicked:

            self.operating_sprite = self.click_sprite

        else:

            self.operating_sprite = self.static_sprite

    def click(self, scene, event):

        self.clicked = True
        self.operating_sprite = self.click_sprite

        self.draw()
        pygame.display.update()

    def un_click(self, scene, event):

        self.clicked = False
        self.operating_sprite = self.static_sprite
