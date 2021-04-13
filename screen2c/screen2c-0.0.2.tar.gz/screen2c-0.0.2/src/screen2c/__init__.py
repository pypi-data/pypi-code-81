# Write your code here :-)
# -*- coding: utf-8 -*-
# Original code found at:
# https://gist.github.com/DenisFromHR/cc863375a6e19dce359d

"""screen2c 0.1, made by Denis Pleic and The Ginger.

|  Compiled, mashed and generally mutilated 2014-2015 by Denis Pleic
|  Made available under GNU GENERAL PUBLIC LICENSE
|
|  Modified Python I2C library for Raspberry Pi, as found on http://www.recantha.co.uk/blog/?p=4849
|  Joined existing 'i2c_lib.py' and 'lcddriver.py' into a single library
|  added bits and pieces from various sources
|  By DenisFromHR (Denis Pleic) 2015-02-10, ver 0.1
|
|  Code modified and packaged 2021 by The Ginger
|  Credit to everyone who had a hand in making the original
|  LONG LIVE LINUX
|  2021-04-12
"""

VERSION = "0.1"

# i2c bus (0 -- original Pi, 1 -- Rev 2 Pi)
import subprocess
if b"i2c-0" in subprocess.run(["ls", "/dev"], capture_output = True).stdout:
    I2CBUS = 0
else:
    I2CBUS = 1


import smbus
from time import sleep

class i2c_device:
    """
       :meta private:
    """
    def __init__(self, addr, port=I2CBUS):
       self.addr = addr
       self.bus = smbus.SMBus(port)

# Write a single command
    def write_cmd(self, cmd):
       self.bus.write_byte(self.addr, cmd)
       sleep(0.0001)

# Write a command and argument
    def write_cmd_arg(self, cmd, data):
       self.bus.write_byte_data(self.addr, cmd, data)
       sleep(0.0001)

# Write a block of data
    def write_block_data(self, cmd, data):
       self.bus.write_block_data(self.addr, cmd, data)
       sleep(0.0001)

# Read a single byte
    def read(self):
       return self.bus.read_byte(self.addr)

# Read
    def read_data(self, cmd):
       return self.bus.read_byte_data(self.addr, cmd)

# Read a block of data
    def read_block_data(self, cmd):
       return self.bus.read_block_data(self.addr, cmd)


# commands
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80

# flags for display entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# flags for display on/off control
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00

# flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

# flags for function set
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00

# flags for setBacklight control
LCD_BACKLIGHT = 0x08
LCD_NOBACKLIGHT = 0x00

En = 0b00000100 # Enable bit
Rw = 0b00000010 # Read/Write bit
Rs = 0b00000001 # Register select bit

class CursorMode():
    """An enum representing the cursor modes available on the display.

        :var NONE: No cursor
        :var LINE: A line cursor
        :var BLINK: A blinking block-shaped cursor.
    """
    NONE = LCD_CURSOROFF | LCD_BLINKOFF
    LINE = LCD_CURSORON | LCD_BLINKOFF
    BLINK = LCD_CURSOROFF | LCD_BLINKON

class Display:

    """The actual display.

        :var backlightOn: Whether or not the backlight is on. DO NOT SET THIS PROPERTY
        :param address: The hex address of the screen (Defaults to 0x27)
        :type address: hex, optional
    """
    def __init__(self, address = 0x27):
       self.lcd_device = i2c_device(address)
       self.setBacklightOn = True
       self.send(0x03)
       self.send(0x03)
       self.send(0x03)
       self.send(0x02)

       self.send(LCD_FUNCTIONSET | LCD_2LINE | LCD_5x8DOTS | LCD_4BITMODE)
       self.send(LCD_DISPLAYCONTROL | LCD_DISPLAYON)
       self.send(LCD_CLEARDISPLAY)
       self.send(LCD_ENTRYMODESET | LCD_ENTRYLEFT)
       sleep(0.2)
    def __del__(self):
       self.clear()
       self.send(LCD_DISPLAYCONTROL | LCD_DISPLAYOFF)
       self.setBacklight(False)

    # clocks EN to latch command
    def _lcd_strobe(self, data):
       self.lcd_device.write_cmd(data | En | LCD_BACKLIGHT)
       sleep(.0005)
       self.lcd_device.write_cmd(((data & ~En) | LCD_BACKLIGHT))
       sleep(.0001)

    def _send_four_bits(self, data):
       self.lcd_device.write_cmd(data | LCD_BACKLIGHT)
       self._lcd_strobe(data)


    # write a command to lcd
    def send(self, cmd, mode=0):
       self._send_four_bits(mode | (cmd & 0xF0))
       self._send_four_bits(mode | ((cmd << 4) & 0xF0))

    # write a character to lcd (or character rom) 0x09: setBacklight | RS=DR<
    # works!
    def _send_char(self, charvalue, mode=1):
       self._send_four_bits(mode | (charvalue & 0xF0))
       self._send_four_bits(mode | ((charvalue << 4) & 0xF0))

    # put string function with optional char positioning
    def write(self, string, line=1, pos=0):
        """Displays a string on the display.

            :param string: The text to display
            :type string: str
            :param line: The line number (Defaults to 1)
            :type line: int, optional
            :param pos: The position of the start of the string (Defaults to 0)
            :type pos: int, optional
        """
        if line == 1:
           pos_new = pos
        elif line == 2:
           pos_new = 0x40 + pos
        elif line == 3:
           pos_new = 0x14 + pos
        elif line == 4:
           pos_new = 0x54 + pos

        self.send(0x80 + pos_new)

        for char in string:
           self.send(ord(char), Rs)

        # clear lcd and set to home
    def clear(self):
        """Clear the display.
        """
        self.send(LCD_CLEARDISPLAY)
        self.send(LCD_RETURNHOME)

    def setCursor(self, mode):
        """Change the cursor mode.

            :param mode: The mode of the cursor.
            :type mode: screen2c.CursorMode
        """
        self.send(LCD_DISPLAYCONTROL | LCD_DISPLAYON | mode)
    def setBacklight(self, state):
        """Changes the state of the backlight.

            :param state: Whether or not the backlight is on.
            :type state: bool
        """
        if state:
            self.backlightOn = True
            self.lcd_device.write_cmd(LCD_BACKLIGHT)
        else:
            self.backlightOn = False
            self.lcd_device.write_cmd(LCD_NOBACKLIGHT)

        # add custom characters (0 - 7)
    def lcd_load_custom_chars(self, fontdata):
        self.send(0x40);
        for char in fontdata:
            for line in char:
                self._send_char(line)