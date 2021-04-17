# -*- coding: utf-8 -*-
"""
This file will receive and parse can-msg from can-bus with PeakCan(current only support).

In current huichuang project, the dbc protocal show below(default_huichuang_dbc.json).
TR      CAN-ID      Name                    Physical Implication
----------------------------------------------------------------------------------------
R       0x6F8       warning_id              the status of current feature 
R       0x6FA       version_id              the version of current software
R       0x500       detections_mem_id       the frame id and timestamp of detections-mem
R       0x501       detections_mem_data     the data of detections-mem 
"""

# @File  : can_process.py
# @Author: Andy.yang lan.zhang
# @Date  : 2021/02/22
# @Software: VS Code

import time

from threading import Thread
from json import load, dump
from os.path import dirname, realpath, join

from can.interface import Bus
from can import CSVWriter, Printer
import pandas as pd
from pandas.api.types import is_numeric_dtype

# peak can setting
try:
    peakcan_bus = Bus(bustype='pcan', channel='PCAN_USBBUS1', bitrate=500000)
except:
    print("The Peak-CAN is not connected")

is_stop = True


class CanParseThread(Thread):
    def __init__(self, func, args, name=''):
        Thread.__init__(self)
        self.name = name
        self.func=func
        self.args = args
        self.result=self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None


def _fillZero(bit_str):
    num_fill_zero = 8 - len(bit_str)
    if num_fill_zero == 0:
        return bit_str
    elif num_fill_zero == 1:
        return f"0{bit_str}"
    elif num_fill_zero == 2:
        return f"00{bit_str}"
    elif num_fill_zero == 3:
        return f"000{bit_str}"
    elif num_fill_zero == 4:
        return f"0000{bit_str}"
    elif num_fill_zero == 5:
        return f"00000{bit_str}"
    elif num_fill_zero == 6:
        return f"000000{bit_str}"
    elif num_fill_zero == 7:
        return f"0000000{bit_str}"
    else:
        print("Error: fill zero in _fillZeon of can_process.py")
        return f"error"


def _convertHexToBits(hex_data):
    bin_0_str = _fillZero(bin(hex_data[0])[2:])
    bin_1_str = _fillZero(bin(hex_data[1])[2:])
    bin_2_str = _fillZero(bin(hex_data[2])[2:])
    bin_3_str = _fillZero(bin(hex_data[3])[2:])
    bin_4_str = _fillZero(bin(hex_data[4])[2:])
    bin_5_str = _fillZero(bin(hex_data[5])[2:])
    bin_6_str = _fillZero(bin(hex_data[6])[2:])
    bin_7_str = _fillZero(bin(hex_data[7])[2:])
    bin_str = f"{bin_0_str}{bin_1_str}{bin_2_str}{bin_3_str}{bin_4_str}{bin_5_str}{bin_6_str}{bin_7_str}"

    return bin_str


