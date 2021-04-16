try:
    import serial
except ImportError:
    raise ImportError('Please instal PySerial module')
import serial.tools.list_ports as list_ports
import sys
TIMEOUT = 0.1


def _search(pid, vid, rate):
    sp=serial.Serial(timeout=0.5)
    sp.baudrate= rate
    ports =list_ports.comports()
    for p  in ports:
        if not hasattr(p,'pid'):
            continue
        if not hasattr(p,'vid'):
            continue
        if (p.pid==pid)and(p.vid==vid):
            sp.port=str(p.device)
            return sp
    else:
        return None
def _open():
    ser=_search(516, 3368, 115200)
    if ser is None:
        raise OSError('Unable to connect to microbit')
    ser.open()
    return ser 
class Microbit:
    def __init__(self):
        self._ser=_open()
        self._stout=None
        self._stin=None
    def read(self):
        return self._ser.read()
    def readline(self):
        return self._ser.readline()
    def write(self,what):
        return self._ser.write(what)
    def writelines(self,lines):
        return sel._ser.writelines(lines)
    def stio_replace(self):
        self._stout=sys.stdout
        self._stin=sys.stdin
        sys.stdout=self
        sys.stdin=self
    def rstio(self):
        if (self._stout is None) or (self._stout is None):
            raise LookupError(
                'nothing to reset')
        sys.stdout=self._stout
        sys.stdin=self._stin
    def __iter__(self):
        return self
    def __next__(self):
        m=self._ser.readline()
        if m==b'\x00':
            raise StopIteration
        return m.decode('utf-8').replace('\n','')

