from ctypes import c_uint8, c_uint16, c_uint32, cast, pointer, POINTER
from ctypes import create_string_buffer, Structure
from fcntl import ioctl
import struct
import os
import sys
import time
import mmap
__all__ = ('led','i2c')
class WiFi:
    def __init__(self,ssid='null',pwd='null'):
        self.set_conf(ssid, pwd)
        self.init()
    def command(self,cmd):
        process = os.popen(cmd) # return file
        out = process.read()
        process.close()
        return out
    def is_exist(self):
        if self.command('cat /proc/net/dev|grep "wlan0"') == '':
            return False
        return True
    def enable(self):
        if self.command('ifconfig|grep "wlan0"') == '':
            self.command("ifconfig wlan0 up")
            return True
            
    def disable(self):
        if self.command('ifconfig|grep "wlan0"') != '':
            self.command("ifconfig wlan0 down")   
            return True
    def status(self):
        return self.command('ifconfig|grep "wlan0"') != ''
    def init(self):
        if self.is_exist() == False:
            self.command("insmod /ko/esp8089.ko")   
            timeout = 10
            while self.is_exist() == False and timeout > 0:
                time.sleep(0.5)
                timeout -= 1
            if self.is_exist() == False:
                print("load wifi driver fail.")
                return False
    def getip(self):
        return self.command("ifconfig wlan0|grep \"inet\"|awk \'{print $2}\'").replace('\n', '')
    def set_conf(self,ssid, pwd):
        conf = \
        "\
        ctrl_interface=/var/run/wpa_supplicant\n\
        \n\
        network={\n\
                ssid=\"%s\"\n\
                psk=\"%s\"\n\
                proto=WPA2\n\
        }\
        " %(ssid, pwd)  
        f = open("/etc/wifi.conf","w+")
        f.write(conf)
        f.close()
        return conf
    def connect(self):
        if self.getip() != '':
            return 
        if self.command("pidof wpa_supplicant") != '':
            self.command("pidof wpa_supplicant|xargs kill -9")
        if self.command("pidof udhcpc") != '':
            self.command("pidof udhcpc|xargs kill -9")
        self.disable()
        if self.status() == False:
            self.enable()
        self.command("wpa_supplicant -B -Dwext -iwlan0 -c /etc/wifi.conf &")
        self.command("udhcpc -iwlan0 &")
        timeout = 10
        while self.getip() == '' and timeout > 0:
            time.sleep(1)
            timeout -= 1
        if self.getip() == '':
            return False

class DevMemBuffer:
    """This class holds data for objects returned from DevMem class. It allows an easy way to print hex data"""

    def __init__(self, base_addr, data):
        self.data = data
        self.base_addr = base_addr

    def __len__(self):
        return len(self.data)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def hexdump(self, word_size = 4, words_per_row = 4):
        # Build a list of strings and then join them in the last step.
        # This is more efficient then concat'ing immutable strings.

        d = self.data
        dump = []

        word = 0
        while (word < len(d)):
            dump.append('0x{0:02x}:  '.format(self.base_addr
                                              + word_size * word))

            max_col = word + words_per_row
            if max_col > len(d): max_col = len(d)

            while word < max_col:
                # If the word is 4 bytes, then handle it and continue the
                # loop, this should be the normal case
                if word_size == 4:
                    dump.append(" {0:08x} ".format(d[word]))

                # Otherwise the word_size is not an int, pack it so it can be
                # un-packed to the desired word size.  This should blindly
                # handle endian problems (Verify?)
                elif word_size == 2:
                    for halfword in struct.unpack('HH', struct.pack('I',(d[word]))):
                        dump.append(" {0:04x}".format(halfword))

                elif word_size == 1:
                    for byte in struct.unpack('BBBB', struct.pack('I',(d[word]))):
                        dump.append(" {0:02x}".format(byte))

                word += 1

            dump.append('\n')

        # Chop off the last new line character and join the list of strings
        # in to a single string
        return ''.join(dump[:-1])

    def __str__(self):
        return self.hexdump()


