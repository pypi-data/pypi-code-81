# imports
from datetime import datetime
import os
import shutil
import zipfile


def convert_date(timestamp: datetime) -> str:
    """
    Function for converting time from timestamp
    :param timestamp: file timestamp
    :return: formated_date: this time in better format
    """
    d = datetime.utcfromtimestamp(timestamp)
    formated_date = d.strftime('%d %b %Y, %H %M')
    return formated_date


def create_zip(files=None, path=None):
    """
    Create zip-archive from files in path
    :param files: list of files paths
    :param path: path where to create zip-archive
    :return: nothing to return
    """
    if not files or not path:
        raise NameError('Required list of files and path')
    with zipfile.ZipFile(path, 'a') as new_zip:
        for name in files:
            new_zip.write(name)


def files_in_zip(path=None) -> list:
    """
    Function that returns list of files from archive
    :param path: path to zip-archive
    :return: list of files in archive
    """
    if not path:
        raise NameError('Required path to archive')
    with zipfile.ZipFile(path, 'r') as zipobj:
        return zipobj.namelist()


def read_zip(path=None):
    """
    Function that prints information about archive
    :param path: path to zip-archive
    :return: nothing to return
    """
    if not path:
        raise NameError('Required path to archive')
    with zipfile.ZipFile(path, 'r') as zipobj:
        files = zipobj.namelist()
        for file_ in files:
            bar_info = zipobj.getinfo(file_)
            print(f"""{bar_info.filename}\t
            Compress size: {int(bar_info.compress_size) / 1024} in KB\t
            Filesize: {int(bar_info.file_size) / 1024} in KB""")


def extract(path_to_zip=None, path_to_file=None):
    """
    Function that extracts files from archive
    :param path_to_zip: path to zip-archive
    :param path_to_file: path to file in zip-archive
    :return: nothing to return
    """
    if not path_to_file or not path_to_zip:
        raise NameError('Required path to both arguments')
    data_zip = zipfile.ZipFile(path_to_zip, 'r')
    if path_to_file:
        data_zip.extract(path_to_file)
    else:
        data_zip.extractall(path='extract_dir/')
    data_zip.close()


def read_file(path=None) -> str:
    """
    Function for reading the single file
    :param path: path to the file
    :return: data: data from the file
    """
    if not path:
        raise NameError('Required path to the file')
    with open(path, 'r') as f:
        data = f.read()
    return data


def write_file(path=None, data=None):
    """
    Function for writing data in the single file
    :param path: path to the file
    :param data: data needs be in the file
    :return: nothing to return
    """
    if not path or not data:
        raise NameError('Required path to the file and data')
    with open(path, 'w') as f:
        f.write(str(data))


def list_dir(path=None) -> list:
    """
    Function that returns list of dirs
    :param path: path to the dir
    :return: dirs: list of the dirs
    """
    if not path:
        raise NameError('Required path to dir')
    dirs = []
    for entry in os.listdir(path):
        if os.path.isdir(os.path.join(path, entry)):
            dirs.append(entry)
    return dirs


def get_files(path: str) -> list:
    """
    Function that returns list of files
    :param path: path to the dir
    :return: files: list of the files
    """
    if not path:
        raise NameError('Required path to dir')
    files = []
    dir_entries = os.scandir(path)
    for entry in dir_entries:
        if entry.is_file():
            info = entry.stat()
            files.append({
                'name': entry.name,
                'date': info.st_mtime,
                'date_str': convert_date(info.st_mtime),
            })
    return files


def sync(path_a=None, path_b=None):
    """
    Main function for synchronize two folders
    :param path_a: path to the first directory
    :param path_b: path to the second directory
    :return: nothing to return
    """
    if not path_a or not path_b:
        raise NameError('Required path to both dirs')
    logs = ''
    files_in_a = get_files(path_a)
    files_in_b = get_files(path_b)
    same_files = []
    for file_a in files_in_a:
        for file_b in files_in_b:
            if file_b['name'] == file_a['name']:
                # compare dates
                if file_b['date'] < file_a['date']:
                    # change
                    shutil.copy2(path_a + '/' + file_a['name'], path_b)
                    logs += f"Change {file_a['name']} in {path_b}" + '\n'
            same_files.append(file_b['name'])
    for file_a in files_in_a:
        if not file_a['name'] in same_files:
            # move to b
            shutil.copy2(path_a + '/' + file_a['name'], path_b)
            logs += f"Create {file_a['name']} in {path_b}" + '\n'

    write_file('./logs.txt', logs)


def files(path=None):
    """
    Function that prints list of files and their last modified date
    :param path: path to the directory
    :return: nothing to return
    """
    files = get_files(path)
    for file_ in files:
        print(f"{file_['name']}\t Last Modified: {file_['date_str']}")


def dirs(path: str):
    """
    Function that prints list of dirs
    :param path: path to the directory
    :return: nothing to return
    """
    dirs = list_dir(path)
    for dir_ in dirs:
        print(dir_)
