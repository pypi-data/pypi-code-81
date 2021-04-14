import pygame
from PygFW.Image import ImageObject, ImageBank
from collections import deque


class ImageGallery:

    def __setitem__(self, index, image_object):

        self.add(image_object, index)

    def __getitem__(self, index: int):

        return self._image_gallery[index]

    def __call__(self, index: int):

        return self._image_gallery[index]

    def __init__(self, initial_images: [ImageObject, ]=[]):

        self._image_gallery = deque(initial_images)

    @property
    def size(self):

        return len(self._image_gallery)

    @property
    def front(self):

        return self._image_gallery[0] if self.size > 1 else None

    @property
    def back(self):

        return self._image_gallery[self.size - 1] if self.size > 1 else None

    @property
    def gallery(self):

        return self._image_gallery

    def add(self, image_object: ImageObject, index=-1):

        if index < 0:

            index = self.size + 1

        self._image_gallery.insert(index, image_object)

    def rotate(self, direction):

        if direction > 0:

            self._image_gallery.rotate(1)

        else:

            self._image_gallery.rotate(-1)
