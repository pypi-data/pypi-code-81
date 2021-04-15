# Project:    PiView
# Filename:   CPU.py
# Location:   ./PiView_AG
# Author:     Adrian Gould <adrian.gould@nmtafe.wa.edu.au>
# Created:    10/04/21
#
# This file provides the following features, methods and associated supporting
# code:
# - speed
# - maximum load
# - temperature

import subprocess

import psutil

from PiView_AG import Utils


class CPU:
    @staticmethod
    def speed():
        """
        Get the CPU frequency using the vcgencmd on Linux based systems

        :rtype: integer
        :return: The CPU frequency in MHz
        """
        try:
            output = subprocess.check_output(
                ['vcgencmd', 'get_config', 'arm_freq'])
            output = output.decode()
            lines = output.splitlines()
            line = lines[0]
            freq = line.split('=')
            freq = freq[1]
        except:
            freq = '0'
        return freq

    @staticmethod
    def max_load():
        """
        This function returns the maximum "CPU load" across all CPU cores,
        or a random value if the actual CPU load can't be determined.

        :rtype: float
        :return: The maximum CPU Load in range 0-100
        """
        if psutil is not None:
            return max(psutil.cpu_percent(percpu=True))
        else:
            return Utils.random_percentage()

    @staticmethod
    def temperature():
        """
        Requests the CPU temperature from the vcgencmd returning the
        result to the caller as a string with a floating point value to 2DP

        :rtype: float
        :return: The CPU temperature in Celcius
        """
        try:
            temp = subprocess.check_output(['vcgencmd', 'measure_temp'])
            temp = temp[5:-3]
        except:
            temp = '0.0'
        temp = round(temp, 2)
        return temp
