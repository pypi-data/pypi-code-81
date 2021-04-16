import json
import os
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from typing import Optional

import attr

from nlidatamanagement.utils.girder_connector import GirderConnector
from nlidatamanagement.utils.girder_instance import GirderInstance
from nlidatamanagement.utils.zotero_connector import ZoteroConnector
from nlidatamanagement.utils.zotero_instance import ZoteroInstance

ZOTERO_INSTANCE_PATH = Path('./zotero.json')
GIRDER_INSTANCE_PATH = Path('./girder.json')


@attr.s(kw_only=True)
class GirderInstanceTreeView:
    """Girder instance Treeview."""
    parent_frame = attr.ib(validator=attr.validators.instance_of(tk.Toplevel))
    girder_connector = attr.ib(validator=attr.validators.instance_of(GirderConnector))
    girder_instance_path = attr.ib(default=GIRDER_INSTANCE_PATH, validator=attr.validators.instance_of(Path))

    # view
    _girder_instance_tv = attr.ib(init=False, validator=attr.validators.instance_of(ttk.Treeview))

    # data
    _girder_instance_map = attr.ib(init=False, factory=dict)

    def __attrs_post_init__(self):
        self._girder_instance_tv = ttk.Treeview(
                self.parent_frame,
                selectmode='browse',
                columns=('Host', 'API')
                )
        self._girder_instance_tv.grid(row=1, columnspan=2, padx=5, pady=5)
        self._girder_instance_tv.column('#0', width=100, minwidth=100, stretch=True, anchor=tk.CENTER)
        self._girder_instance_tv.column('Host', width=300, minwidth=300, stretch=True)
        self._girder_instance_tv.column('API', width=300, minwidth=300, stretch=True)
        self._girder_instance_tv.heading('#0', text='Name')
        self._girder_instance_tv.heading('Host', text='Host')
        self._girder_instance_tv.heading('API', text='API Key')

        if os.path.exists(self.girder_instance_path):
            with open(self.girder_instance_path, 'r') as f:
                instances = json.load(f)
                for instance in instances:
                    girder_instance = GirderInstance(
                            name=instance['name'],
                            host=instance['host'],
                            api_key=instance['api_key']
                            )
                    iid = self.add(girder_instance)

        def on_right_click(evt):
            w = evt.widget
            item_index = w.identify_row(evt.y)
            if item_index:
                w.selection_set(item_index)
                selected_item_name = self._girder_instance_map[item_index].name

                confirm_box = tk.messagebox.askquestion('Delete',
                                                        f'Do you want to delete Instance {selected_item_name}?')

                if confirm_box == 'yes':
                    self.remove(item_index)

        self._girder_instance_tv.bind('<Button-2>', on_right_click)
        attr.validate(self)

    @property
    def girder_instance_tv(self):
        return self._girder_instance_tv

    def get_selection(self) -> Optional[str]:
        """Get selected girder instance iid."""
        selections = self._girder_instance_tv.selection()
        if not selections:
            tk.messagebox.showerror('Error', f'Please select a Girder Instance')
            return None
        return selections[0]

    def add(self, girder_instance: GirderInstance, dump: bool = False) -> Optional[str]:
        """Add a new girder instance and return its iid.
        
        Dump the data to local file if dump == True.
        """
        if girder_instance in self._girder_instance_map.values():
            tk.messagebox.showerror('Error', f'Girder host {girder_instance.host} exists')
            return
        iid = self._girder_instance_tv.insert(
                '',
                'end',
                text=girder_instance.name,
                values=(girder_instance.host, girder_instance.api_key)
                )
        self._girder_instance_map[iid] = girder_instance
        if dump:
            self._dump()

        return iid

    def remove(self, iid: str):
        """Remove the girder instance at iid."""
        instance = self._girder_instance_map[iid]
        self._girder_instance_tv.delete(iid)
        self._girder_instance_map.pop(iid)
        self._dump()

    def connect(self, iid: str):
        """Connect to the girder instance at iid."""
        girder_instance = self._girder_instance_map[iid]
        self.girder_connector.connect(girder_instance)

    def _dump(self):
        with open(self.girder_instance_path, 'w') as f:
            json.dump(
                    obj=list(self._girder_instance_map.values()),
                    fp=f,
                    default=lambda x: x.to_json(),
                    indent=2
                    )