def _parseMsg(dbc_name, msg):
    msg_ts = msg.timestamp
    msg_id = hex(msg.arbitration_id)
    msg_data = msg.data
    
    msg_bits = _convertHexToBits(msg_data)

    DIR_PATH = dirname(dirname(realpath(__file__)))
    if dbc_name == 'huichuang':
        hc_dbc_path = join(DIR_PATH, "config", "default_huichuang_dbc.json")
        with open(hc_dbc_path, 'r') as f:
            hc_dbc = load(f)
            """
            timeArray = time.localtime(msg_ts)
            dt_new = time.strftime('%Y-%m-%d %H:%M:%S.%f')
            print(dt)
            """

            if msg_id == "0x6f8":
                start       = hc_dbc["0x6f8"]["warn_mode"]["start"]
                stop        = hc_dbc["0x6f8"]["warn_mode"]["stop"]
                fc          = hc_dbc["0x6f8"]["warn_mode"]["factor"]
                ofs         = hc_dbc["0x6f8"]["warn_mode"]["offset"]
                warn_mode   = int(msg_bits[start:stop], 2) * fc + ofs

                start   = hc_dbc["0x6f8"]["bsd_right"]["start"]
                stop    = hc_dbc["0x6f8"]["bsd_right"]["stop"]
                fc      = hc_dbc["0x6f8"]["bsd_right"]["factor"]
                ofs     = hc_dbc["0x6f8"]["bsd_right"]["offset"]
                rbsd    = int(msg_bits[start:stop], 2) * fc + ofs

                start   = hc_dbc["0x6f8"]["bsd_left"]["start"]
                stop    = hc_dbc["0x6f8"]["bsd_left"]["stop"]
                fc      = hc_dbc["0x6f8"]["bsd_left"]["factor"]
                ofs     = hc_dbc["0x6f8"]["bsd_left"]["offset"]
                lbsd    = int(msg_bits[start:stop], 2) * fc + ofs

                return ["ff", msg_ts, warn_mode, rbsd, lbsd]
            elif msg_id == "0x6fa":
                start   = hc_dbc["0x6fa"]["major_ver_id"]["start"]
                stop    = hc_dbc["0x6fa"]["major_ver_id"]["stop"]
                fc      = hc_dbc["0x6fa"]["major_ver_id"]["factor"]
                ofs     = hc_dbc["0x6fa"]["major_ver_id"]["offset"]
                maj_ver = int(msg_bits[start:stop], 2) * fc + ofs

                start   = hc_dbc["0x6fa"]["minor_ver_id"]["start"]
                stop    = hc_dbc["0x6fa"]["minor_ver_id"]["stop"]
                fc      = hc_dbc["0x6fa"]["minor_ver_id"]["factor"]
                ofs     = hc_dbc["0x6fa"]["minor_ver_id"]["offset"]
                min_ver = int(msg_bits[start:stop], 2) * fc + ofs

                start   = hc_dbc["0x6fa"]["stage_ver_id"]["start"]
                stop    = hc_dbc["0x6fa"]["stage_ver_id"]["stop"]
                fc      = hc_dbc["0x6fa"]["stage_ver_id"]["factor"]
                ofs     = hc_dbc["0x6fa"]["stage_ver_id"]["offset"]
                stg_ver = int(msg_bits[start:stop], 2) * fc + ofs

                return ["sw-ver", msg_ts, maj_ver, min_ver, stg_ver]
            elif msg_id=="0x500":
                start       = hc_dbc["0x500"]["frame_id"]["start"]
                stop        = hc_dbc["0x500"]["frame_id"]["stop"]
                fc          = hc_dbc["0x500"]["frame_id"]["factor"]
                ofs         = hc_dbc["0x500"]["frame_id"]["offset"]
                # change low-endian to big-endian
                low_endian_bits = msg_bits[start:stop]
                big_endian_bits = f"{low_endian_bits[24:32]}{low_endian_bits[16:24]}{low_endian_bits[8:16]}{low_endian_bits[0:8]}"
                frame_id    = int(big_endian_bits, 2) * fc + ofs

                start       = hc_dbc["0x500"]["frame_ts"]["start"]
                stop        = hc_dbc["0x500"]["frame_ts"]["stop"]
                fc          = hc_dbc["0x500"]["frame_ts"]["factor"]
                ofs         = hc_dbc["0x500"]["frame_ts"]["offset"]
                # change low-endian to big-endian
                low_endian_bits = msg_bits[start:stop]
                big_endian_bits = f"{low_endian_bits[24:32]}{low_endian_bits[16:24]}{low_endian_bits[8:16]}{low_endian_bits[0:8]}"

                frame_ts    = int(big_endian_bits, 2) * fc + ofs
                
                return ["detection-mem-id-ts", msg_ts, frame_id, frame_ts]
            elif msg_id=="0x501":
                start  = hc_dbc["0x501"]["range"]["start"]
                stop   = hc_dbc["0x501"]["range"]["stop"]
                fc     = hc_dbc["0x501"]["range"]["factor"]
                ofs    = hc_dbc["0x501"]["range"]["offset"]
                # change low-endian to big-endian
                low_endian_bits = msg_bits[start:stop]
                big_endian_bits = f"{low_endian_bits[8:16]}{low_endian_bits[0:8]}"
                rng    = int(big_endian_bits, 2) / fc + ofs

                start  = hc_dbc["0x501"]["doppler_vel"]["start"]
                stop   = hc_dbc["0x501"]["doppler_vel"]["stop"]
                fc     = hc_dbc["0x501"]["doppler_vel"]["factor"]
                ofs    = hc_dbc["0x501"]["doppler_vel"]["offset"]
                # change low-endian to big-endian
                low_endian_bits = msg_bits[start:stop]
                big_endian_bits = f"{low_endian_bits[8:16]}{low_endian_bits[0:8]}"
                doppler_vel = int(big_endian_bits, 2) / fc + ofs

                start  = hc_dbc["0x501"]["angle"]["start"]
                stop   = hc_dbc["0x501"]["angle"]["stop"]
                fc     = hc_dbc["0x501"]["angle"]["factor"]
                ofs    = hc_dbc["0x501"]["angle"]["offset"]
                # change low-endian to big-endian
                low_endian_bits = msg_bits[start:stop]
                big_endian_bits = f"{low_endian_bits[8:16]}{low_endian_bits[0:8]}"
                angle  = int(big_endian_bits, 2) / fc + ofs

                start  = hc_dbc["0x501"]["snr"]["start"]
                stop   = hc_dbc["0x501"]["snr"]["stop"]
                fc     = hc_dbc["0x501"]["snr"]["factor"]
                ofs    = hc_dbc["0x501"]["snr"]["offset"]
                # change low-endian to big-endian
                low_endian_bits = msg_bits[start:stop]
                big_endian_bits = f"{low_endian_bits[8:16]}{low_endian_bits[0:8]}"
                snr = int(big_endian_bits, 2) / fc + ofs

                return ["detection-mem-data", msg_ts, rng, doppler_vel, angle, snr]


