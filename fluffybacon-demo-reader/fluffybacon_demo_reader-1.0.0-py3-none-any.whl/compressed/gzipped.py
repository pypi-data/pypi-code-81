import gzip
from .. util import writer

opener = gzip.open

if __name__ == '__main__':
    writer.main(opener)
