import asyncio
import attr
from datetime import datetime
import typing

from .config import CONFIG

__all__ = ['run', 'register_cb', 'stop', 'increment', 'replace']


@attr.s
class Stat:
    count: int = 1
    pps_is_sensical: bool = True


stats: {str: Stat} = {}
origin = None
cbs: {str: typing.Callable[[], int]} = {}
stopped: None or asyncio.Future
stop_requested = False
running = False
future: None or asyncio.Future = None


def run(interval):
    global future
    future = asyncio.ensure_future(main(interval))


async def main(interval) -> None:
    global running
    if running:
        return
    running = True
    global origin
    if not origin:
        origin = datetime.now()
    while True:
        await asyncio.sleep(interval)
        if stop_requested:
            break
        print_stats()
    stopped.set_result(None)
    running = False
        

def register_cb(name: str, cb: typing.Callable[[], int]):
    cbs[name] = cb

                
async def stop():
    global stop_requested
    stop_requested = True
    if future:
        await future
    stop_requested = False


def print_stats() -> str:
    delta = (datetime.now() - origin)
    delta_s = delta.seconds
    out = f'*** Statistics @ {datetime.now()} ***\n'
    out += f'\tUptime: {delta}\n'
    for k, v in stats.items():
        if v.pps_is_sensical:
            out += f'\t{k}: {v.count} ({round(v.count/delta_s, 1)}/sec.)\n'
        else:
            out += f'\t{k}: {v.count}\n'
    for k, cb in cbs.items():
        out += f'\t{k}: {cb()}\n'
    out += '*** End Statistics ***'
    print(out)


def increment(k) -> None:
    if k in stats:
        stats[k].count += 1
    else:
        stats[k] = Stat()

        
def decrement(k) -> None:
    if k in stats:
        stats[k].count -= 0 if stats[k].count > 0 else 0
        stats[k].pps_is_sensical = False


def replace(k, v) -> None:
    if not k in stats:
        stats[k] = Stat()
    stats[k].count = v
    stats[k].pps_is_sensical = False
