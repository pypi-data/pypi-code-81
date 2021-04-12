""" test of FPCVTMuxInOut

    tests close to the limit of the target output
"""

from ieee754.fcvt.pipeline import (FPCVTDownMuxInOut,)
from ieee754.fpcommon.test.fpmux import runfp
from ieee754.fcvt.test.rangelimited import (create_ranged_fp16,
                                            create_ranged_min_fp16,
                                            create_ranged_min_normal_fp16,
                                            create_ranged_fp32,
                                            create_ranged_min_fp32,
                                            create_ranged_min_normal_fp32)

from sfpy import Float64, Float32, Float16


import unittest

def fcvt_16(x):
    return Float16(x)

def fcvt_32(x):
    return Float32(x)

def test_down_pipe_fp32_16():
    dut = FPCVTDownMuxInOut(32, 16, 4)
    vals = []
    for i in range(100):
        vals.append(create_ranged_fp16(Float32))
        vals.append(create_ranged_min_fp16(Float32))
        vals.append(create_ranged_min_normal_fp16(Float32))
    runfp(dut, 32, "test_fcvt_down_pipe_fp32_16_ranged", Float32, fcvt_16, True,
            vals=vals)

def test_down_pipe_fp64_16():
    dut = FPCVTDownMuxInOut(64, 16, 4)
    vals = []
    for i in range(100):
        vals.append(create_ranged_fp16(Float64))
        vals.append(create_ranged_min_fp16(Float64))
        vals.append(create_ranged_min_normal_fp16(Float64))
    runfp(dut, 64, "test_fcvt_down_pipe_fp64_16_ranged", Float64, fcvt_16, True,
            vals=vals)

def test_down_pipe_fp64_32():
    dut = FPCVTDownMuxInOut(64, 32, 4)
    vals = []
    for i in range(100):
        vals.append(create_ranged_fp32(Float64))
        vals.append(create_ranged_min_fp32(Float64))
        vals.append(create_ranged_min_normal_fp32(Float64))
    runfp(dut, 64, "test_fcvt_down_pipe_fp64_32_ranged", Float64, fcvt_32, True,
            vals=vals)

if __name__ == '__main__':
    for i in range(200):
        test_down_pipe_fp64_16()
        test_down_pipe_fp32_16()
        test_down_pipe_fp64_32()

