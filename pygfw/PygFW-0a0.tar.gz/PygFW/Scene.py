import pygame
from PygFW import Data, Volatile, Event
from PygFW.Data import DataContainer

class Scene(Volatile.VolatileObject):

    def __init__(self, engine_surface):

        Volatile.VolatileObject.__init__(self)

        self._continue_scene = True

        self.engine_surface = engine_surface

        self.events = DataContainer()
        self.threaded_events = DataContainer()
        self.entities = DataContainer()

        self._coordinate_offset = (0, 0)
        self._coordinate_offset_x = self._coordinate_offset[0]
        self._coordinate_offset_y = self._coordinate_offset[0]

    @property
    def run(self):

        return self._continue_scene

    @run.setter
    def run(self, new_run_status):

        self._continue_scene = new_run_status

    @property
    def coordinate_offset(self):

        return self._coordinate_offset

    @coordinate_offset.setter
    def coordinate_offset(self, new_coordinate_offset):

        new_x, new_y = new_coordinate_offset

        self._coordinate_offset = (new_x, new_y)
        self._coordinate_offset_x = new_x
        self._coordinate_offset_y = new_y

    def map_entities(self):

        entity_coordinates = [entity.relative_position for entity in self.entities._list_]

        mapped_entities = []

        for x in range(self.engine_surface.window_width):

            x_layer = []

            for y in range(self.engine_surface.window_height):

                x_layer.append(0 if (x, y) not in entity_coordinates else 1)

            mapped_entities.append(x_layer)

        return mapped_entities

    def map_entities_in_selection(self, radical_x, a_radical_x, radical_y, a_radical_y):

        entity_coordinates = [entity.relative_position for entity in self.entities._list_]

        mapped_entities = []

        for x in range(radical_x, a_radical_x):

            x_layer = []

            for y in range(radical_y, a_radical_y):

                x_layer.append(0 if (x, y) not in entity_coordinates else 1)

            mapped_entities.append(x_layer)

        return mapped_entities