class DevMem:
    """Class to read and write data aligned to word boundaries of /dev/mem"""

    # Size of a word that will be used for reading/writing
    word = 4
    mask = ~(word - 1)
    f = None

    def __init__(self, base_addr, length = 1, filename = '/dev/mem',
                 debug = 0):

        if base_addr < 0 or length < 0: raise AssertionError
        self._debug = debug

        self.base_addr = base_addr & ~(mmap.PAGESIZE - 1)
        self.base_addr_offset = base_addr - self.base_addr

        stop = base_addr + length * self.word
        if (stop % self.mask):
            stop = (stop + self.word) & ~(self.word - 1)

        self.length = stop - self.base_addr
        self.fname = filename

        # Check filesize (doesn't work with /dev/mem)
        #filesize = os.stat(self.fname).st_size
        #if (self.base_addr + self.length) > filesize:
        #    self.length = filesize - self.base_addr

        self.debug('init with base_addr = {0} and length = {1} on {2}'.
                format(hex(self.base_addr), hex(self.length), self.fname))

        # Open file and mmap
        self.f = os.open(self.fname, os.O_RDWR | os.O_SYNC)
        self.mem = mmap.mmap(self.f, self.length, mmap.MAP_SHARED,
                mmap.PROT_READ | mmap.PROT_WRITE,
                offset=self.base_addr)

    def __del__(self):
        if self.f:
            os.close(self.f)

    def read(self, offset, length):
        """Read length number of words from offset"""

        if offset < 0 or length < 0: raise AssertionError

        # Make reading easier (and faster... won't resolve dot in loops)
        mem = self.mem

        self.debug('reading {0} bytes from offset {1}'.
                   format(length * self.word, hex(offset)))

        # Compensate for the base_address not being what the user requested
        # and then seek to the aligned offset.
        virt_base_addr = self.base_addr_offset & self.mask
        mem.seek(virt_base_addr + offset)

        # Read length words of size self.word and return it
        data = []
        for i in range(length):
            data.append(struct.unpack('I', mem.read(self.word))[0])

        abs_addr = self.base_addr + virt_base_addr
        return DevMemBuffer(abs_addr + offset, data)


    def write(self, offset, din):
        """Write length number of words to offset"""

        if offset < 0 or len(din) <= 0: raise AssertionError

        self.debug('writing {0} bytes to offset {1}'.
                format(len(din) * self.word, hex(offset)))

        # Make reading easier (and faster... won't resolve dot in loops)
        mem = self.mem

        # Compensate for the base_address not being what the user requested
        # fix double plus offset
        #offset += self.base_addr_offset

        # Check that the operation is going write to an aligned location
        if (offset & ~self.mask): raise AssertionError

        # Seek to the aligned offset
        virt_base_addr = self.base_addr_offset & self.mask
        mem.seek(virt_base_addr + offset)

        # Read until the end of our aligned address
        for i in range(len(din)):
            self.debug('writing at position = {0}: 0x{1:x}'.
                        format(self.mem.tell(), din[i]))
            # Write one word at a time
            mem.write(struct.pack('I', din[i]))

    def debug_set(self, value):
        self._debug = value

    def debug(self, debug_str):
        if self._debug: print('DevMem Debug: {0}'.format(debug_str))

class devmem:
    def read(self, addr):
        mem = DevMem(addr&0xFFFF0000, 0xFFFF, "/dev/mem", 0)
        data = mem.read(addr&0x0000FFFF, 1)
        return data.data[0]
        
    def write(self, addr, val):
        mem = DevMem(addr&0xFFFF0000, 0xFFFF, "/dev/mem", 0)
        data = mem.write(addr&0x0000FFFF, [val])
        
class i2c_msg(Structure):
    """Linux i2c_msg struct."""
    _fields_ = [
        ("addr", c_uint16),
        ("flags", c_uint16),
        ("len", c_uint16),
        ("buf", POINTER(c_uint8)),
    ]
class i2c_rdwr_ioctl_data(Structure):  # pylint: disable=invalid-name
    """Linux i2c data struct."""
    _fields_ = [("msgs", POINTER(i2c_msg)), ("nmsgs", c_uint32)]


class LED:
    def __init__(self, pin=72):
        self._gpio = "/sys/class/gpio/gpio{0}".format(pin)
        if os.path.exists(self._gpio) == False: 
            self.open(self._gpio)
            self._pin = pin
            self.direction(self._gpio, "in")
    def open(self, pin):
        node = open("/sys/class/gpio/export", "w")
        node.write(str(pin))
        node.close()
    def direction(self, pin,inout):
        node = open("/sys/class/gpio/gpio{}/direction".format(pin), "w")
        node.write(inout)
        node.close()
    
    def on(self):
        self.direction(self._pin, "out")
    
    def off(self):
        self.direction(self._pin, "in")
        
