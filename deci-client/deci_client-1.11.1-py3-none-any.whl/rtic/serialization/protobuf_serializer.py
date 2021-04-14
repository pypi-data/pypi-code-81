from typing import List, Union

import numpy as np

from deci_client.rtic.serialization.protobuf.rtic_server_pb2 import PredictRequest, PredictResponse, GRPCTensor


class NumpyProtobufSerializer:
    """
    A protobuf tensor serializer.
    """

    @staticmethod
    def serialize_response(outputs: List[np.ndarray],
                           model_forward_pass_time_ms: float,
                           server_process_time_ms: float) -> PredictResponse:
        return PredictResponse(outputs=[GRPCTensor(dtype=str(tensor.dtype.str),
                                                   shape=tensor.shape,
                                                   content=bytes(tensor.data)) for tensor in outputs],
                               model_forward_pass_time_ms=model_forward_pass_time_ms,
                               server_process_time_ms=server_process_time_ms)

    @staticmethod
    def serialize_request(model_name: str, inputs: Union[np.ndarray, List[np.ndarray]]) -> PredictRequest:
        arrays_to_serialize = inputs if isinstance(inputs, list) else [inputs]
        return PredictRequest(model_name=model_name,
                              inputs=[GRPCTensor(dtype=str(tensor.dtype.str),
                                                 shape=tensor.shape,
                                                 content=bytes(tensor.data)) for tensor in arrays_to_serialize])

    @staticmethod
    def deserialize_from_request(message: PredictRequest) -> Union[np.ndarray, List[np.ndarray]]:
        outputs = [np.frombuffer(buffer=_input.content,
                                 dtype=_input.dtype).reshape(tuple(_input.shape)) for _input in message.inputs]
        # Correcting the array output - single output will return a single np.ndarray instead of a list
        if len(outputs) == 1:
            return outputs[0]
        return outputs

    @staticmethod
    def deserialize_from_response(message: PredictResponse) -> List[np.ndarray]:
        return [np.frombuffer(buffer=output.content,
                              dtype=output.dtype).reshape(tuple(output.shape)) for output in message.outputs]
