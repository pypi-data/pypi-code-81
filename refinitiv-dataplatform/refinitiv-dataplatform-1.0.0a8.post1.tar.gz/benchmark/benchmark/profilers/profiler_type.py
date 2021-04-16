from enum import Enum, unique


@unique
class ProfilerType(Enum):
    timeit = 'timeit'
    pytest = 'pytest'
    mprof = 'mprof'
    time = 'time'


def convert_to_profiler_type(some):
    if isinstance(some, ProfilerType):
        return some
    elif isinstance(some, str):
        return ProfilerType[some]
    else:
        return None
