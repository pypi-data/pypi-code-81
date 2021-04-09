import time
from funcx.sdk.client import FuncXClient
fxc = FuncXClient()


def hello_world():
    return "Hello World!"


def run(endpoint):
    func_uuid = fxc.register_function(hello_world, endpoint)
    print(func_uuid)

    res = fxc.run(endpoint_id=endpoint, function_id=func_uuid)
    print(res)
    time.sleep(5)
    print(fxc.get_result(res))


if __name__ == '__main__':

    endpoint = 'c75bc3c8-eb2e-469f-bb45-b6827f41fe8f'
    from funcx.serialize import FuncXSerializer
    fxs = FuncXSerializer()

    serialized = fxs.serialize(hello_world)
    print("Serialized : \n", serialized)

    print(fxs.deserialize(serialized))

    from parsl.serialize import ParslSerializer
    ps = ParslSerializer()

    s = ps.serialize(hello_world)
    print("Serialized with parsl \n", s)
    print(ps.deserialize(s))

    run(endpoint)
