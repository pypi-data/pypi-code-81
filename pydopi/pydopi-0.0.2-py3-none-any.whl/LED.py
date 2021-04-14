import os
class LED(object):
    RED     = 0
    BLUE    = 1
    GREEN   = 2
    def __init__(self, color=0):
        self.RED     = 0
        self.BLUE    = 1
        self.GREEN   = 2
        self._red_pin = 72
        self._blue_pin = 4
        self._green_pin = 73
        if color == self.RED:    
            self.color = self.RED
        elif color == self.BLUE:
            self.color = self.BLUE
        elif color == self.GREEN:
            self.color = self.GREEN
        self._red_led = "/sys/class/gpio/gpio{0}".format(72)
        self._blue_led = "/sys/class/gpio/gpio{0}".format(4)
        self._green_led = "/sys/class/gpio/gpio{0}".format(73)
        if os.path.exists(self._red_led) == False: 
            self.open(self._red_pin)
            self.direction(self._red_pin, "in")
        if os.path.exists(self._blue_led) == False:
            self.open(self._blue_pin)
            self.direction(self._blue_pin, "in")
        if os.path.exists(self._green_led) == False:
            self.open(self._green_pin)
            self.direction(self._green_pin, "in")
    def open(self, pin):
        node = open("/sys/class/gpio/export", "w")
        node.write(str(pin))
        node.close()
    def direction(self, pin,inout):
        node = open("/sys/class/gpio/gpio{}/direction".format(pin), "w")
        node.write(inout)
        node.close()
    
    def on(self, color=0):
        if color == self.RED:
            self.direction(self._blue_pin, "in")
            self.direction(self._green_pin, "in")
            self.direction(self._red_pin, "out")
        elif color == self.BLUE:
            self.direction(self._red_pin, "in")
            self.direction(self._green_pin, "in")
            self.direction(self._blue_pin, "out")
        elif color == self.GREEN:
            self.direction(self._red_pin, "in")
            self.direction(self._blue_pin, "in")
            self.direction(self._green_pin, "out")
    
    def off(self, color=0):
        self.direction(self._red_pin, "in")
        self.direction(self._blue_pin, "in")
        self.direction(self._green_pin, "in")