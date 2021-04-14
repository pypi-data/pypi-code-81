from PygFW.Volatile import VolatileObject
import pygame

class Event(VolatileObject):

    def __call__(self, scene, event):

        self.executor(scene, event)

    def __init__(self, scene_surface, listener, event_id: str = None):

        self.listener = listener
        self.surface = scene_surface
        self.event_id = f'<Event Object (listener={listener}, scene={scene_surface}' if event_id is None else event_id

        self.executor_maps = {}

    def executor(self, scene, event):

        for mapped_function in self.executor_maps:

            mapped_function['function'](scene, event, *mapped_function['args'], *mapped_function['kwargs'])

    def maps(self, *args, **kwargs):

        def add_function(function):

            self.executor_maps[function] = {'function': function, 'args': args, 'kwargs': kwargs}

            return function

        return add_function


def Eventifies(scene, listener=None, add=False):

    def set_executor(function):

        event = Event(scene_surface=scene, listener=listener)
        event.executor = function

        return event

    if add:

        scene.events.add(set_executor)

    return set_executor