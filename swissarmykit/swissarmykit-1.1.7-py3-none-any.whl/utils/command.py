import os
import subprocess
from swissarmykit.utils.bytesutils import BytesUtils

class Command:

    def __init__(self):
        pass

    @staticmethod
    def exec(command):
        ''' os.command("git --version") '''
        os.system(command)
        print('INFO: Execute ', command)
        return command


    @staticmethod
    def exec_output(commands, cwd=None): # type: (any, any) -> str
        ''' commands = ['wc', '-l', 'my_text_file.txt']

            err: UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 2: invalid
        '''
        commands = commands if isinstance(commands, list) else commands.split(' ')
        print('INFO: ', ' '.join(commands))
        if cwd:
            out = subprocess.Popen(commands, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        else:
            out = subprocess.Popen(commands, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        stdout, stderr = out.communicate()
        return stdout.decode('utf-8', 'slashescape')
        # return stdout.decode('utf-8')

if __name__ == '__main__':
    c = Command()
    # c.exec('mysqldump')
    # c.exec('which mongodump')
    # print(c.exec('dir'))
    print(c.exec_output(['C:/cygwin64/bin/ls.exe']))