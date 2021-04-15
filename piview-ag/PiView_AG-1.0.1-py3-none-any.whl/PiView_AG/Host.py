# Project:    PiView
# Filename:   Host.py
# Location:   ./PiView_AG
# Author:     Adrian Gould <adrian.gould@nmtafe.wa.edu.au>
# Created:    10/04/21
#
# This file provides the following features, methods and associated supporting
# code:
# - get boot time
# - get model
# - get revision
# - get serial
# - get uptime
#
# The following may be deprecated at some point:
# - name

from datetime import datetime, timedelta
from socket import gethostname
from sys import version_info

import psutil


class Host:
    @staticmethod
    def boot_time():
        """
        Determines the time the device was started

        :rtype: datetime
        :return: How long ago the Pi was booted
        """
        booted_at = datetime.fromtimestamp(psutil.boot_time())
        return booted_at

    @staticmethod
    def model():
        """
        Provide Pi Model Details

        Extracts the details from the device tree model file

        :rtype: string
        :return: The model name and other identifying details
        """
        try:
            my_model = open('/proc/device-tree/model').readline()
        except:
            my_model = "Error"

        return my_model

    @staticmethod
    def name():
        """
        Provides the host name to the user

        :rtype: string
        :return: The host name of the Pi
        """
        return gethostname()

    @staticmethod
    def python():
        """
        Get current Python version

        :rtype: string
        :return: A string containing the version of python that is being used
        """
        pythonv = '.'.join([str(x) for x in version_info[:3]])
        return pythonv

    @staticmethod
    def revision():
        """
        Provide board revision details

        The details are extracted from the cpu info file

        :rtype: string
        :return: The revision number of the Pi motherboard
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

    @staticmethod
    def serial():
        """
        Provide the Serial Number of the Pi CPU

        The details are extracted from the cpu info file

        :rtype: string
        :return: The Pi's serial number
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

    @staticmethod
    def uptime():
        """
        Determines the amount of time the device has been running for in
        seconds

        :rtype: float
        :return: The time that the Pi has been 'up' for
        """
        booted_at = Host.boot_time()
        current_at = datetime.now()
        uptime_seconds = (current_at - booted_at).total_seconds()
        uptime = timedelta(seconds=uptime_seconds)
        return uptime
