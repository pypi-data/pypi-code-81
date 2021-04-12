import os
import sys
import time
import logging
from pathlib import Path
from typing import List, Set, Dict

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class BaseWatcherEventHandler(FileSystemEventHandler):
    def __init__(self, runner):
        super().__init__()
        self.runner = runner
        self.logger = logging.root

    def on_moved(self, event):
        super().on_moved(event)

        what = 'directory' if event.is_directory else 'file'
        self.logger.info("Moved %s: from %s to %s", what, event.src_path, event.dest_path)

    def on_created(self, event):
        super().on_created(event)

        what = 'directory' if event.is_directory else 'file'
        self.logger.info("Created %s: %s", what, event.src_path)

    def on_deleted(self, event):
        super().on_deleted(event)

        what = 'directory' if event.is_directory else 'file'
        self.logger.info("Deleted %s: %s", what, event.src_path)

    def raran(self, unprocessed_filepath: str):
        filepath = Path(unprocessed_filepath)
        if filepath.suffix == '.md' and filepath.parts[-1][0:2] == '__':
            self.runner.run_with_filepath(source_filepath=unprocessed_filepath, run_test=False)

    def process_src_path(self, src_path: str) -> str:
        if src_path[-1] == '~':
            src_path = src_path[0:-1]
        return src_path

    def confirm_modified(self, event, source_filepath: str):
        dependencies_filepaths = self.runner.files_dependencies.dependencies_to_parents.get(source_filepath, None)
        if dependencies_filepaths is not None:
            for dependency_filepath in dependencies_filepaths:
                self.raran(dependency_filepath)

        self.raran(source_filepath)

        what = 'directory' if event.is_directory else 'file'
        self.logger.info("Modified %s: %s", what, event.src_path)


class FolderWatcherEventHandler(BaseWatcherEventHandler):
    def on_modified(self, event):
        super().on_modified(event)
        source_filepath = self.process_src_path(src_path=event.src_path)
        self.confirm_modified(event=event, source_filepath=source_filepath)

class DirectoryFilesWatcherEventHandler(BaseWatcherEventHandler):
    def __init__(self, runner, watched_files: Set[str]):
        super().__init__(runner=runner)
        self.watched_files = watched_files

    def on_modified(self, event):
        super().on_modified(event)
        source_filepath = self.process_src_path(src_path=event.src_path)
        if source_filepath in self.watched_files:
            self.confirm_modified(event=event, source_filepath=source_filepath)


class Watcher:
    def __init__(self, runner):
        self.runner = runner
        self.observer = Observer()
        self.directory_files_watchers: Dict[str, DirectoryFilesWatcherEventHandler] = dict()

    def start(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        path = sys.argv[1] if len(sys.argv) > 1 else 'F:/Inoft/StructNoSQL/docs/docs'
        self.observer.schedule(event_handler=FolderWatcherEventHandler(runner=self.runner), path=path, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()

    def add_file_watch(self, filepath: str):
        dirpath = os.path.dirname(filepath)
        existing_directory_files_watcher = self.directory_files_watchers.get(dirpath, None)
        if existing_directory_files_watcher is not None:
            existing_directory_files_watcher.watched_files.add(filepath)
        else:
            event_handler = DirectoryFilesWatcherEventHandler(runner=self.runner, watched_files={filepath})
            self.observer.schedule(event_handler=event_handler, path=dirpath, recursive=False)


if __name__ == "__main__":
    pass
