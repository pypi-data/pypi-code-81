import json
import tkinter as tk
from tkinter import ttk

import attr
from pyzotero import zotero

from nlidatamanagement.views.common.item_info import ItemInfo


@attr.s(kw_only=True)
class ZoteroFileSystem:
    parent_frame = attr.ib(validator=attr.validators.instance_of(tk.Frame))
    zotero_client = attr.ib(validator=attr.validators.instance_of(zotero.Zotero))
    on_item_select = attr.ib(validator=attr.validators.is_callable())

    # data
    _file_sys_tv_index_item_map = attr.ib(init=False, factory=dict)
    _explored = attr.ib(init=False, factory=set)

    # view
    _file_sys_tv = attr.ib(
            init=False, validator=attr.validators.instance_of(ttk.Treeview)
            )

    def __attrs_post_init__(self):
        # self.current_mode = COLLECTION
        self.parent_frame.rowconfigure(1, weight=1)
        self.parent_frame.columnconfigure([0, 1], weight=1)

        indicator_label = tk.Label(self.parent_frame, text="Collections")
        indicator_label.grid(row=0, column=0, columnspan=2, sticky="NSEW")

        self._file_sys_tv = ttk.Treeview(
                self.parent_frame, selectmode="browse", columns="Type"
                )
        self._file_sys_tv.grid(
                row=1, column=0, columnspan=2, padx=3, pady=3, sticky="NSEW"
                )

        self._file_sys_tv.column("#0", width=300, minwidth=300)
        self._file_sys_tv.column("Type", width=100, minwidth=100, anchor=tk.CENTER)
        self._file_sys_tv.heading("#0", text="Name")
        self._file_sys_tv.heading("Type", text="Type")

        def on_select(evt):
            """Show item info on select."""
            w = evt.widget
            selections = w.selection()
            if not selections:
                return
            item_index = selections[0]
            selected_item = self._file_sys_tv_index_item_map[item_index]
            if "itemType" in selected_item["data"]:
                self.on_item_select(selected_item)

        def on_open(evt):
            """Retrieve the next level item info on expand."""
            w = evt.widget
            item_index = w.selection()[0]
            if item_index not in self._explored:
                self._explored.add(item_index)
                children = w.get_children(item_index)
                for child in children:
                    self._retrieve_information(child)

        def on_right_click(evt):
            w = evt.widget
            item_index = w.identify_row(evt.y)
            if item_index:
                w.selection_set(item_index)
                selected_item = self._file_sys_tv_index_item_map[item_index]
                if "itemType" in selected_item["data"]:
                    item_type = "Item"
                    selected_item["data"]["creators"] = json.dumps(
                            selected_item["data"]["creators"], indent=2
                            )
                else:
                    item_type = "Collection"
                ItemInfo(
                        parent_frame=self.parent_frame,
                        item=selected_item["data"],
                        item_type=item_type,
                        )

        self._file_sys_tv.bind("<<TreeviewOpen>>", on_open)
        self._file_sys_tv.bind("<<TreeviewSelect>>", on_select)
        self._file_sys_tv.bind("<Button-2>", on_right_click)

        attr.validate(self)
        self._retrieve_information()

    def refresh(self):
        """Refresh the collection."""
        self._file_sys_tv.delete(*self._file_sys_tv.get_children())
        self._retrieve_information()

    def _retrieve_information(self, parent_item_index: str = None):
        """Retrieve items infromation and insert into the treeview.

        Parameters:
            parent_item_index: treeview index of its parent item (default: None, e.g. root level)
        """
        # root directory. retrieve collections info
        if not parent_item_index:
            collections = self.zotero_client.collections_top()
            # collections = self.girder_client.listCollection()
            for collection in collections:
                # insert root collection only
                collection_index = self._insert_item_to_treeview(
                        collection, isCollection=True
                        )
                collection_id = collection["data"]["key"]

                # get sub collection info
                subcollections = self.zotero_client.collections_sub(
                        collection_id, isCollection=True
                        )
                for subcollection in subcollections:
                    self._insert_item_to_treeview(
                            subcollection, isCollection=True, parent=collection_index
                            )

                # get item info
                items = self.zotero_client.collection_items_top(
                        collection_id, itemType="book || journalArticle"
                        )
                for item in items:
                    self._insert_item_to_treeview(
                            item, isCollection=False, parent=collection_index
                            )

        # retrieve child info
        else:
            item = self._file_sys_tv_index_item_map[parent_item_index]
            data = item["data"]

            if "title" not in data:
                # is sub collection
                collection_id = data["key"]
                # get sub collection info
                subcollections = self.zotero_client.collections_sub(
                        collection_id, isCollection=True
                        )
                for subcollection in subcollections:
                    self._insert_item_to_treeview(
                            subcollection, isCollection=True, parent=parent_item_index
                            )

                # get item info
                items = self.zotero_client.collection_items_top(
                        collection_id, itemType="book || journalArticle"
                        )
                for item in items:
                    self._insert_item_to_treeview(
                            item, isCollection=False, parent=parent_item_index
                            )

    def _insert_item_to_treeview(
            self, item: dict, isCollection: bool, parent: str = ""
            ) -> str:
        """Insert a Zotero item into the treeview.

        Parameters:
            item: A Zotero item represented by a dict
            parent: The index of the parent item (default: '', e.g. root level)
            isCollection: if the inserted item is collection

        Return:
            str: the new index of the inserted item
        """
        data = item["data"]
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(item)
        if isCollection:
            name = ((data["name"][:40] + "...")
                    if len(data["name"]) > 40
                    else data["name"]
                    )
            item_type = "collection"
        else:
            name = ((data["title"][:40] + "...")
                    if len(data["title"]) > 40
                    else data["title"]
                    )
            item_type = data["itemType"]
        item_index = self._file_sys_tv.insert(
                parent, "end", text=name, values=item_type
                )

        self._file_sys_tv_index_item_map[item_index] = item
        return item_index
