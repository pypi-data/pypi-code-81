import subprocess

import psutil

from PiView_AG.Utils import random_percentage


class CPU:
    def speed(self):
        """
            Get the CPU frequency using the vcgencmd on Linux based systems

            :return: integer
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

    def max_load(self):
        """
            This function returns the maximum "CPU load" across all CPU cores,
            or a random value if the actual CPU load can't be determined.

            :return float: Actual CPU load if available, else a random CPU load
            """
        if psutil is not None:
            return max(psutil.cpu_percent(percpu=True))
        else:
            return random_percentage()

    def temperature(self):
        """
        Requests the CPU temperature from the vcgencmd returning the
        result to the caller as a string with a floating point value to 2DP

        :return float: CPU temperature to 2DP
        """
        # Extract CPU temp
        try:
            temp = subprocess.check_output(['vcgencmd', 'measure_temp'])
            temp = temp[5:-3]
        except:
            temp = '0.0'
        temp = round(temp,2)
        return temp
