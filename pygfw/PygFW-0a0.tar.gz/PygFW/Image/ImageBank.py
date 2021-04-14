from PygFW.Image.ImageObject import ImageObject


class ImageBank:

    def __call__(self, image_key):

        return self.get(image_key)

    def __repr__(self):

        return f"""<Image Bank Object (size={self.size}, _dict_={self._dict_})>"""

    def __init__(self):

        self._bank = {}

    @property
    def bank(self):

        return self._bank

    @property
    def size(self):

        return len(self._bank)

    @property
    def _dict_(self):

        self_dict = {}

        index = 0
        for image in self._bank:

            self_dict[index] = image

            index += 1

        return self_dict

    def add(self, image: ImageObject, use_self_proclaimed_id=True, overwrite=True):

        image_id = image.user_defined_id if use_self_proclaimed_id else image.actual_image_id

        if image_id not in self._bank or overwrite:

            self._bank[image_id] = image

            return True

        else:

            return False

    def get(self, image_key) -> ImageObject:

        return self._bank[image_key] if image_key in self._bank else False
