# Imports
import os
import time


def delete_old_files(folder: str, ageTime: int) -> str:
    """
    Function for deleting old files
    :param folder: path to folder
    :param ageTime: time to control
    :return: logs: result of function
    """
    logs = ''
    global TOTAL_DELETED_FILE
    global TOTAL_DELETED_SIZE
    for path, dirs, files in os.walk(folder):
        for file in files:
            fileName = os.path.join(path, file)  # get Full path to file
            fileTime = os.path.getmtime(fileName)
            if fileTime < ageTime:
                sizeFile = os.path.getsize(fileName)
                TOTAL_DELETED_SIZE += sizeFile
                TOTAL_DELETED_FILE += 1
                logs += f"Deleting file: {fileName}" + '\n'
                os.remove(fileName)
    return logs


def delete_empty_dir(folder: str, logs: str) -> str:
    """
    Function for deleting empty folders
    :param folder: path to folder
    :param logs: early logs
    :return: logs: new logs
    """
    logs_in = logs
    global TOTAL_DELETED_DIRS
    empty_folders_in_this_run = 0
    for path, dirs, files in os.walk(folder):
        if not dirs and not files:
            TOTAL_DELETED_DIRS += 1
            empty_folders_in_this_run += 1
            logs_in += f"Deleting empty dir: {path}" + '\n'
            os.rmdir(path)
    if empty_folders_in_this_run > 0:
        delete_empty_dir(folder, logs_in)
    return logs_in


# Some constants
TOTAL_DELETED_SIZE = 0  # Total deleted size of all files
TOTAL_DELETED_FILE = 0  # Total deleted files
TOTAL_DELETED_DIRS = 0  # Total deleted empty folders


def cleaner(FOLDERS=None, DAYS=None):
    """
    Main function of cleaning
    :param FOLDERS: list of folders
    :param DAYS: number of days
    :return: nothin to return
    """
    if not isinstance(FOLDERS, list):
        raise TypeError('Folders must be as list')
    if not DAYS:
        raise NameError('Enter the limit of the days')
    logs = ''
    nowTime = time.time()                         # Get current time in seconds
    ageTime = nowTime - 60 * 60 * 24 * int(DAYS)  # Minus DAYS in seconds
    starttime = time.asctime()
    for folder in FOLDERS:
        logs += delete_old_files(folder, ageTime)      # Delete old files
        logs += delete_empty_dir(folder, '')           # Delete empty folders
    finishtime = time.asctime()

    print(f'START TIME: {starttime}')
    print(f'Total deleted size: {TOTAL_DELETED_SIZE/1024/1024} MB')
    print(f'Total deleted files: {TOTAL_DELETED_FILE}')
    print(f'Total deleted empty folders: {TOTAL_DELETED_DIRS}')
    print(f'FINISH TIME: {finishtime}')

    f = open('./logs.txt', 'w')
    f.write(logs)
    f.close()
