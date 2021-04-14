from PygFW.Cake import Cake
from PygFW.Scene import Scene
from PygFW.Volatile import VolatileObject, default_clock
from PygFW.Image import ImageBank
from PygFW.Data import DataContainer, Manipulator

import pygame
from _thread import start_new_thread

class Engine(VolatileObject):

    def __init__(self, window_dimensions, fps):

        VolatileObject.__init__(self)

        self._window_dimensions = window_dimensions
        self.pygame_surface = pygame.display.set_mode(window_dimensions)

        self._surface_fps = 1
        self.surface_fps = fps

        self.window_caption = 'A PygFW'
        self.window_icon = None

        self.scenes = DataContainer()
        self._image_bank = ImageBank()

        self.single_events = DataContainer()
        self.repeated_events = DataContainer()

    @property
    def image_bank(self):

        return self._image_bank

    def console_log(self, message, event: str=None):

        event_str = ''

        if event:

            event_str = f'Triggered by event: \'{event}\' '

        print(f""" Console.) {message} {event_str}(time={default_clock})""")

    def console_warn(self, message, event: str=None):

        event_str = ''

        if event:
            event_str = f'Triggered by event: \'{event}\' '

        print(f""" <WARN> Console <WARN>.) {message} {event_str}(time={default_clock})""")

    @property
    def window_dimensions(self):

        return self._window_dimensions

    @window_dimensions.setter
    def window_dimensions(self, new_x_y):

        self._window_dimensions = new_x_y

    @property
    def window_width(self):

        return self._window_dimensions[0]

    @property
    def window_height(self):

        return self._window_dimensions[1]

    @property
    def window_middle_x(self):

        return int(self.window_width / 2)

    @property
    def window_middle_y(self):

        return int(self.window_height / 2)

    @property
    def surface_fps(self):

        return self._surface_fps

    @surface_fps.setter
    def surface_fps(self, fps: int, absolute_set=False):

        if absolute_set:

            self._surface_fps = fps

        else:

            self._surface_fps = int(1000 / fps)

    def start_background_process(self, function, *args, pass_engine=True, **kwargs):

        if pass_engine:

            start_new_thread(function, (self, *args), **kwargs)

        else:

            start_new_thread(function, *args, **kwargs)

    def register_scene(self, scene, scene_id, warn=True):

        if self.scenes.contains_tag(scene_id) and warn:

            self.console_warn(f'Scene with id: \'{scene_id}\' already exists', '*.register_scene()')

        else:

            self.scenes.add(scene, scene_id)

    def get_scene(self, scene_id):

        return self.scenes.get(scene_id) if self.scenes.contains_tag(scene_id) else None

    def start_scene(self, scene_id):

        workspace_scene: Scene = self.get_scene(scene_id)
        workspace_scene.engine_surface = self


        while workspace_scene.run:

            self.pygame_surface = pygame.display.set_mode(self.window_dimensions)
            self.pygame_surface.fill((0, 0, 0))

            pygame.display.set_caption(self.window_caption)
            if self.window_icon:

                pygame.display.set_icon(self.window_icon)

            active_keys = pygame.key.get_pressed()
            pygame_events = pygame.event.get()

            for event in workspace_scene.events._list_:

                for pygame_event in pygame_events:

                    if event.listener == pygame_event.type:

                        event.executor(workspace_scene, pygame_event)

                if active_keys[event.listener]:

                    event.executor(workspace_scene, active_keys)

            for event in workspace_scene.threaded_events._list_:

                for pygame_event in pygame_events:

                    if event.listener == pygame_event.type:

                        start_new_thread(event.executor, (workspace_scene, event))

                if active_keys[event.listener]:

                    start_new_thread(event.executor, (workspace_scene, event))

            for entity in workspace_scene.entities._list_:

                entity.tick()
                entity.draw()

            for event in Manipulator.JoinLists(self.single_events._list_, self.repeated_events._list_):

                event.executor(workspace_scene, event)

            self.single_events.clear()

            pygame.display.update()