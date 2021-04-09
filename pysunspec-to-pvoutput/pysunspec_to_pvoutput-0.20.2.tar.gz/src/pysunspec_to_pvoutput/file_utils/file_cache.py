import glob
import logging
import os
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)


def sibling(cache_dir):
    return Path(cache_dir.parent, "completed")


class FileProcessCache:

    def __init__(self, cache_dir: Path, processed_dir: Path = None, extension: str = "json"):
        self.entries = []
        self.extension = extension
        self.store_dir = processed_dir if processed_dir is not None else sibling(cache_dir)
        self.cache_dir = cache_dir

    def size(self) -> int:
        return len(self.entries)

    def load(self) -> List[Path]:
        """Loads all of the paths in the cache directory to a list and returns it
        When a file has been successfully processed, call move_to_processed
        The entry will be removed from that list
        Only call load again if you want to refresh the list with any new files that have been added to the cache dir"""
        pattern = Path.joinpath(self.cache_dir, "*." + self.extension)
        self.entries = [Path(f) for f in glob.glob(str(pattern))]
        self.sort_entries()
        logger.info("Loaded cache, file count {}".format(len(self.entries)))
        return self.entries

    def sort_entries(self):
        self.entries.sort()

    def move_to_processed(self, entry: Path) -> Path:
        """Moves the given path to the completed dir
        path is removed from the list of files in the cache
        Only call load again if you want to refresh the list with any new files that have been added to the cache dir
        """
        self.create_dir(self.store_dir)
        self.entries.remove(entry)
        dest = Path(self.store_dir, entry.name)
        os.rename(str(entry), dest)
        logger.info(f"Moving file to {dest}")
        return dest

    @staticmethod
    def create_dir(path):
        os.makedirs(path, exist_ok=True)


def move_to_completed(readings: List[Path], cache):
    for reading in readings:
        cache.move_to_processed(reading)
