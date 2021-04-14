from PygFW.Event import Event
import pygame

class QuitEvent(Event):

    def __init__(self, surface):

        Event.__init__(self, surface, pygame.QUIT, 'quit_event')

    def executor(self, scene, event):

        scene.run = False