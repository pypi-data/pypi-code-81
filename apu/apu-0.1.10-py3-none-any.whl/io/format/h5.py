""" handle h5 data """
import h5py
from apu.io.fileformat import FileFormat

# pylint: disable=C0103,W0104
class H5(FileFormat):
    """ h5 fileformat handler """

    def recursively_save_dict_contents_to_group(self, h5file: h5py.File,
                                                    path: str, dic: dict):
        """ save recursivly """
        for key, value in dic.items():
            if isinstance(value, dict):
                if value['type'] == 1:
                    group = h5file.create_group(path + key)
                    for attr_key, attr_value in value["attr"].items():
                        group.attrs[attr_key, attr_value]

                    if len(value.items()) > 0:
                        self.recursively_save_dict_contents_to_group(
                            h5file, path + key + "/", value)

                elif value['type'] == 0:
                    dataset = h5file.create_dataset(path + key,
                                                    data=value["data"])
                    for attr_key, attr_value in value["attr"].items():
                        dataset.attrs[attr_key, attr_value]
                else:
                    print("do not know the type?")
                    continue
            elif isinstance(value, (list, tuple)):
                self.recursively_save_dict_contents_to_group(
                    h5file, path + key + '/', value)

    def recursively_load_dict_contents_from_group(self, h5_file, path):
        """
        Load contents of an HDF5 group. If further groups are encountered,
        treat them like dicts and continue to load them recursively.
        """
        self.data = {}
        for key, item in h5_file[path].items():
            if isinstance(item, h5py.Dataset):
                self.data[key] ={ "attr": item.attrs,
                    "data": item[()],
                    "type": 0
                }
            elif isinstance(item, h5py.Group):
                if len(item.items()) == 0:
                    self.data[key] = {
                        "attr": item.attrs,
                        "name": item.name,
                        "type": 1
                    }
                else:
                    self.recursively_load_dict_contents_from_group(
                        h5_file, path + key + '/')

    def read(self):
        with h5py.File(self._filepath, "r") as h5file:
            self.recursively_load_dict_contents_from_group(h5file, "/")
        return self.data

    def write(self):
        with h5py.File(self._filepath, 'w') as h5file:
            self.recursively_save_dict_contents_to_group(h5file, '/', self.data)
        return self.data

    @classmethod
    def suffix(cls):
        return (".h5", ".hdf5")
