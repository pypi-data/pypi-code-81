class Cake:

    def __init__(self):

        self._layers = []

    @property
    def length(self):

        return len(self._layers)

    @property
    def full(self):

        return self._layers

    @property
    def _dict_(self):

        cake_dict = {}

        for index in range(self.length):
            cake_dict[index] = self._layers[index]

        return cake_dict

    def apply(self, obj, *args, index=-1, **kwargs):

        if index < 0:

            index = self.length + 1

        self._layers.insert(index, (obj, args, kwargs))

    def get(self, layer_index, delete=False):

        if layer_index < self.length:

            layer = self._layers[layer_index]

            if delete:

                self._layers.pop(layer_index)

            return layer

        else:

            return None

    def enumerate(self):

        return [(index, self._layers[index]) for index in range(self.length)]

    def destroy(self):

        self._layers = []