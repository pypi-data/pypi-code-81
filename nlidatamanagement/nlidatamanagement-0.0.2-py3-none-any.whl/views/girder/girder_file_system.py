import json
import os
import tkinter as tk
from tkinter import ttk
import types

import attr
import girder_client
from PIL import ImageTk

from nlidatamanagement.imgs import DOWNLOAD_IMG, FOLDER_IMG, REFRESH_IMG
import nlidatamanagement.utils.parser as parser
from nlidatamanagement.views.common.item_info import ItemInfo
from nlidatamanagement.views.girder.girder_download import GirderDownload
from nlidatamanagement.views.girder.girder_new_folder import GirderNewFolder

COLLECTION = "collection"
FOLDER = "folder"
ITEM = "item"


@attr.s(kw_only=True)
class GirderFileSystem:
    """Girder File System View.

    Required Attributes:
        parent_frame: tk.Frame
        girder_client: girder_client.GriderClient
        on_item_select: a callback method that triggered while select an item
    """

    parent_frame = attr.ib(validator=attr.validators.instance_of(tk.Frame))
    girder_client = attr.ib(
            validator=attr.validators.instance_of(girder_client.GirderClient)
            )
    on_item_select = attr.ib(validator=attr.validators.instance_of(types.MethodType))

    # data
    _file_sys_tv_index_item_map = attr.ib(init=False, factory=dict)
    _item_tv_index_file_map = attr.ib(init=False, factory=dict)
    _explored = attr.ib(init=False, factory=set)
    _selected_item = attr.ib(default=None, init=False)

    # imgs
    _download_img = attr.ib(
            init=False, validator=attr.validators.instance_of(ImageTk.PhotoImage)
            )
    _refresh_img = attr.ib(
            init=False, validator=attr.validators.instance_of(ImageTk.PhotoImage)
            )
    _folder_img = attr.ib(
            init=False, validator=attr.validators.instance_of(ImageTk.PhotoImage)
            )

    # view
    _file_sys_tv = attr.ib(
            init=False, validator=attr.validators.instance_of(ttk.Treeview)
            )
    _item_tv = attr.ib(init=False, validator=attr.validators.instance_of(ttk.Treeview))

    def __attrs_post_init__(self):
        self.parent_frame.rowconfigure(1, weight=1)
        self.parent_frame.columnconfigure([0, 1, 2], weight=1)

        self._download_img = ImageTk.PhotoImage(DOWNLOAD_IMG)
        self._refresh_img = ImageTk.PhotoImage(REFRESH_IMG)
        self._folder_img = ImageTk.PhotoImage(FOLDER_IMG)

        indicator_label = tk.Label(self.parent_frame, text="Girder File System")
        indicator_label.grid(row=0, column=0, columnspan=3, sticky="NSEW")

        self._file_sys_tv = ttk.Treeview(
                self.parent_frame, selectmode="browse", columns=("Type", "Size")
                )
        self._file_sys_tv.grid(
                row=1, column=0, columnspan=3, padx=3, pady=3, sticky="NSEW"
                )

        self._file_sys_tv.column("#0", width=300, minwidth=300)
        self._file_sys_tv.column("Type", width=100, minwidth=100, anchor=tk.CENTER)
        self._file_sys_tv.column("Size", width=100, minwidth=100, anchor=tk.CENTER)
        self._file_sys_tv.heading("#0", text="Name")
        self._file_sys_tv.heading("Type", text="Type")
        self._file_sys_tv.heading("Size", text="Size")

        def on_select(evt):
            """Show item info on select."""
            w = evt.widget
            selections = w.selection()
            if not selections:
                return
            item_index = selections[0]
            self._selected_item = self._file_sys_tv_index_item_map[item_index]
            _id = self._selected_item["_id"]
            model_type = self._selected_item["_modelType"]

            self.on_item_select(self._selected_item)
            self._item_tv.delete(*self._item_tv.get_children())
            if model_type == ITEM:
                # show files in item
                file_list = self.girder_client.listFile(itemId=_id)
                for file in file_list:
                    size = parser.parse_size_from_byte(file["size"])
                    name = (
                        (file["name"][:40] + "...")
                        if len(file["name"]) > 40
                        else file["name"]
                    )
                    created_time = parser.parse_isoformat_datetime(file["created"])
                    iid = self._item_tv.insert(
                            "", "end", text=name, values=(created_time, size)
                            )
                    self._item_tv_index_file_map[iid] = file

        def on_open(evt):
            """Retrieve the next level item info on expand."""
            w = evt.widget
            item_index = w.selection()[0]
            if item_index not in self._explored:
                self._explored.add(item_index)
                children = w.get_children(item_index)
                for child in children:
                    self._retrieve_information(child)

        def on_right_click(evt, index_item_map: dict):
            w = evt.widget
            iid = w.identify_row(evt.y)
            if iid:
                w.selection_set(iid)
                item = index_item_map[iid]
                model_type = item["_modelType"]
                _id = item["_id"]
                try:
                    access = self.girder_client.get(path=f"/{model_type}/{_id}/access")
                except Exception:
                    access = "Admin access denied"

                item["access"] = json.dumps(access, indent=2)
                ItemInfo(
                        parent_frame=self.parent_frame,
                        item=item,
                        item_type=item["_modelType"],
                        )

        self._file_sys_tv.bind("<<TreeviewSelect>>", on_select)
        self._file_sys_tv.bind("<<TreeviewOpen>>", on_open)
        self._file_sys_tv.bind(
                "<Button-2>",
                lambda evt: on_right_click(evt, self._file_sys_tv_index_item_map),
                )

        item_label = tk.Label(self.parent_frame, text="Files")
        item_label.grid(row=2, column=0, columnspan=3, sticky="NSEW")
        self._item_tv = ttk.Treeview(
                self.parent_frame, selectmode="browse", columns=("Date Modified", "Size")
                )
        self._item_tv.grid(row=3, column=0, columnspan=3, padx=3, pady=3, sticky="NSEW")

        self._item_tv.column("#0", width=250, minwidth=250)
        self._item_tv.column("Date Modified", width=150, minwidth=150, anchor=tk.CENTER)
        self._item_tv.column("Size", width=100, minwidth=100, anchor=tk.CENTER)
        self._item_tv.heading("#0", text="Name")
        self._item_tv.heading("Date Modified", text="Date Modified")
        self._item_tv.heading("Size", text="Size")

        self._item_tv.bind(
                "<Button-2>", lambda evt: on_right_click(evt, self._item_tv_index_file_map)
                )

        download_btn = tk.Button(
                self.parent_frame,
                image=self._download_img,
                command=lambda: self._download(),
                )
        download_btn.grid(row=4, column=0, padx=3, pady=3, sticky="NSEW")

        refresh_btn = tk.Button(
                self.parent_frame, image=self._refresh_img, command=lambda: self.refresh()
                )
        refresh_btn.grid(row=4, column=1, padx=3, pady=3, sticky="NSEW")

        add_folder_btn = tk.Button(
                self.parent_frame,
                image=self._folder_img,
                command=lambda: self._add_folder(),
                )
        add_folder_btn.grid(row=4, column=2, padx=3, pady=3, sticky="NSEW")

        self._retrieve_information()
        attr.validate(self)

    @property
    def selected_item(self):
        return self._selected_item

    def clear(self):
        """Clear current selected item."""
        self._selected_item = None
        self._file_sys_tv.selection_remove(*self._file_sys_tv.selection())
        self._item_tv.delete(*self._item_tv.get_children())

    def _retrieve_information(self, parent_item_index: str = None):
        """Retrieve items infromation and insert into the treeview.

        Parameters:
            parent_item_index: treeview index of its parent item (default: None, e.g. root level)
        """
        # root directory. retrieve collections info
        if not parent_item_index:
            collections = self.girder_client.listCollection()
            for collection in collections:
                collection_index = self._insert_item_to_treeview(collection)

                # get folder info
                folders = self.girder_client.listFolder(
                        parentId=collection["_id"],
                        parentFolderType=collection["_modelType"],
                        )
                for folder in folders:
                    self._insert_item_to_treeview(folder, collection_index)

        # retrieve folder info
        else:
            item = self._file_sys_tv_index_item_map[parent_item_index]
            _id = item["_id"]
            if item["_modelType"] == FOLDER:
                # Girder folder contains subfolder or items
                folders = self.girder_client.listFolder(
                        parentId=_id, parentFolderType=FOLDER
                        )
                for folder in folders:
                    self._insert_item_to_treeview(folder, parent_item_index)

                files = self.girder_client.listItem(folderId=_id)
                for file in files:
                    self._insert_item_to_treeview(file, parent_item_index)

    def _insert_item_to_treeview(self, item: dict, parent: str = "") -> str:
        """Insert a Girder item into the treeview.

        Parameters:
            item: A Girder item represented by a dict
            parent: The index of the parent item (default: '', e.g. root level)

        Return:
            str: the new index of the inserted item
        """
        model_type = item["_modelType"]
        name = (item["name"][:40] + "...") if len(item["name"]) > 40 else item["name"]

        # The size of folder return by Girder API doesn't include its subfolders
        # Don't show the folder size as it is not accurate
        if model_type != FOLDER:
            size = parser.parse_size_from_byte(item["size"])
            item_index = self._file_sys_tv.insert(
                    parent, "end", text=name, values=(model_type, size)
                    )
        else:
            size = "..."
            item_index = self._file_sys_tv.insert(
                    parent, "end", text=name, values=(model_type, size)
                    )

        self._file_sys_tv_index_item_map[item_index] = item
        return item_index

    def _download(self):
        """Create a new window and download selected item."""
        if self._selected_item:
            download_folder = tk.filedialog.askdirectory()
            if download_folder == "":
                return

            name = self._selected_item["name"]

            # if item exists, return
            for entry in os.scandir(download_folder):
                if entry.name == name:
                    tk.messagebox.showerror("Error", f"Item {name} exists.")
                    return

            download_frame = GirderDownload(
                    window=tk.Toplevel(self.parent_frame),
                    girder_client=self.girder_client,
                    download_dir=download_folder,
                    download_item=self._selected_item,
                    )
            download_frame.run()

        else:
            tk.messagebox.showerror("Error", "Please select an item.")

    def _add_folder(self):
        """Add a new folder to a collection or folder."""
        if not self._selected_item:
            tk.messagebox.showerror("Error", f"Please select a collection or folder")
            return

        GirderNewFolder(
                parent_win=self.parent_frame,
                girder_client=self.girder_client,
                parent_item=self._selected_item,
                folder_on_upload=self.refresh,
                )

    def refresh(self):
        """Refresh the file system and clear selection."""
        self._file_sys_tv.delete(*self._file_sys_tv.get_children())
        self._item_tv.delete(*self._item_tv.get_children())
        self._selected_item = None
        self.on_item_select(None)
        self._retrieve_information()
