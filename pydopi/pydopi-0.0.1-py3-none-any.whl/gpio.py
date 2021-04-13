import os
import csv
import pydopi.devmem as devmem 
class gpio:
    def __init__(self, num=None, config='config/pin.csv'):
        self._num = num
        self._cfg = None
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        cfg = curr_dir + os.sep + config
        self.get_config(cfg)
        self._gpio = "/sys/class/gpio/gpio{0}".format(self._pin)
        if os.path.exists(self._gpio) == False: 
            self.open(self._pin)
            self.direction(self._pin, "out")
    def get_config(self, config):
        with open(config, mode='r') as infile:
            reader = csv.DictReader(infile)
            for rows in reader:
                if rows['num'] == str(self._num) and rows['pin'][:4] == 'GPIO':
                    self._cfg = rows
                    self._pin = int(rows['pin'][4:])
                    self._reg_addr = int(rows['reg_addr'],16)
                    self._reg_val = int(rows['reg_val'],16)
                    devmem.write(self._reg_addr, self._reg_val)
                    break
    def open(self, pin):
        node = open("/sys/class/gpio/export", "w")
        node.write(str(pin))
        node.close()
    def direction(self, pin,inout):
        node = open("/sys/class/gpio/gpio{}/direction".format(pin), "w")
        node.write(inout)
        node.close()
    def set_value(self,val):
        self.direction(self._pin, "out")
        with open("/sys/class/gpio/gpio{}/value".format(self._pin), "w") as node:
            node.write(str(val))
            node.close()
    def get_value(self):
        self.direction(self._pin, "in")
        with open("/sys/class/gpio/gpio{}/value".format(self._pin), "r") as node:
            val = node.read()
            node.close()
            return val

