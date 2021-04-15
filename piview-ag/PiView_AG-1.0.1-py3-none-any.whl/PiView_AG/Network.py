# Project:    PiView
# Filename:   Network.py
# Location:   ./PiView_AG
# Author:     Adrian Gould <adrian.gould@nmtafe.wa.edu.au>
# Created:    10/04/21
#
# This file provides the following features, methods and associated
# supporting code:
# - host name
# - interface names
# - ip addresses
# - mac addresses

import os
from socket import gethostname


class Network:
    @staticmethod
    def host_name():
        """Provide the host name to the user

        :rtype: string
        :return: The host name of the Pi
        """
        # return platform.node()
        # return platform.uname()[1]
        return gethostname()

    @staticmethod
    def eth_name(_type=None):
        """Provide the Ethernet interface name

        :param _type: string, possible options are: enx or eth
        :rtype: string
        :return: The network interface name
        """
        options = ['enx', 'eth']
        interface = None
        if _type == 'w':
            options = ['wla']
        if _type == 'l':
            options = ['lo']
        try:
            for root, dirs, files in os.walk('/sys/class/net'):
                for dir in dirs:
                    for option in options:
                        if dir[:3] == option:
                            interface = dir
        except:
            interface = "None"
        return interface

    @staticmethod
    def mac(interface='eth0'):
        """Provides the hardware MAC address for the interface requested

        Default is eth0

        :param interface: string, the interface name to query
        :rtype: string
        :return: Mac address of the selected interface
        """
        # Return the MAC address of named Ethernet interface
        try:
            line = open('/sys/class/net/%s/address' % interface).read()
        except:
            line = "None"
        return line[0:17]

    @staticmethod
    def ip(interface='eth0'):
        """Provide IP Address from the named interface

        Default is eth0

        Uses the ifconfig command to create a text file, then processes this
        file to obtain the IP address.

        :param interface: string, the interface to obtain the IP address for
        :rtype: string
        :return: IPv4 address of the selected interface
        """
        try:
            filename = 'ifconfig_' + interface + '.txt'
            os.system('ifconfig ' + interface + ' > /home/pi/' + filename)
            f = open('/home/pi/' + filename, 'r')
            skip_line = f.readline()  # skip 1st line
            line = f.readline()  # read 2nd line
            line = line.strip()
            f.close()

            if line.startswith('inet '):
                a, b, c = line.partition('inet ')
                a, b, c = c.partition(' ')
                a = a.replace('addr:', '')
            else:
                a = 'None'

            return a

        except:
            return 'Error'
