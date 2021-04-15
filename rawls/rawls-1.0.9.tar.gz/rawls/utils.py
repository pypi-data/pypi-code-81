"""Utils function for .rawls file
"""


# utils functions
def check_file_paths(filepaths):
    """check filepaths input extension
    
    Arguments:
        filepaths: {[str]} -- image filepaths list
    
    Raises:
        Exception: Invalid input filepaths extension
    """

    if isinstance(filepaths, list):
        for p in filepaths:
            check_file_paths(p)
    else:
        if not '.rawls' in filepaths:
            raise Exception('Unvalid input filepath images, need .rawls image')