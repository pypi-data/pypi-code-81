import serial

ser = None

def open_fpga(port, baud = None, timeout=2.0):
    global ser

    if baud == None:
        baud = 1000000
    ser = serial.Serial(port, baud, timeout=timeout)
    return ser

def call_fpga(size, count):
    global ser

    if not ser:
        raise Exception('FPGA I/O not open')

    ser.write(b' ')
    buf = bytearray()
    for i in range(count):
        x = ser.read(size)
        if len(x) == size:
            buf.extend(x)
        else:
            break
    return bytes(buf)

def read_fpga(size, count):
    global ser

    if not ser:
        raise Exception('FPGA I/O not open')

    buf = bytearray()
    for i in range(count):
        x = ser.read(size)
        if len(x) == size:
            buf.extend(x)
        else:
            break
    return bytes(buf)

def stop_fpga(flush):
    global ser

    if not ser:
        raise Exception('FPGA I/O not open')

    ser.write(b'!')
    if flush:
        flushed = 0
        while len(ser.read()):
            flushed += 1
        print(flushed, 'flushed')

def close_fpga():
    if ser:
        ser.close()
