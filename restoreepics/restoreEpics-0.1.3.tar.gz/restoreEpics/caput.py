import epics
from . import backUpVals, restoreMethods


def caput(pvname, value, wait=False, timeout=60.0, bak=backUpVals):
    val = epics.caget(pvname, timeout=timeout)
    if all([ele['name'] != pvname for ele in bak]):
        bak += [{'type': 'channel', 'name': pvname, 'value': val}]
    return epics.caput(pvname=pvname, value=value, wait=wait, timeout=timeout)


def restoreChannel(bakVal):
    epics.caput(bakVal['name'], bakVal['value'])


restoreMethods['channel'] = restoreChannel
