# Project:    PiView
# Filename:   GPU.py
# Location:   ./PiView_AG
# Author:     Adrian Gould <adrian.gould@nmtafe.wa.edu.au>
# Created:    10/04/21
#
# This file provides the following features, methods and associated supporting
# code:
# - temperature

import subprocess


class GPU:
    @staticmethod
    def temperature():
        """
        Requests the GPU temperature from the thermal zone details

        :rtype: string
        :return: GPU temperature to 2DP
        """
        try:
            temp = subprocess.check_output(
                ['cat', '/sys/class/thermal/thermal_zone0/temp'])
            temp = float(temp) / 1000
        except:
            temp = 0.0
        temp = round(temp, 2)
        return temp
