"""
Project:    PiView
Filename:   Network.py
Location:   ./PiView_AG
Author:     Adrian Gould <adrian.gould@nmtafe.wa.edu.au>
Created:    10/04/21
Purpose:
    This file provides the following features, methods and associated
    supporting code:
    - host name
    - interface names
    - ip addresses
    - mac addresses
"""
import os
from socket import gethostname


class Network:

    def host_name(self):
        """Provide the host name to the user

        :return:
        """
        # return platform.node()
        # return platform.uname()[1]
        return gethostname()

    def eth_name(self, type=None):
        """Provide the Ethernet interface name

        :param type: Options are: enx or eth
        :return: String
        """
        options = ['enx', 'eth']
        interface = None
        if type == 'w':
            options = ['wla']
        if type == 'l':
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

    def mac(self, interface='eth0'):
        """Provides the hardware MAC address for the interface requested

        Default is eth0

        :param interface: String, The interface name to query
        :return: String
        """
        # Return the MAC address of named Ethernet interface
        try:
            line = open('/sys/class/net/%s/address' % interface).read()
        except:
            line = "None"
        return line[0:17]

    def ip(self, interface='eth0'):
        """Provide IP Address from the named interface

        Default is eth0

        Uses the ifconfig command to create a text file, then processes this
        file to obtain the IP address.

        :param interface: String the interface to obtain the IP address for
        :return: String
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
