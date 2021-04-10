"""
Project:    PiView
Filename:   Host.py
Location:   ./PiView_AG
Author:     Adrian Gould <adrian.gould@nmtafe.wa.edu.au>
Created:    10/04/21
Purpose:
    This file provides the following features, methods and associated
    supporting code:
    - get boot time
    - get model
    - get revision
    - get serial
    - get uptime

    The following are yet to be implemented fully:
    - name
    
"""
from datetime import datetime, timedelta
from socket import gethostname
from sys import platform

import psutil


class Host():

    def boot_time(self):
        """Determines the time the device was started

        :return: datetime
        """
        booted_at = datetime.fromtimestamp(psutil.boot_time())
        return booted_at

    def model(self):
        """Provide Pi Model Details

        Extracts the details from the device tree model file

        :return:
        """
        try:
            my_model = open('/proc/device-tree/model').readline()
        except:
            my_model = "Error"

        return my_model

    def name(self):
        """Provides the host name to the user

        :return: String
        """
        return gethostname()

    def get_python():
        """Get current Python version

        :return: string
        """
        pythonv = platform.python_version()
        return pythonv

    def revision(self):
        """Provide board revision details

        The details are extracted from the cpu info file

        :return: string
        """
        my_revision = "Error"
        try:
            f = open('/proc/cpuinfo', 'r')
            for line in f:
                if line[0:8] == 'Revision':
                    my_revision = line[11:-1]
            f.close()
        except:
            my_revision = "Error"

        return my_revision

    def serial(self):
        """Provide the Serial Number of the Pi CPU

        The details are extracted from the cpu info file

        :return: string
        """
        my_cpu_serial = "Error"
        try:
            f = open('/proc/cpuinfo', 'r')
            for line in f:
                if line[0:6] == 'Serial':
                    my_cpu_serial = line[10:26]
            f.close()
        except:
            my_cpu_serial = "Error"

        return my_cpu_serial

    def uptime(self):
        """Determines the amount of time the device has been running for in
        seconds

        :return: seconds (float)
        """
        booted_at = self.boot_time()
        current_at = datetime.now()
        uptime_seconds = (current_at - booted_at).total_seconds()
        uptime = timedelta(seconds=uptime_seconds)
        return uptime
