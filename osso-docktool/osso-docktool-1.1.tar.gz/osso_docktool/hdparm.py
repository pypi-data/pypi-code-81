import subprocess

__author__ = 'osso'


class HdparmParser(object):
    def __init__(self, devname):
        self._rawdata = subprocess.check_output(
            ['/sbin/hdparm', '-I', devname]).decode('utf-8')

    def get_security_info(self):
        if 'Security' in self._rawdata:
            lines = self._rawdata.split('\n')
            security_info = {}
            do_collect = False
            for line in lines:
                if do_collect:
                    if not line.startswith('\t'):
                        do_collect = False
                    else:
                        splitted = line.split('\t')
                        if (len(splitted) == 3 and
                                'master password' not in splitted[1].lower()):
                            security_info[splitted[2]] = (
                                splitted[1].lower() != 'not')
                elif line.startswith('Security'):
                    do_collect = True
            return security_info
        return None
