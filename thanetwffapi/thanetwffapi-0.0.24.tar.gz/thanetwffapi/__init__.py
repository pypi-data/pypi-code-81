name = "thanetwffapi"
__version__ = "0.0.24"


def parse_thanetwffapi_version(init_file_path: str) -> str:
    """ **Method parsing an __init__.py file and returns version as a string.**

    :param init_file_path: a relative path to an __init__.py file with version of a package
    :type init_file_path: str
    :return: string with version of a package
    """
    import io
    import re
    with io.open(init_file_path, "rt", encoding="utf8") as f:
        return re.search(r'__version__ = "(.*?)"', f.read()).group(1)