class I2C:
    # ctypes versions of I2C structs defined by kernel.
    # Tone down pylint for the Python classes that mirror C structs.
    # pylint: disable=invalid-name,too-few-public-methods



    # pylint: enable=invalid-name,too-few-public-methods


    def __make_i2c_rdwr_data(self,messages):
        """Utility function to create and return an i2c_rdwr_ioctl_data structure
        populated with a list of specified I2C messages.  The messages parameter
        should be a list of tuples which represent the individual I2C messages to
        send in this transaction.  Tuples should contain 4 elements: address value,
        flags value, buffer length, ctypes c_uint8 pointer to buffer.
        """
        # Create message array and populate with provided data.
        msg_data_type = i2c_msg * len(messages)
        msg_data = msg_data_type()
        for i, message in enumerate(messages):
            msg_data[i].addr = message[0] & 0x7F
            msg_data[i].flags = message[1]
            msg_data[i].len = message[2]
            msg_data[i].buf = message[3]
        # Now build the data structure.
        data = i2c_rdwr_ioctl_data()
        data.msgs = msg_data
        data.nmsgs = len(messages)
        return data

    
    def __init__(self, bus=2, addr=0x12):
        # I2C C API constants (from linux kernel headers)
        self.__I2C_M_TEN = 0x0010  # this is a ten bit chip address
        self.__I2C_M_RD = 0x0001  # read data, from slave to master
        self.__I2C_M_STOP = 0x8000  # if I2C_FUNC_PROTOCOL_MANGLING
        self.__I2C_M_NOSTART = 0x4000  # if I2C_FUNC_NOSTART
        self.__I2C_M_REV_DIR_ADDR = 0x2000  # if I2C_FUNC_PROTOCOL_MANGLING
        self.__I2C_M_IGNORE_NAK = 0x1000  # if I2C_FUNC_PROTOCOL_MANGLING
        self.__I2C_M_NO_RD_ACK = 0x0800  # if I2C_FUNC_PROTOCOL_MANGLING
        self.__I2C_M_RECV_LEN = 0x0400  # length will be first received byte

        self.__I2C_SLAVE = 0x0703  # Use this slave address
        self.__I2C_SLAVE_FORCE = 0x0706  # Use this slave address, even if
        # is already in use by a driver!
        self.__I2C_TENBIT = 0x0704  # 0 for 7 bit addrs, != 0 for 10 bit
        self.__I2C_FUNCS = 0x0705  # Get the adapter functionality mask
        self.__I2C_RDWR = 0x0707  # Combined R/W transfer (one STOP only)
        self.__I2C_PEC = 0x0708  # != 0 to use PEC with SMBus
        self.__I2C_SMBUS = 0x0720  # SMBus transfer
        self.dev = None
        self.open(bus, addr)
    def open(self,bus=2, addr=0x12):
        self.close()
        mem = devmem()
        if bus == 0:
            self.sda_addr = 0x112C0030
            self.scl_addr = 0x112C0034
        elif bus == 1:
            self.sda_addr = 0x112C00A0
            self.scl_addr = 0x112C00A4
        elif bus == 2:
            self.sda_addr = 0x112C0038
            self.scl_addr = 0x112C003c
        val = mem.read(self.sda_addr)
        mem.write(self.sda_addr, (val &0xFFFFFFF0)|0x1)
        val = mem.read(self.scl_addr)
        mem.write(self.scl_addr, (val &0xFFFFFFF0)|0x1)
        self.dev = open("/dev/i2c-{0}".format(bus), "r+b", buffering=0)
        self.addr = addr
    def __del__(self):
        self.close()
    def close(self):
        if self.dev is not None:
            self.dev.close()
            self.dev = None
    def read(self, cmd):
        """Read a single byte from the specified cmd register of the device."""
        assert (
            self.dev is not None
        ), "Bus must be opened before operations are made against it!"
        # Build ctypes values to marshall between ioctl and Python.
        reg = c_uint8(cmd)
        result = c_uint8()
        # Build ioctl request.
        request = self.__make_i2c_rdwr_data(
            [
                (self.addr, 0, 1, pointer(reg)),  # Write cmd register.
                (self.addr, self.__I2C_M_RD, 1, pointer(result)),  # Read 1 byte as result.
            ]
        )
        # Make ioctl call and return result data.
        ioctl(self.dev.fileno(), self.__I2C_RDWR, request)
        return result.value
    def write(self, cmd, val):
        """Write a byte of data to the specified cmd register of the device.
        """
        assert (
            self.dev is not None
        ), "Bus must be opened before operations are made against it!"
        # Construct a string of data to send with the command register and byte value.
        data = bytearray(2)
        data[0] = cmd & 0xFF
        data[1] = val & 0xFF
        # Send the data to the device.
        ioctl(self.dev.fileno(), self.__I2C_SLAVE, self.addr & 0x7F)
        self.dev.write(data)
class QMA7981:
    def __init__(self):
        self.init()
    def init(self):
        self.i2c = I2C(2, 0x12)
        init_tab = [
            (0x11, 0x80),
            (0x36, 0xb6),
            (0xff, 50),
            (0x36, 0x00),
            (0x0f, 0x02),
            (0x10, 0xe1),		# ODR 130hz	
            #(0x4a, 0x08),		//Force I2C I2C s32erface.SPI is disabled,SENB can be used as ATB
            #(0x20, 0x05),	
            (0x11, 0x80),
            (0x5f, 0x80),		# enable test mode,take control the FSM
            (0x5f, 0x00),		#normal mode

            (0xff, 20),
            (0x10, 0xe1),
            (0x11, 0x80)
        ]
        for st in init_tab:
            reg = st[0]
            val = st[1]
            if reg == 0xff:
                time.sleep(val/1000)
                continue
            i2c.write(reg, val)
            time.sleep(2/1000)
    def read(self):
        num = []
        for i in range(1,7):
            num.append(i2c.read(i))
            #print(i,hex(num[i-1]))
        ax = (num[1]<<8)|(num[0])
        ay = (num[3]<<8)|(num[2])
        az = (num[5]<<8)|(num[4])
        res = {}
        res['x'] = ax 
        res['y'] = ay
        res['z'] = az
        return res
led = LED()
i2c = I2C()
accel = QMA7981()
    