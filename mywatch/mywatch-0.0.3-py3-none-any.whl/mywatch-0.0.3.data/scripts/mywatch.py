#!python

import sys
import subprocess
import checksumdir
from time import sleep


_dir = sys.argv[1]
command = sys.argv[2]


subprocess.run(command, shell=True)

dirhash = checksumdir.dirhash(_dir)


if __name__ == '__main__':
    while True:
        sleep(1)
        new_hash = checksumdir.dirhash(_dir)
        if new_hash != dirhash:
            print(f"Change detected, new hash: {new_hash}")
            dirhash = new_hash
            subprocess.run(command, shell=True)
