import ctypes
lib = ctypes.CDLL("./libpycall.so")
lib.my_calculate.restype = ctypes.c_double

o = lib.test_new()
res = lib.my_calculate(o, ctypes.c_int(23), ctypes.c_double(23.4))
print('res', res)
