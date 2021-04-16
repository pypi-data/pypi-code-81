#!/usr/bin/env python3


from binascii import unhexlify
from glob import glob
import os
import numpy as np
import sys
import mmap
import struct
import rawprasslib
import logging

logger = logging.getLogger('acqLogLogger')

utypes = {
        unhexlify("0300000000000000"): [1, np.bool],
        unhexlify("0400000000000000"): [1, np.bool],
        unhexlify("0600000000000000"): [2, np.int16],
        unhexlify("0900000000000000"): [4, np.int32],
        unhexlify("0800000002000000"): [4, np.int32],
        unhexlify("0a00000002000000"): [4, np.float32],
        unhexlify("0b00000002000000"): [8, np.float64]}

#ANOTHER DIRTY THING
globtmpheaders = []

def load_log(raw_file, tmp_folder):
    inf = open(raw_file, "rb")
    mf = mmap.mmap(inf.fileno(), 0, access=mmap.ACCESS_READ)
    data_format = rawprasslib.rawprasslib.get_data_format(mf)
    if data_format in (47, 57, 60, 63):
        if data_format in (47, 60, 63):
            pos = mf.find(unhexlify("ffffffffffffffff"))+32
            mf.seek(pos+40)
        else:
            while 1:
                pos = mf.find(unhexlify("01000000"))
                if pos == int(-1):
                    raise Exception(
                        "[ERROR] expected date and time not found in the file,"
                        " unknown .raw file format")
                mf.seek(pos+4)
                fmt = "<8h"
                year, month, dow, dom, h, m, s, ms = struct.unpack(
                        fmt, mf.read(struct.calcsize(fmt)))
                if year > 1980 and 0 < month <= 12 and 0 < dow <= 7 and\
                        0 < dom <= 31 and 0 <= h < 24 and 0 <= m < 60 and\
                        0 <= s < 60 and 0 <= ms < 1000:
                    break
            mf.seek(pos+44)
        tail_pos = struct.unpack("<i", mf.read(4))[0]
        temp = False
        if tail_pos == 0:
            temp = True
            logger.warning("Did not find parameters in the original file\n"
                           "Looks like the scanning is in progress,"
                           " will search for the temp file")
        else:
            mf.seek(tail_pos+36)
            parvals_start, parvals_end = struct.unpack("<ii", mf.read(8))
            pos = mf.find(struct.pack("<i", tail_pos))
            mf.seek(pos+12)
            if not struct.unpack("<i", mf.read(4))[0] == 1:
                print(parvals_start, parvals_end)
                raise Exception("[ERROR] Position check failed, raising exception")
            mf.seek(pos-28)
            supparams_pos = struct.unpack("<i", mf.read(4))[0]
            mf.seek(pos+24)
            mtlen = struct.unpack("<i", mf.read(4))[0]*2
            machtype = mf.read(mtlen).decode("UTF-16")
            logger.info("Stated machine type is {}".format(machtype))
            # skip next 4 values as they're of no interest to us
            for i in range(4):
                skiplen = struct.unpack("<i", mf.read(4))[0]*2
                mf.seek(mf.tell()+skiplen)
            mf.seek(mf.tell()+16)
    else:
        raise Exception('unknown .RAW data format')
    logger.info("Performing parameters/vals readout")
    names, units = [], []
    if temp == False:
        while (mf.tell() < parvals_start):
            paramunit = mf.read(8)
            strlen = struct.unpack("<i", mf.read(4))[0]*2
            param = mf.read(strlen).decode("UTF-16")
            if len(param) > 0:
                names.append(param)
                units.append(paramunit)
        logger.info("Found {} parameters".format(len(names)))
        mf.seek(parvals_start)
        paramvals = []
        while (mf.tell() < parvals_end):
            paramscan = []
            for i, unit in enumerate(units):
                if i == 0:
                    paramscan.append(np.frombuffer(
                        mf.read(4), dtype=np.float32)[0])
                elif unit == unhexlify("0000000000000000"):
                    paramscan.append("")
                elif unit[:4] == unhexlify("0d000000"):
                    strlen = struct.unpack("<i", unit[4:])[0]*2
                    paramscan.append(mf.read(strlen).decode("UTF-16"))
                elif unit in utypes:
                    paramscan.append(np.frombuffer(
                        mf.read(utypes[unit][0]), dtype=utypes[unit][1])[0])
                else:
                    raise Exception(
                            "unknown encountered during parsing, surrending")
            paramvals.append(paramscan)
            logger.info("Performed readout @ t={}".format(paramscan[0]))
        logger.info("Found {} parameters".format(len(paramvals)))
    else:
        #!!! DIRTY DIRTY DIRTY !!! JUST PROOF OF CONCEPT FOR TSQ MACHINES!!!
        #WILL NEED TO REWRITE QUITE SOON!!!
        def read_tmp_file(file):
            inp = open(file, mode="rb")
            data = inp.read()
            inp.close()
            return data
        def find_tmp_file(array, targpos, tmp_files):
            for file in tmp_files:
                if read_tmp_file(file).find(unhexlify(array)) == targpos:
                    logger.info("Found temp file"+file)
                    data = open(file, "rb")
                    return file, data
            raise Exception("[ERROR] Valid .tmp file was not found")
        tmp_files = sorted(glob(tmp_folder+"/*"),
                       key=lambda tmpf: os.stat(tmpf).st_mtime,
                       reverse=True)
        filename, paramfile = find_tmp_file(
                "0F00000041005000430049002F00450053004900200053004F005500", 24, tmp_files)
        paramfile.seek(16)
        emptylines = 0
        while emptylines < 3:
            paramunit = paramfile.read(8)
            strlen = struct.unpack("<i", paramfile.read(4))[0]*2
            param = paramfile.read(strlen).decode("UTF-16")
            if len(param) > 0:
                names.append(param)
                units.append(paramunit)
                emptylines = 0
            else:
                emptylines += 1
        logger.info("Found {} parameters".format(len(names)))
        base, tmpnumber = filename.split(".")[0].split("LCQ")
        datapath = base + "LCQ" + str(hex(int(tmpnumber, 16)+1))[2:].upper() + ".tmp"
        globtmpheaders.clear()
        globtmpheaders.append(base + "LCQ" + str(hex(int(tmpnumber, 16)+7))[2:].upper() + ".tmp")
        valsfile = open(datapath, "rb")
        paramvals = []
        bacon = True
        while bacon:
            paramscan = []
            for i, unit in enumerate(units):
                if i == 0:
                    paramscan.append(np.frombuffer(
                        valsfile.read(4), dtype=np.float32)[0])
                elif unit == unhexlify("0000000000000000"):
                    paramscan.append("")
                elif unit[:4] == unhexlify("0d000000"):
                    strlen = struct.unpack("<i", unit[4:])[0]*2
                    paramscan.append(valsfile.read(strlen).decode("UTF-16"))
                elif unit in utypes:
                    paramscan.append(np.frombuffer(
                        valsfile.read(utypes[unit][0]), dtype=utypes[unit][1])[0])
                else:
                    raise Exception(
                            "unknown encountered during parsing, surrending")
            if paramscan[0] == 0:
                break
            else:
                paramvals.append(paramscan)
            logger.warn("Performed readout @ t={}".format(paramscan[0]))
        supparams_pos = -666

    return data_format, supparams_pos, names, paramvals


