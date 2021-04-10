from datetime import datetime

LOCAL_TIMEZONE = datetime.now().astimezone().tzinfo


def parse_isoformat_datetime(datetime_str: str) -> str:
    """Parse a isoformat datetime string to a readable datetime str."""
    local_time = datetime.fromisoformat(datetime_str).astimezone(LOCAL_TIMEZONE)
    return local_time.strftime("%m-%d-%Y %H:%M")


def parse_size_from_byte(byte_num: int) -> str:
    """Return a readable size from byte number."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB']:
        if abs(byte_num) < 1024.0:
            return "%3.1f %s" % (byte_num, unit)
        byte_num /= 1024.0
    return "%.1f %s" % (byte_num, 'YB')