@attr.s(kw_only=True)
class ZoteroInstanceTreeView:
    """Zotero instance Treeview."""
    parent_frame = attr.ib(validator=attr.validators.instance_of(tk.Toplevel))
    zotero_connector = attr.ib(validator=attr.validators.instance_of(ZoteroConnector))
    zotero_instance_path = attr.ib(default=ZOTERO_INSTANCE_PATH, validator=attr.validators.instance_of(Path))

    # view
    _zotero_instance_tv = attr.ib(init=False, validator=attr.validators.instance_of(ttk.Treeview))
    # data
    _zotero_instance_map = attr.ib(init=False, factory=dict)

    def __attrs_post_init__(self):
        self._zotero_instance_tv = ttk.Treeview(
                self.parent_frame,
                selectmode='browse',
                columns=('Id', 'Type', 'API')
                )
        self._zotero_instance_tv.column('#0', width=100, minwidth=100, stretch=True, anchor=tk.CENTER)
        self._zotero_instance_tv.column('Id', width=150, minwidth=100, stretch=True, anchor=tk.CENTER)
        self._zotero_instance_tv.column('Type', width=150, minwidth=100, stretch=True, anchor=tk.CENTER)
        self._zotero_instance_tv.column('API', width=300, minwidth=300, stretch=True)
        self._zotero_instance_tv.heading('#0', text='Name')
        self._zotero_instance_tv.heading('Id', text='Id')
        self._zotero_instance_tv.heading('Type', text='Type')
        self._zotero_instance_tv.heading('API', text='API Key')

        if os.path.exists(self.zotero_instance_path):
            with open(self.zotero_instance_path, 'r') as f:
                instances = json.load(f)
                for instance in instances:
                    zotero_instance = ZoteroInstance(
                            name=instance['name'],
                            api_key=instance['api_key'],
                            library_id=instance['library_id'],
                            library_type=instance['library_type']
                            )
                    iid = self.add(zotero_instance)

        def on_right_click(evt):
            w = evt.widget
            item_index = w.identify_row(evt.y)
            if item_index:
                w.selection_set(item_index)
                selected_item_name = self._zotero_instance_map[item_index].name

                confirm_box = tk.messagebox.askquestion('Delete',
                                                        f'Do you want to delete Instance {selected_item_name}?')

                if confirm_box == 'yes':
                    self.remove(item_index)

        self._zotero_instance_tv.bind('<Button-2>', on_right_click)
        attr.validate(self)

    @property
    def zotero_instance_tv(self):
        return self._zotero_instance_tv

    def get_selection(self) -> Optional[str]:
        """Get selected zotero instance iid."""
        selections = self.zotero_instance_tv.selection()
        if not selections:
            tk.messagebox.showerror('Error', f'Please select a Zotero Instance')
            return None
        return selections[0]

    def add(self, zotero_instance: ZoteroInstance, dump: bool = False) -> Optional[str]:
        """Add a new zotero instance and return its iid.
        
        Dump the data to local file if dump == True.
        """
        if zotero_instance in self._zotero_instance_map.values():
            tk.messagebox.showerror('Error', f'Zotero libary {zotero_instance.libary_id} exists')
            return
        iid = self.zotero_instance_tv.insert(
                '',
                'end',
                text=zotero_instance.name,
                values=(zotero_instance.library_id, zotero_instance.library_type, zotero_instance.api_key)
                )
        self._zotero_instance_map[iid] = zotero_instance
        if dump:
            self._dump()

        return iid

    def remove(self, iid: str):
        """Remove the zotero instance at iid."""
        instance = self._zotero_instance_map[iid]
        self.zotero_instance_tv.delete(iid)
        self._zotero_instance_map.pop(iid)
        self._dump()

    def connect(self, iid: str):
        """Connect to the zotero instance at iid."""
        zotero_instance = self._zotero_instance_map[iid]
        self.zotero_connector.connect(zotero_instance)

    def _dump(self):
        with open(self.zotero_instance_path, 'w') as f:
            json.dump(
                    obj=list(self._zotero_instance_map.values()),
                    fp=f,
                    default=lambda x: x.to_json(),
                    indent=2
                    )
