from typing import Iterable, Tuple


def _archive_zip(output_path):
    """Return the file at the output_path as a zipfile."""
    import zipfile

    return zipfile.ZipFile(output_path, mode='w')


def archive_create(file_path, output_path, *, archive_name=None):
    """Archive the given file."""
    from d8s_file_system import file_name

    if archive_name is None:
        archive_name = file_name(file_path)

    with _archive_zip(output_path) as zipped_file:
        zipped_file.write(file_path, arcname=archive_name)


def _archive_unzip(archive_path):
    """Read the file at the archive_path as a zipfile."""
    import zipfile

    return zipfile.ZipFile(archive_path)


# TODO: I think the `archive_name` parameter should be changed to something like `file_name`
# TODO: I think the `file_path` parameter should be changed to something like `archive_path`
# TODO: we should probably allow an encoding to be passed in for decoding the zip contents
def archive_read(file_path, *, archive_name=None, password=None) -> Iterable[Tuple[str, str]]:
    """Read file(s) from the archive. If archive_name is given, read only that file; otherwise, read all files."""
    from d8s_strings import bytes_decode_as_string, string_encode_as_bytes

    if password:
        password = string_encode_as_bytes(password)

    with _archive_unzip(file_path) as unzipped_archive:
        if archive_name:
            yield archive_name, bytes_decode_as_string(unzipped_archive.read(archive_name, pwd=password))
        else:
            for file_name in unzipped_archive.namelist():
                yield file_name, bytes_decode_as_string(unzipped_archive.read(file_name, pwd=password))


# TODO: make a function out of this call: unzipped_archive.namelist()
