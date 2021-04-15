from tarfile import TarFile


def tar_json_generator(tar_file: TarFile):
    for f in tar_file:
        if not (f.name.endswith("json")):
            continue
        yield json.load(tar_file.extractfile(f))
