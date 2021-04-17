from fsplit.filesplit import Filesplit
from tempfile import TemporaryDirectory


def splite2chunks(filepath):
    fs = Filesplit()
    temp_dir = TemporaryDirectory()
    print(temp_dir.name)
    fs.split(file=filepath, split_size=8688608, output_dir=temp_dir.name)
    return temp_dir
