from io import BytesIO
import pysftp
import os
import tempfile


class SFTP:

    def __init__(self, host, user=None, password=None, port=22):
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        self.client = pysftp.Connection(host, username=user, password=password, port=port, cnopts=cnopts)

    def download(self, path, local_path=None):
        filename = os.path.basename(path)
        local_file_path = os.path.join(tempfile.gettempdir(), filename)
        if local_path is not None and os.path.isdir(local_path):
            local_file_path = os.path.join(local_path, filename)

        if not self.client.isfile(path):
            return False

        try:
            self.client.get(path, local_file_path)

            if not os.path.isfile(local_file_path):
                return False

            return local_file_path
        except Exception as e:
            print('[error] ', e)

            return False

    def retrieve(self, path):
        binary_content = BytesIO()
        if not self.client.isfile(path):
            print('[error] File "{}" does not exist on remote server'.format(path))
            return False

        try:
            self.client.getfo(path, binary_content)
        except Exception as e:
            print('[error] ', e)

            return False

        return binary_content

    def close(self):
        self.client.close()