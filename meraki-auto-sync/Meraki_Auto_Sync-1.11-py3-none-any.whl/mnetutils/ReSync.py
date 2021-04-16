from autosync import lib
from click import echo
from meraki.exceptions import AsyncAPIError

async def reSYNC(_db: object, _net_id: str,network: object,task: str, product: str, _appcfg: object):
    """
         Function reSyces a spefic meraki dashbaord eliment
    Args:
        _db(object): Meraki dashboard SDK Objeect
        _net_id(str): Network Id String
        network(object): Data object for current network
        task(str): Task to resync
        product(str): Meraki Product being synced I.E. switch, wirless
        _appcfg(object): Application Config Object
    Returns:
       Nothing Updateds the network Object that is passed
    """
    try:
        action = getattr(_db, f'get{task}')
        setattr(network, task, await action(_net_id))
    except AsyncAPIError as apie:
        echo(
            f'\t {lib.bc.FAIL} Error Running Setting {task} '
            f'{lib.bc.WARNING}Error Message: {str(apie)}{lib.bc.Default}')
    except Exception as e:
        echo(
                f'{lib.bc.WARNING}Error with Module: {str(e)}'
                f'{lib.bc.Default}')
                