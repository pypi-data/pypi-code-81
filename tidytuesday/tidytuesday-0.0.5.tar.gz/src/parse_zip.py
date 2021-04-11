import zipfile
from io import BytesIO


def parse_zip(stream, parsers):
    files = {}
    with zipfile.ZipFile(stream, "r") as zip_ref:
        names = zip_ref.namelist()

        for f in names:
            dtype = f.split(".")[-1]
            name = f.split(".")[0]

            print(f"\t\t--- Unzipping {f} ---")

            files[name] = parsers[dtype](BytesIO(zip_ref.read(f)))

    return files
