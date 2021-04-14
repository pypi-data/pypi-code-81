class DataContainer:

    def __setitem__(self, data_tag, data):

        self.add(data, data_tag)

    def __getitem__(self, data_tag):

        return self.get(data_tag)

    def __call__(self, data_tag):

        return self.get(data_tag)

    def __repr__(self):

        return f"""<Data Container Object (size={self.size}, values={self.container})>"""

    def __init__(self, initial_values: dict=None, size_allowance: int=None):

        self._data_container = {} if initial_values is None else initial_values
        self.size_allowance = -1 if size_allowance is None else size_allowance

        self._cap_sizes = {}

    @property
    def container(self) -> dict:

        return self._data_container

    @property
    def size(self) -> int:

        return len(self._data_container)

    @property
    def _list_(self) -> list:

        return [self._data_container[tag] for tag in self._data_container]

    @property
    def _list_tags_(self) -> list:

        return [tag for tag in self._data_container]

    @property
    def _switch_(self) -> dict:

        switched_dict = {}

        for tag in self._data_container:

            switched_dict[self._data_container[tag]] = tag

        return switched_dict

    @property
    def _wrapped_(self):

        return f'{self.container}'

    @property
    def string(self):

        return ''.join(self._list_) if [True*self.size] == [isinstance(item, str) for item in self._list_] else None

    def add(self, data, data_tag: str=None, overwrite=True):

        data_tag = f'<DataContainerItem (index={self.size}, data={data})>' if data_tag is None else data_tag

        if data_tag is None:

            raise ValueError(f'Data tag belonging to :\'{data}\' is None, this means no data_tag was given in \'MDTContainer.add)\' and no data_tag value was given to the MDTObject')

        if data_tag not in self._data_container or overwrite:

            if self.size_allowance > self.size or self.size_allowance < 0:


                if self.capped(data.__class__) and len(self.findall(data.__class__)) < self._cap_sizes[data.__class__]:

                    self._data_container[data_tag] = data

                    return data_tag

                elif not self.capped(data.__class__):

                    self._data_container[data_tag] = data

                    return data_tag

                else:

                    return None

            else:

                return None

        else:

            return None

    def contains(self, data) -> bool:

        return data in self._list_

    def contains_tag(self, data_tag) -> bool:

        return data_tag in self._list_tags_

    def get(self, data_tag):

        return self._data_container[data_tag] if data_tag in self._data_container else None

    def get_tag(self, data) -> str:

        return self._switch_[data]

    def clear(self):

        self._data_container = {}

    def remove(self, data_tag, i_know_what_im_doing=False):

        if data_tag in self._data_container and i_know_what_im_doing:

            data = self._data_container[data_tag]

            del self._data_container[data_tag]

            return data

    def remove_index(self, index, i_know_what_im_doing=False):

        if index < self.size and i_know_what_im_doing:

            data = self._data_container[self._list_tags_[index]]

            del self._data_container[self._list_tags_[index]]

            return data

    def cap(self, object_class, amount):

        self._cap_sizes[object_class] = amount

    def capped(self, object_class):

        return self._cap_sizes[object_class] if object_class in self._cap_sizes else None

    def findall(self, object_type):

        found_objects = []

        for found_object in self._list_:

            if found_object.__class__ == object_type:

                found_objects.append(found_object)

        return found_objects
