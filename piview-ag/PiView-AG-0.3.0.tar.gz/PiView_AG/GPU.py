import subprocess

import psutil

from PiView_AG.Utils import random_percentage


class GPU:
    def temperature(self):
        """
        Requests the GPU temperature from the thermal zone details

        :return string: GPU temperature to 2DP
        """
        # Extract CPU temp
        try:
            temp = subprocess.check_output(
                ['cat', '/sys/class/thermal/thermal_zone0/temp'])
            temp = float(temp) / 1000
        except:
            temp = 0.0
        temp = round(temp,2)
        return temp