def load_scanlog(raw_file, data_format, supparams_pos):
    if supparams_pos == -666:
        #print(globtmpheaders[0])
        mf = open(globtmpheaders[0], 'rb')
    else:
        inf = open(raw_file, "rb")
        mf = mmap.mmap(inf.fileno(), 0, access=mmap.ACCESS_READ)
        mf.seek(supparams_pos)
    scancount = struct.unpack("<i", mf.read(4))[0]
    # things which are hidden in x are not understood yet
    if data_format == 47:
        #fmt = "<36xd8xd12x2d12x"
        fmt = "<4xbxb29xd8xd12x2d12x"
        fmtsize = struct.calcsize(fmt)
        # neg/pos, ms^n, q1 mass selection, COFF, start m/z, end m/z
        scanlogs = [struct.unpack(fmt, mf.read(fmtsize))
                    for _ in range(scancount)]
    elif data_format in (57, 60, 63):
        def augunpack(mf):
            negpos, msn = struct.unpack("<4xbxh", mf.read(8))
            offset = "<76x" if data_format in (57, 60) else "<124x"
            fmt = offset+"".join(["3d8x" for i in range(msn-1)])+"4x2d12x"
            log = struct.unpack(fmt, mf.read(struct.calcsize(fmt)))
            return (negpos, msn)+log
        # neg/pos, ms^n, (parent m/z, selection width, coff)*cidcount,
        # start m/z, end m/z
        # selection width needs to be verified, it is just guess for now
        scanlogs = [augunpack(mf) for _ in range(scancount)]
    else:
        raise Exception("unknown encountered during parsing, surrending")
    return scanlogs


def load_params(
        filename, tmp_glob=r"C:/ProgramData/Thermo Scientific/Temp/*.tmp"):
    machtype, sppos, names, paramvals = load_log(filename, tmp_glob)
    scanlog = load_scanlog(filename, machtype, sppos)
    logger.info("parameters loaded, hopefully in correct way")
    return [names, paramvals], scanlog, machtype


if __name__ == "__main__":
    logging.basicConfig()
    logger.setLevel("DEBUG")
    filename = sys.argv[1]
    machtype, sppos, names, paramvals = load_log(filename, "")
    load_scanlog(filename, machtype, sppos)
    if machtype == 47:
        dataset = [np.average([param[i] for param in paramvals[1:]])
                   for i in (3, 4, 5, 12, 36)]
        print("spray voltage {:.1f} kV, capillary temperature {:.0f} °C, "
              "Capillary voltage {:.0f} V, Tube lens voltage {:.0f} V, p(Xe) "
              "= {:.2f} mTorr,".format(*dataset))
    elif machtype in (60, 63):
        dataset = [np.average([param[i] for param in paramvals[1:]])
                   for i in (1, 9, 8, 10, 5, 6)]
        print("spray voltage {:.1f} kV, capillary temperature {:.0f} °C, "
              "Capillary voltage {:.0f} V, Tube lens voltage {:.0f} V, sheat "
              "gas flow rate = {:.2f} (arb), aux gas flow rate = {:.2f} (arb)"
              .format(*dataset))
