# Project:    PiView
# Filename:   Hardware.py
# Location:   ./PiView_AG
# Author:     Adrian Gould <adrian.gould@nmtafe.wa.edu.au>
# Created:    10/04/21
#
# This file provides the following features, methods and associated supporting
# code:
# - bt (Bluetooth status)
# - camera (camera status)
# - spi (SPI Bus status)
# - i2c (I2C status)

import subprocess


class Hardware:
    @staticmethod
    def bt():
        """
        Check if Bluetooth module is enabled

        :rtype: boolean
        :return: True|False
        """
        bt = False
        try:
            c = subprocess.Popen("lsmod", stdout=subprocess.PIPE)
            gr = subprocess.Popen(["grep", "bluetooth"], stdin=c.stdout,
                                  stdout=subprocess.PIPE)
            output = gr.communicate()[0]
            if output[:9] == 'bluetooth':
                bt = True
        except:
            pass
        return bt

    @staticmethod
    def spi():
        """
        Check if SPI bus is enabled by checking for spi_bcm2 modules

        :rtype: boolean
        :return: True|False
        """
        spi = False
        try:
            c = subprocess.Popen("lsmod", stdout=subprocess.PIPE)
            gr = subprocess.Popen(["grep", "spi_bcm2"], stdin=c.stdout,
                                  stdout=subprocess.PIPE)
            output = gr.communicate()[0]
            if output[:8] == 'spi_bcm2':
                spi = True
        except:
            pass
        return spi

    @staticmethod
    def i2c():
        """
        Check if I2C bus is enabled by checking for i2c_bcm2 modules

        :rtype: boolean
        :return: True|False
        """
        i2c = False
        try:
            c = subprocess.Popen("lsmod", stdout=subprocess.PIPE)
            gr = subprocess.Popen(["grep", "i2c_bcm2"], stdin=c.stdout,
                                  stdout=subprocess.PIPE)
            output = gr.communicate()[0]
            if output[:8] == 'i2c_bcm2':
                i2c = True
        except:
            pass
        return i2c

    @staticmethod
    def camera():
        """
        Check if camera is enabled and present

        :rtype: dictionary
        :return: Details in form {"supported": boolean, "detected": boolean}
        """
        camera = {"supported": None, "detected": None}
        try:
            c = subprocess.Popen(["/opt/vc/bin/vcgencmd", "get_camera"],
                                 stdout=subprocess.PIPE)
            output = c.communicate()[0]
            supported = output[10] == ord("1")
            detected = output[21] == ord("1")
            camera = {"supported": supported, "detected": detected}
        except:
            pass
        return camera
