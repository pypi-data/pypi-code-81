from PygFW import Event
import pygame

class EntityClickEvent(Event):

    def __init__(self, scene_surface):

        Event.__init__(self, scene_surface, pygame.MOUSEBUTTONDOWN)

    def executor(self, scene, event):

        for entity in scene.entities._list_:

            if entity.collides_with([event.pos]):

                entity.click(scene, event)

class EntityUnclickEvent(Event):

    def __init__(self, scene_surface):

        Event.__init__(self, scene_surface, pygame.MOUSEBUTTONUP)

    def executor(self, scene, event):

        for entity in scene.entities._list_:

            entity.un_click(scene, event)
