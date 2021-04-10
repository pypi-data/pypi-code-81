"""
Project:    PiView
Filename:   Storage.py
Location:   ./PiView_AG
Author:     Adrian Gould <adrian.gould@nmtafe.wa.edu.au>
Created:    10/04/21
Purpose:
    This file provides the following features, methods and associated
    supporting code:
    - total ram and free ram (tuple)
    - total disk storage and free storage space (tuple)
    - disc storage for all disks connected to Pi (Total and Free) as a
    list/dictionary
"""
import subprocess


class Storage():
    def ram(self):
        """Provide the total RAM and free RAM to the user as a tuple

        :return Total, Free: tuple
        """
        # free -m
        output = subprocess.check_output(['free', '-m'])
        lines = output.splitlines()
        line = str(lines[1])
        ram = line.split()
        # total/free
        return ram[1], ram[3]

    def disc(self):
        """Provide the total disc space and the disc space that is free

        :return Total, Free: tuple
        """
        # df -h
        output = subprocess.check_output(['df', '-h'])
        lines = output.splitlines()
        line = str(lines[1])
        disk = line.split()
        # total/free
        return disk[1], disk[3]

    def all_discs(self):
        """Provide the user with the storage space (Total, Free) for each
        disc attached to the Pi as a dictionary.

        The dictionary will have:
            {
                "disc name" : total storage, free storage),
                ...
            }

        :return disc stats: dictionary of tuples
        """
        disc_stats = {}
        # For each disc:
        #   obtain free space and total space
        #   add "disk_name" :(total, free) to 'disc_stats' dictionary
        return disc_stats

    def disk(self):
        """Alias for disc()
        see :func:`~PiView_AG.Storage.disc`
        """
        return self.disc()

    def all_disks(self):
        """Alias for all_discs()
        see :func:`~PiView_AG.Storage.all_discs`
        """
        return self.all_discs()