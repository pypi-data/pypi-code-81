import struct
from abc import ABCMeta
from functools import reduce
from typing import Union, List

import numpy as np


class AbstractSerializer(ABCMeta):
    """
    Serializes and Deserializes arbitrary data.
    """

    @staticmethod
    def serialize(obj):
        """Converts the object to a buffer, which can be later reconstructed using the class's deseralize() method.
        :type obj: np.ndarray
        :return: bytes
        """
        raise NotImplementedError

    @staticmethod
    def deserialize(obj_bytes):
        """
        Deserialized the bytes into a python object.
        :type obj_bytes: bytes
        return: np.ndarray
        """
        raise NotImplementedError


class ClientNumpySerializer(AbstractSerializer):
    """
    A numpy array serializer/deserializer (like JSON but tiny and fast).
    Effecient to replace JSON and sometimes beats Protobuf in efficiency and memory
    """

    # Warning: Any line of code added here will delay inference runtime.
    # These methods are called 100s of time per second.

    @staticmethod
    def serialize(obj: Union[np.ndarray, List[np.ndarray]]) -> bytes:
        """
        Serializes np.ndarray instances to native bytearrays.
        :param obj: A numpy.ndarray, or a list of np.ndarray instances, to bytes.
        :param data_type: The type of the data in struct library: https://docs.python.org/3/library/struct.html#format-characters
        """
        serialized_bytes: bytes = bytes()
        arrays_to_serialize = obj if isinstance(obj, list) else [obj]
        for array in arrays_to_serialize:
            shape_dims = len(array.shape)
            # Adding the shape dimensions
            serialized_bytes += struct.pack("<I", shape_dims)
            # Adding the shape values
            serialized_bytes += struct.pack("<%uI" % shape_dims, *array.shape)
            # Adding the data type
            serialized_bytes += array.dtype.str.encode()
            # Adding the data length for the tensor.
            # The data length is array.dtype.itemsize times each of the elements in the array shape.
            tensor_size_in_bytes = reduce(lambda a, b: a * b, [array.dtype.itemsize] + list(array.shape))
            serialized_bytes += struct.pack("<I", tensor_size_in_bytes)
            # Adding array raw bytes
            serialized_bytes += bytearray(array.data)
        return serialized_bytes

    @staticmethod
    def deserialize(obj_bytes: bytes) -> Union[np.ndarray, List[np.ndarray]]:
        """
        Deserializes native buffer instance to np.ndarray instance(s).
        :param obj_bytes:
        :param obj: A numpy.ndarray, or a list of np.ndarray instances, to bytes.
        """
        obj_bytes = memoryview(obj_bytes)
        input_buffer_length = len(obj_bytes)
        deserialized_tensors = []
        deserialize_index = 0
        deserialized_all = False
        while not deserialized_all:
            # Deserializing the shape
            shape_dims: int = struct.unpack("<I", obj_bytes[deserialize_index:deserialize_index + 4])[0]
            deserialize_index += 4
            shape: tuple = \
                struct.unpack("<%uI" % shape_dims,
                              obj_bytes[deserialize_index:deserialize_index + 4 * shape_dims])
            deserialize_index += 4 * shape_dims

            # Deserializing the np.dtype
            dtype_length = 3
            dtype_bytes = obj_bytes[deserialize_index: deserialize_index + dtype_length].tobytes()
            dtype = np.dtype(dtype_bytes)
            deserialize_index += dtype_length

            # Deserializing the data length
            tensor_length_field_size = 4
            next_index = deserialize_index + tensor_length_field_size
            tensor_size_in_bytes = struct.unpack("<I", obj_bytes[deserialize_index:next_index].tobytes())[0]
            deserialize_index += tensor_length_field_size

            # Deserializing the data
            data = obj_bytes[deserialize_index:deserialize_index + tensor_size_in_bytes]
            tensor = np.frombuffer(data, dtype=np.dtype(dtype)).reshape(shape)
            deserialize_index += tensor_size_in_bytes
            deserialized_tensors.append(tensor)

            # Check if we went through the entire buffer, or are there remaining objects:
            if deserialize_index >= input_buffer_length:
                deserialized_all = True
        return deserialized_tensors
