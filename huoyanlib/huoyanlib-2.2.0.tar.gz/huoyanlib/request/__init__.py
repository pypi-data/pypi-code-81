class HuoYanLibRequestsError(Exception):
    """Nothing"""


def _raise_huoyanlibrequestserror_sys():
    raise HuoYanLibRequestsError(
        'length of object \'sys.argv\' is not enough, please use 360 explorer -- xueersi running this function'
    )


def _raise_huoyanlibrequestserror_socket():
    raise HuoYanLibRequestsError('can\'t connect to socket server.')
