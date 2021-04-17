from pathlib import Path
from jhelper.encode import to_md5
from fsplit.filesplit import Filesplit
from shutil import copyfile
import csv


def _extract_timestamp(filename):
    name_only = filename.replace(".jpg", "")
    return name_only.split("_")[2]


def decode_file(filepath):
    chunk = Path(filepath)

    with chunk.open("r+b") as f:
        spliter = to_md5(_extract_timestamp(chunk.name))
        raw = f.read().split(spliter, 1)[1]
        f.seek(0)
        f.write(raw)
        f.truncate()


def decode_dir(dirpath, dest):
    files = []
    for chunk in Path(dirpath).iterdir():
        decode_file(chunk)
        files.append(chunk.name)

    files.sort()
    create_manifest(files, dirpath)
    _merge(dirpath, dest)


def _merge(dirpath, dest):
    fs = Filesplit()
    fs.merge(dirpath, output_file=dest)


def create_manifest(files, dirpath):
    csv_file = Path(dirpath) / "fs_manifest.csv"
    fieldnames = ["filename", "filesize", "encoding", "header"]
    with csv_file.open("w") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for file_ in files:
            writer.writerow(
                {"filename": file_, "filesize": 8000000, "encoding": "", "header": ""}
            )


class JDecoder:
    def __init__(self, source, dest):
        self.source = source
        self.dest = dest

    def decode(self):
        fpath = Path(self.source)
        if fpath.is_dir():
            decode_dir(fpath, self.dest)
        else:
            decode_file(self.source)
            copyfile(self.source, self.dest)
