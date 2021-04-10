from concurrent import futures
import os
from pathlib import Path
import threading
import tkinter as tk
from tkinter import ttk

import attr
import girder_client

COLLECTION = "collection"
FOLDER = "folder"
ITEM = "item"

thread_pool_executor = futures.ThreadPoolExecutor(max_workers=1)


@attr.s(kw_only=True)
class GirderDownload(object):
    window = attr.ib(validator=attr.validators.instance_of(tk.Toplevel))
    girder_client = attr.ib(
            validator=attr.validators.instance_of(girder_client.GirderClient)
            )
    download_dir = attr.ib(validator=attr.validators.instance_of(str))
    download_item = attr.ib(validator=attr.validators.instance_of(dict))

    def __attrs_post_init__(self):
        self.download_thread = threading.Thread(target=self._download)
        self.window.title("Downloading")

    def run(self):
        item_type = self.download_item["_modelType"]
        item_name = self.download_item["name"]
        if item_type == COLLECTION or item_type == FOLDER:
            new_dir = Path(self.download_dir)
            new_dir = new_dir / item_name
            new_dir.mkdir()
            self.download_dir = new_dir

        item_size, init_size = self._progress_bar_init()
        expected_size = item_size + init_size

        thread_pool_executor.submit(self._download)
        self._set_progress_bar_value(init_size, expected_size)

    def _set_progress_bar_value(self, init_size, expected_size):
        current_size = self._get_directory_size(self.download_dir)
        current_progress = current_size - init_size
        self.progress_bar["value"] = current_progress

        if current_size >= expected_size or self.window.state() == "withdraw":
            self.window.destroy()
        else:
            self.window.after(
                    1000, self._set_progress_bar_value, init_size, expected_size
                    )

    def _progress_bar_init(self):
        item_size = self.download_item["size"]
        item_name = self.download_item["name"]
        item_label = tk.Label(
                self.window, text=f"Downloading {item_name}", font=("Helvetica Neue", 20)
                )
        item_label.pack()
        progress_bar_style = ttk.Style()
        progress_bar_style.theme_use("default")
        progress_bar_style.configure(
                "TProgressbar", thickness=20, background="blue", foreground="blue"
                )
        self.progress_bar = ttk.Progressbar(
                self.window,
                orient="horizontal",
                length=200,
                mode="determinate",
                style="TProgressbar",
                )
        self.progress_bar.pack(padx=5, pady=5)
        self.progress_bar["value"] = 0
        self.progress_bar["maximum"] = item_size
        return item_size, self._get_directory_size(self.download_dir)

    def _download(self):
        item_id = self.download_item["_id"]
        item_type = self.download_item["_modelType"]
        if item_type == COLLECTION or item_type == FOLDER:
            self.girder_client.downloadResource(
                    resourceId=item_id, dest=self.download_dir, resourceType=item_type
                    )
        elif item_type == ITEM:
            self.girder_client.downloadItem(item_id, self.download_dir)
        self.window.withdraw()

    def _get_directory_size(self, directory):
        """Returns the `directory` size in bytes."""
        total = 0
        try:
            for entry in os.scandir(directory):
                if entry.is_file():
                    # if it's a file, use stat() function
                    total += entry.stat().st_size
                elif entry.is_dir():
                    # if it's a directory, recursively call this function
                    total += self._get_directory_size(entry.path)
        except NotADirectoryError:
            # if `directory` isn't a directory, get the file size then
            return os.path.getsize(directory)
        except PermissionError:
            # if for whatever reason we can't open the folder, return 0
            return 0
        return total
