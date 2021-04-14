import shutil
from pathlib import Path


def clean_deepchain_cache():
    path = Path.home().joinpath(".cache", "deepchain-apps", "data")
    try:
        shutil.rmtree(str(path))
    except FileNotFoundError:
        pass
