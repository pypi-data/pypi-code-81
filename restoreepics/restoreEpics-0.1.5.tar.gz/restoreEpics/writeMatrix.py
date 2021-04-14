#!/usr/bin/env python3

from epics import caput
import numpy as np
import argparse
from .readMatrix import readMatrix
from time import sleep
from . import backUpVals, restoreMethods


def writeMatrix(basename, inpMat, firstRow=1, firstCol=1, suffix=None,
                tramp=3.0, bak=backUpVals):
    '''
    Write epics channels to put matrix on a EPICS channel matrix.
    '''
    curMat = readMatrix(basename=basename, rows=inpMat.shape[0],
                        cols=inpMat.shape[1], firstRow=firstRow,
                        firstCol=firstCol, suffix=suffix)
    if all([ele['name'] != basename for ele in bak]):
        bak += [{'type': 'matrix', 'name': basename, 'suffix': suffix,
                 'value': curMat, 'firstRow': firstRow, 'firstCol': firstCol,
                 'tramp': tramp}]
    # Special case, changing filter gains, can use TRAMP
    rampYourself = True
    if suffix == 'GAIN':
        try:
            curTramp = readMatrix(basename=basename, rows=inpMat.shape[0],
                                  cols=inpMat.shape[1], firstRow=firstRow,
                                  firstCol=firstCol, suffix='TRAMP')
            for ii in range(firstRow, firstRow + np.shape(inpMat)[0]):
                for jj in range(firstCol, firstCol + np.shape(inpMat)[1]):
                    chName = (basename + '_' + str(ii) + '_' + str(jj)
                              + '_TRAMP')
                    caput(chName, tramp)
            rampYourself = False
        except BaseException:
            rampYourself = True
    if rampYourself:
        rampSteps = 100
        # Get current matrix values
        stepMat = (inpMat - curMat) / rampSteps
        for tstep in range(1, rampSteps):
            for ii in range(firstRow, firstRow + np.shape(inpMat)[0]):
                for jj in range(firstCol, firstCol + np.shape(inpMat)[1]):
                    chName = basename + '_' + str(ii) + '_' + str(jj)
                    if suffix is not None:
                        chName = chName + '_' + suffix
                    matToWrite = (curMat[ii-firstRow, jj-firstCol]
                                  + tstep * stepMat[ii-firstRow, jj-firstCol])
                    caput(chName, matToWrite)
            sleep(tramp/rampSteps)
    # Finally write the required matrix
    for ii in range(firstRow, firstRow + np.shape(inpMat)[0]):
        for jj in range(firstCol, firstCol + np.shape(inpMat)[1]):
            chName = basename + '_' + str(ii) + '_' + str(jj)
            if suffix is not None:
                chName = chName + '_' + suffix
            caput(chName, inpMat[ii-firstRow, jj-firstCol])
    if not rampYourself:
        sleep(tramp + 0.5)    # Wait for ramping to end
        for ii in range(firstRow, firstRow + np.shape(inpMat)[0]):
            for jj in range(firstCol, firstCol + np.shape(inpMat)[1]):
                chName = (basename + '_' + str(ii) + '_' + str(jj)
                          + '_TRAMP')
                caput(chName, curTramp[ii-firstRow, jj-firstCol])


def restoreMatrix(bakVal):
    writeMatrix(basename=bakVal['name'], suffix=bakVal['suffix'],
                inpMat=bakVal['value'], firstCol=bakVal['firstCol'],
                firstRow=bakVal['firstRow'], tramp=10, bak=[])


restoreMethods['matrix'] = restoreMatrix


def grabInputArgs():
    parser = argparse.ArgumentParser(
        description='This writes matrix coefficients from a text file to '
                    'EPICS channels. Note that all indices start from 1 by '
                    'convention for EPICS channels.'
        )
    parser.add_argument('inMatFile', type=str, help='Input Matrix file name')
    parser.add_argument('basename', type=str, help='Matrix EPICS base name')
    parser.add_argument('-r', '--rows', type=int,
                        help='Number of rows to write. Default None(all)',
                        default=None)
    parser.add_argument('-c', '--cols', type=int,
                        help='Number of columns to write. Default None(all)',
                        default=None)
    parser.add_argument('--firstRow', type=int,
                        help='First index of output. Default 1',
                        default=1)
    parser.add_argument('--firstCol', type=int,
                        help='First index of input. Default 1',
                        default=1)
    parser.add_argument('--fileRowInd', type=int,
                        help='First row index in file. Default 1',
                        default=1)
    parser.add_argument('--fileColInd', type=int,
                        help='First col index in file. Default 1',
                        default=1)
    parser.add_argument('-t', '--tramp', type=int,
                        help='Ramping time when chaning values. Default 3',
                        default=3)
    parser.add_argument('-s', '--suffix', type=str,
                        help='Any suffix after the matrix indices in channel '
                             'names. Default is None.')

    return parser.parse_args()


if __name__ == '__main__':
    args = grabInputArgs()
    inpMat = np.loadtxt(args.inMatFile, ndmin=2)[args.fileRowInd-1:,
                                                 args.fileColInd-1:]
    if args.cols is not None:
        inpMat = inpMat[:, :args.cols]
    if args.rows is not None:
        inpMat = inpMat[:args.rows, :]
    writeMatrix(basename=args.basename, inpMat=inpMat, firstRow=args.firstRow,
                firstCol=args.firstCol, suffix=args.suffix, tramp=args.tramp)
