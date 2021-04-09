from ftplib import FTP as FTPSession
from io import BytesIO
import tempfile
import os


class FTP:

    def __init__(self, host, user=None, password=None, port=21):
        self.client = FTPSession()
        self.client.connect(host, port)
        if user is not None and password is not None:
            self.client.login(user, password)

    def download(self, path, local_path=None):
        directory = os.path.dirname(path)
        filename = os.path.basename(path)
        local_file_path = os.path.join(tempfile.gettempdir(), filename)

        if local_path is not None and local_path != '':
            if os.path.isdir(local_path):
                local_file_path = os.path.join(local_path, filename)

        if directory != '':
            self.client.cwd(directory)
        
        try:
            output = self.client.retrbinary('RETR ' + filename, open(local_file_path, 'wb').write)
            if not output.startswith('226'):
                # raise Exception('[error] Could not download file from FTP')
                print('[error] Could not download file')
                print('[error] Output: {}'.format(output))

                return False

            return local_file_path
        except Exception as e:
            # raise Exception('[error] ', e)
            print('[error] ', e)

            return False

    def retrieve(self, path):
        directory = os.path.dirname(path)
        filename = os.path.basename(path)

        if directory != '':
            self.client.cwd(directory)
        
        try:
            binary_content = BytesIO()
            cmd = 'RETR {}'.format(filename)
            self.client.retrbinary(cmd, binary_content.write)

            return binary_content
        except Exception as e:
            print('[error] ', e)

            return False

    def close(self):
        self.client.close()
