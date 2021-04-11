import os

def create_directory(dir, raiseFileExists=False):
    try:
        os.mkdir(dir)
    except FileExistsError:
        if raiseFileExists:
            raise
    except OSError:
        raise

def get_script_location():
    """ 
    Returns the path to current file
    """
    return os.path.dirname(os.path.realpath(__file__))