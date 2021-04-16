import asyncio
from autosync import lib
import threading
from random import randrange
from meraki.exceptions import AsyncAPIError


async def sync(_db: object, _net_id: str, _net_name: str, _appcfg: object,
               _config: object, product: str,oFunc):
    """
    Proforms a full sync of the _config object that is passed to the fuction
    using the meraki dashboard SDK
    Args:
        oFunc: OverRide Functions
        _db(object): Meraki dashboard SDK Objeect
        _net_id(str): Current Network ID
        _net_name(str): Current Network Name
        _appcfg(object): Application Config
        _config(object): Current Network Configuration Object
        product(str):  Meraki Product being synced I.E. switch, wirless
    Returns:
	   Nothing Updates the _Config Object that is passed
    """
    if _appcfg.DEBUG:
        print(
                f'Current Thread Name:{threading.currentThread().name} '
                f'Thread id:{threading.currentThread().native_id}')
    _maction = getattr(_db,product)
    settings = _config.settings()
    for attr in settings:


        waiting = randrange(0, 2)
        await asyncio.sleep(waiting)
        if _appcfg.DEBUG:
            print(
                    f'\t {lib.bc.OKGREEN}Network:{_net_name}'
                    f'{lib.bc.OKBLUE} Requesting Config Object P{product} - {attr} '
                    f'in Orginization {threading.currentThread().name} with '
                    f'thread :{threading.currentThread().native_id} {lib.bc.Default}')
      
        if attr in oFunc:
            try:
                await eval(f'_config.Get_{attr}(_db, _net_id,_appcfg)')
            except AsyncAPIError as apie:
                print(
                    f'\t {lib.bc.FAIL} Error Running Setting {attr} '
                    f'{lib.bc.WARNING}Error Message: {str(apie)}{lib.bc.Default}')
            except Exception as e:
                print(
                        f'{lib.bc.FAIL}Network: {_net_name} '
                        f'{lib.bc.WARNING}Error with Module: {str(e)}'
                        f'{lib.bc.Default}'
                        f'Running OVerride Function {attr}')
        else:
            try:
                action = getattr(_maction, f'get{attr}')
                setattr(_config, attr, await action(_net_id))
            except AsyncAPIError as apie:
                print(
                    f'\t {lib.bc.FAIL} Error Running Setting {attr} '
                    f'{lib.bc.WARNING}Error Message: {str(apie)}{lib.bc.Default}')
            except Exception as e:
                print(
                        f'{lib.bc.FAIL}Network: {_net_name} '
                        f'{lib.bc.WARNING}Error with Module: {str(e)}'
                        f'{lib.bc.Default}')
                
