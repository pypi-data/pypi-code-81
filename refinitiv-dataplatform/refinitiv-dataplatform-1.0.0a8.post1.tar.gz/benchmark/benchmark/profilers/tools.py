from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

SKIP = {'mocks', '__pycache__'}


def get_current_time(use_utc=False):
    if use_utc:
        return datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    else:
        return datetime.now().strftime("%Y%m%d%H%M%S")


def multithreading(func, args, workers):
    with ThreadPoolExecutor(max_workers=workers) as executor:
        res = executor.map(func, args)
    return list(res)


def get_benchmarks(root):
    for filename in root.iterdir():
        name = filename.stem
        if name in SKIP:
            continue
        yield filename
