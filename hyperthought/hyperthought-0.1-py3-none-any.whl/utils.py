import os
import platform


ID_PATH_SEP = ','
PATH_SEP = '/'
WINDOWS_PATH_PREFIX = '//?/'
FOLDER_TYPE = 'Folder'


class InvalidMetadataFormatException(Exception):
    pass


def get_active_path(path):
    """Get a path that can be used to get a file size, read/write a file, etc."""
    if platform.system() != 'Windows':
        return path

    path = path.lstrip(WINDOWS_PATH_PREFIX)
    return f'{WINDOWS_PATH_PREFIX}{path}'.replace(PATH_SEP, os.path.sep)


def validate_metadata(metadata):
    """
    Make sure metadata is in the proper form for API upload.
    
    An exeption will be thrown if the metadata is invalid.
    """
    if metadata is None:
        return

    try:
        metadata = list(dict(item) for item in metadata)
    except Exception:
        raise InvalidMetadataFormatException(
            "metadata must be list-like of dict-like")

    EXPECTED_KEYS = {'keyName', 'value'}
    EXPECTED_VALUE_KEYS = {'type', 'link'}
    ALLOWED_TYPES = {'string', 'link'}

    for item in metadata:
        item_keys = set(item.keys())

        if len(EXPECTED_KEYS - item_keys) > 0:
            raise InvalidMetadataFormatException(
                f"metadata items must have keys: {', '.join(EXPECTED_KEYS)}")

        try:
            item['value'] = dict(item['value'])
        except Exception:
            raise InvalidMetadataFormatException(
                "the value key in a metadata item must have a dict-like value")

        value_keys = set(item['value'].keys())

        if len(EXPECTED_VALUE_KEYS - value_keys) > 0:
            raise InvalidMetadataFormatException(
                "the value key in a metadata item must itself have keys "
                f"{', '.join(EXPECTED_VALUE_KEYS)}"
            )

        if item['value']['type'] not in ALLOWED_TYPES:
            raise InvalidMetadataFormatException(
                "an item['value']['type'] must be one of "
                f"{', '.join(ALLOWED_TYPES)}"
            )
