from .base import BaseResponse
import dimod

class DimodResponse(BaseResponse, dimod.SampleSet):
    @classmethod
    def from_json_obj(cls, json_obj):
        return cls.from_serializable(json_obj)

    @classmethod
    def empty_data(cls):
        return cls.from_samples([], 'BINARY', 0)

    def __repr__(self):
        return BaseResponse.__repr__(self) + '\n' + dimod.SampleSet.__repr__(self)

    def __str__(self):
        return BaseResponse.__str__(self) + '\n' + dimod.SampleSet.__str__(self)
