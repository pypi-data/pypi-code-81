import pygame

pygame.init()

class ImageObject:

    def __repr__(self):

        return f"""<Image Object (path={self.image_path}, dimensions={self.dimensions})>"""

    def __init__(self, image_path, self_proclaimed_id: str=None, convert_to_alpha=True, initial_rotation=None, initial_scale=None, initial_dimensions=None):

        self.image_path = image_path
        self.image_loaded = pygame.image.load(image_path)

        self._self_proclaimed_id = f'<Image Object (path={self.image_path}, alpha={convert_to_alpha}, rotation={initial_rotation})>' if self_proclaimed_id is None else self_proclaimed_id
        self._actual_image_id = self._self_proclaimed_id

        self._image_converted = self.image_loaded.convert_alpha() if convert_to_alpha else self.image_loaded.convert()
        self._initialised_image = self._image_converted

        self.original_dimensions = self.width, self.height
        self.dimensions_history = []

        self.initialised_rotation = initial_rotation
        self.initial_rotation = self.initialised_rotation
        if initial_rotation:

            self.change_rotation(initial_rotation)
            self.initial_rotation = initial_rotation

        self.initialised_scale = 1
        self.initial_scale = self.initialised_scale
        if initial_scale:

            self.change_scale(initial_scale)
            self.initial_scale = initial_scale

        self.initialised_dimensions = (self.width, self.height)
        self.initial_dimensions = self.initialised_dimensions
        if initial_dimensions:

            self.change_dimensions(initial_dimensions)
            self.initial_dimensions = initial_dimensions




    @property
    def user_defined_id(self):

        return self._self_proclaimed_id

    @property
    def actual_image_id(self):

        return self._actual_image_id

    @actual_image_id.setter
    def actual_image_id(self, new_id: str):

        self._actual_image_id = new_id

    @property
    def pygame_rect(self):

        return self._image_converted.get_rect()

    @property
    def width(self):

        return self.pygame_rect.width

    @property
    def height(self):

        return self.pygame_rect.height

    @property
    def dimensions(self):

        return self.width, self.height

    @property
    def image(self):

        return self._image_converted

    def get_warped(self, new_dimensions: [int, int]):

        return pygame.transform.scale(self._initialised_image, new_dimensions)

    def change_dimensions(self, new_dimensions: [int, int]):

        self._image_converted = self.get_warped(new_dimensions)

    def change_scale(self, new_scale: float):

        self._image_converted = self.get_warped((self.width * new_scale, self.height * new_scale))

    def get_rotated(self, new_rotation):

        return pygame.transform.rotate(self._initialised_image, new_rotation)

    def change_rotation(self, new_rotation: int):

        self._image_converted = self.get_rotated(new_rotation)

    def draw(self, pygame_surface: pygame.Surface, spawn: [int, int], offset_x=0, offset_y=0):

        pygame_surface.blit(self._image_converted, (spawn[0] + offset_x, spawn[1] + offset_y))

    def convert(self, convert_to_alpha=True):

        self._image_converted = self.image_loaded.convert_alpha() if convert_to_alpha else self.image_loaded.convert()

    def get_faded(self, new_alpha):

        original_image = self._initialised_image
        faded_image = original_image
        faded_image.set_alpha(new_alpha)

        return faded_image

    def fade(self, new_alpha):

        self._image_converted = self.get_faded(new_alpha)