import os
from datetime import datetime

now = datetime.now()

time = {
    "year": now.year,
    "month": now.month,
    "day": now.day,
    "hour": now.hour,
    "minute": now.minute,
    "second": now.second,
}

filesystem = {
    "cwd": os.getcwd(),
}

dynamic_render_context = dict(**time, **filesystem)
