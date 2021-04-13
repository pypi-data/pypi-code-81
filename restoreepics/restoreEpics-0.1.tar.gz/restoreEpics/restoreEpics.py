from . import backUpVals, restoreMethods


def restoreEpics(bak=backUpVals):
    print('Restoring channel values...')
    for ii in range(len(bak)-1, -1, -1):
        restoreMethods[bak[ii]['type']](bak[ii])
