"""
handling numpy data for json

author: anton feldmann <anton.feldmann@gmail.com>
"""
from json.encoder import JSONEncoder
from json.decoder import JSONDecoder

import numpy as np

# pylint: disable=C0103,R0201,R1705,R0911

class NumpyEncoder(JSONEncoder):
    """ Custom encoder for numpy data types
        The NumpyEncoder is a JSONEncoder


    Examples:
    ..  example_code::
        >>> import numpy as np
        >>> import json
        >>> from apu.encoding.json.np import NumpyEncoder
        >>> arr = array([   0,  239,  479,  717,  952, 1192, 1432, 1667],
        ...      dtype=int64)
        >>> json.dumps(arr,cls=NumpyEncoder)
    """

    def np_list(self, obj):
        """ numpy array object to json list """
        return obj.tolist()

    def np_float(self, obj):
        """ numpy float type to float """
        return float(obj)

    def np_int(self, obj):
        """ numpy int to int """
        return int(obj)

    def np_complex(self, obj):
        """ numpy complex to dict.
        because the decoder has to decode
        complex i use a dict """
        return { "real": obj.real, "imag": obj.imag }

    def np_bool(self, obj):
        """ numpy boolean to boolean """
        return bool(obj)

    def np_null(self, obj):
        """ numpy null no None or json null """
        return None

    def np(self, obj):
        """ np function to check for all numpy objects """
        if isinstance(obj, np.integer):
            return self.np_int(obj)

        elif isinstance(obj, np.floating):
            return self.np_float(obj)

        elif isinstance(obj, (np.complex_, np.complex64, np.complex128)):
            return self.np_complex(obj)

        elif isinstance(obj, (np.ndarray,)):
            return self.np_list(obj)

        elif isinstance(obj, (np.bool_)):
            return self.np_bool(obj)

        elif isinstance(obj, (np.void)):
            return self.np_null(obj)

        return JSONEncoder.default(self, obj)

    def default(self, obj):
        """ defualt Encoder entrypoint to encode """
        return self.np(obj)

class NumpyDecoder(JSONDecoder):
    """ Custom decode for numpy data types

    Examples:
    ..  example_code::
        >>> import numpy as np
        >>> import json
        >>> from apu.encoding.json.np import NumpyDecoder
        >>> arr = '[[2.468031, 0.0, 0.0],
                    [-1.234015, 2.137377, 0.0],
                    [0.0, 0.0, 19.998293]]'
        >>> json.loads(arr,cls=NumpyDecoder)
        [[ 2.468031  0.        0.      ]
        [-1.234015  2.137377  0.      ]
        [ 0.        0.       19.998293]]
    """

    _recursable_types = [str, list, dict]

    def _is_recursive(self, obj) -> bool:
        """ check if the onject is recursiveable

        Returns:
            (bool): the object is recursiveable
        """
        return type(obj) in NumpyDecoder._recursable_types

    # pylint: disable=R1710, R0912:
    def decode(self, obj, *args, **kwargs):
        """ decode the json string """
        if not kwargs.get('recurse', False):
            obj = super().decode(obj, *args, **kwargs)

        if isinstance(obj, list):
            try:
                return np.array(obj)
            except: # pylint: disable=W0702
                for item in obj:
                    if self._is_recursive(item):
                        obj[item] = self.decode(item, recurse=True)

        elif isinstance(obj, dict):
            for key, value in obj.items():
                if str(key) in "real":
                    return np.complex(obj['real'], obj['imag'])
                elif self._is_recursive(value):
                    obj[key] = self.decode(value, recurse=True)

        elif isinstance(obj, bool):
            return np.bool(obj)

        elif isinstance(obj, float):
            return np.float(obj)

        elif obj is None:
            return np.void

        else:
            return obj
