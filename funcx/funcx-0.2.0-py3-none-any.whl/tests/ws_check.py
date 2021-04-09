
from funcx.sdk.client import FuncXClient
fxc = FuncXClient(funcx_service_address='http://localhost:5000/api/v1', asynchronous=True)


def hello_world():
    return "Hello World!"


async def task():
    endpoint = '9c81a6d6-578b-4a44-8397-1314f2d16247'
    func_uuid = fxc.register_function(hello_world, endpoint)
    res = fxc.run(endpoint_id=endpoint, function_id=func_uuid)
    print(await res)


fxc.loop.run_until_complete(task())