def checkConnectStatusOfPeakCAN():
    return peakcan_bus.status_is_ok()


def switchStop(st_stop):
    global is_stop
    is_stop=st_stop


def writeCanMsg():
    global is_stop
    data_js = {
        "ff": {
            "ts": [],
            "warning_mode": [],
            "bsd_left_level": [],
            "bsd_right_level": []
        },
        "sw-ver": {
            "ts": [],
            "major": [],
            "minor": [],
            "stage": []
        },
        "det-mem-id-ts":{
            'ts':[],
            'frame-id':[],
            'frame-ts':[],
        },
        'det-mem-data':{
            'ts':[],
            'range':[],
            'doppler-vel':[],
            'angle':[],
            'snr':[]
        }
    }

    st_is_frame_id_aligned = False
    for msg in peakcan_bus:
        physical_data = _parseMsg('huichuang', msg)

        if physical_data[0] == "ff":
            data_js['ff']['ts'].append(physical_data[1])
            data_js['ff']['warning_mode'].append(physical_data[2])
            data_js['ff']['bsd_left_level'].append(physical_data[3])
            data_js['ff']['bsd_right_level'].append(physical_data[4])
        elif physical_data[0] == "sw-ver":
            data_js['sw-ver']['ts'].append(physical_data[1])
            data_js['sw-ver']['major'].append(physical_data[2])
            data_js['sw-ver']['minor'].append(physical_data[3])
            data_js['sw-ver']['stage'].append(physical_data[4])
        elif physical_data[0]=='detection-mem-id-ts':
            if not st_is_frame_id_aligned:
                st_is_frame_id_aligned = True
            data_js['det-mem-id-ts']['ts'].append(physical_data[1])
            data_js['det-mem-id-ts']['frame-id'].append(physical_data[2])
            data_js['det-mem-id-ts']['frame-ts'].append(physical_data[3])
        elif physical_data[0]=='detection-mem-data' and st_is_frame_id_aligned:
            data_js['det-mem-data']['ts'].append(physical_data[1])
            data_js['det-mem-data']['range'].append(physical_data[2])
            data_js['det-mem-data']['doppler-vel'].append(physical_data[3])
            data_js['det-mem-data']['snr'].append(physical_data[4])

        if is_stop:
            DIR_PATH = dirname(dirname(realpath(__file__)))
            cur_time = time.strftime("%Y-%m-%d %Hh-%Mm-%Ss", time.localtime(time.time()))
            data_store_path = join(DIR_PATH, "data", f"{cur_time}.json")
            with open(data_store_path, 'w') as f:
                dump(data_js, f)
            
            break


def readCanMsg():
    for msg in peakcan_bus:
        physical_data = _parseMsg('huichuang', msg)
        print(physical_data)


def printOneCanMsg():
    msg = peakcan_bus.recv()
    cmd_listener = Printer()
    cmd_listener.on_message_received(msg)
    _parseMsg('huichuang', msg)
    cmd_listener.stop()


def filterCanID():
    peakcan_bus.set_filters([
        # receive warning-message
        {
            "can_id": 0x6F8,
            "can_mask": 0xFFFFFFFF,
            "extended": False
        },
        # receive deftech sw version id message
        {
            "can_id": 0x6FA,
            "can_mask": 0xFFFFFFFF,
            "extended": False
        },
        # receive detections-mem-id-timestamp message
        {
            "can_id": 0x500,
            "can_mask": 0xFFFFFFFF,
            "extended": False
        },
        # receive detections-mem-data message
        {
            "can_id": 0x501,
            "can_mask": 0xFFFFFFFF,
            "extended": False
        },
    ])
