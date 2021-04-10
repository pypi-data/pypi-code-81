import sys
import tkinter as tk

import attr
from PIL import ImageTk

from nlidatamanagement.imgs import ADD_IMG, CONNECT_IMG, DELETE_IMG
from nlidatamanagement.utils.girder_connector import GirderConnector
from nlidatamanagement.utils.girder_instance import GirderInstance
from nlidatamanagement.utils.zotero_connector import ZoteroConnector
from nlidatamanagement.utils.zotero_instance import ZoteroInstance
from nlidatamanagement.views.common.setting import (
    GirderInstanceTreeView,
    ZoteroInstanceTreeView,
    )


@attr.s(kw_only=True)
class ZoteroSetting:
    """Window for girder client config.

    Required Attributes:
        parent_frame: tk.Frame
        girder_connector: current connected girder connector
        zotero_connector: current connected zotero connector
        on_connect: callback for connection. require new connectors for parameter.
    """

    parent_win = attr.ib(validator=attr.validators.instance_of((tk.Toplevel, tk.Tk)))
    girder_connector = attr.ib(validator=attr.validators.instance_of(GirderConnector))
    zotero_connector = attr.ib(validator=attr.validators.instance_of(ZoteroConnector))
    on_connect = attr.ib(validator=attr.validators.is_callable())

    # img
    _connect_img = attr.ib(
            init=False, validator=attr.validators.instance_of(ImageTk.PhotoImage)
            )
    _add_img = attr.ib(
            init=False, validator=attr.validators.instance_of(ImageTk.PhotoImage)
            )
    _delete_img = attr.ib(
            init=False, validator=attr.validators.instance_of(ImageTk.PhotoImage)
            )

    # view
    _setting_win = attr.ib(
            init=False, validator=attr.validators.instance_of(tk.Toplevel)
            )
    _girder_instances = attr.ib(
            init=False, validator=attr.validators.instance_of(GirderInstanceTreeView)
            )
    _zotero_instances = attr.ib(
            init=False, validator=attr.validators.instance_of(ZoteroInstanceTreeView)
            )

    # data
    _girder_name_var = attr.ib(
            init=False, validator=attr.validators.instance_of(tk.StringVar)
            )
    _girder_host_var = attr.ib(
            init=False, validator=attr.validators.instance_of(tk.StringVar)
            )
    _girder_api_key_var = attr.ib(
            init=False, validator=attr.validators.instance_of(tk.StringVar)
            )

    _zotero_name_var = attr.ib(
            init=False, validator=attr.validators.instance_of(tk.StringVar)
            )
    _zotero_library_id_var = attr.ib(
            init=False, validator=attr.validators.instance_of(tk.StringVar)
            )
    _zotero_library_type_var = attr.ib(
            init=False, validator=attr.validators.instance_of(tk.StringVar)
            )
    _zotero_api_key_var = attr.ib(
            init=False, validator=attr.validators.instance_of(tk.StringVar)
            )

    def __attrs_post_init__(self):
        self._connect_img = ImageTk.PhotoImage(CONNECT_IMG)
        self._add_img = ImageTk.PhotoImage(ADD_IMG)
        self._delete_img = ImageTk.PhotoImage(DELETE_IMG)

        self._girder_name_var = tk.StringVar()
        self._girder_host_var = tk.StringVar()
        self._girder_api_key_var = tk.StringVar()

        self._zotero_name_var = tk.StringVar()
        self._zotero_api_key_var = tk.StringVar()
        self._zotero_library_id_var = tk.StringVar()
        self._zotero_library_type_var = tk.StringVar()

        self._setting_win = tk.Toplevel(self.parent_win)
        self._setting_win.title("Setting")
        self._setting_win.grid_columnconfigure(0, weight=70)
        self._setting_win.grid_columnconfigure(1, weight=15)
        self._setting_win.grid_columnconfigure(2, weight=15)

        tk.Label(self._setting_win, text="Select Girder Instance").grid(
                row=0, columnspan=2, sticky="nsew"
                )

        self._girder_instances = GirderInstanceTreeView(
                parent_frame=self._setting_win, girder_connector=self.girder_connector
                )
        self._girder_instances.girder_instance_tv.grid(
                row=1, columnspan=2, padx=5, pady=5
                )

        tk.Label(self._setting_win, text="Select Zotero Instance").grid(
                row=2, columnspan=2, sticky="nsew"
                )

        self._zotero_instances = ZoteroInstanceTreeView(
                parent_frame=self._setting_win, zotero_connector=self.zotero_connector
                )
        self._zotero_instances.zotero_instance_tv.grid(
                row=3, columnspan=2, padx=5, pady=5
                )

        add_girder_instance_frame = tk.Frame(
                self._setting_win, borderwidth=2, relief=tk.GROOVE
                )
        add_girder_instance_frame.grid(
                row=4, column=0, padx=10, pady=10, ipadx=5, ipady=5, sticky="nsew"
                )
        add_girder_instance_frame.grid_columnconfigure(2, weight=1)

        tk.Label(add_girder_instance_frame, text="Add new Girder instance").grid(
                row=0, columnspan=5, sticky="nsew"
                )

        tk.Label(add_girder_instance_frame, text="Name: ").grid(
                row=1, column=0, sticky="nsew"
                )

        tk.Entry(add_girder_instance_frame, textvariable=self._girder_name_var).grid(
                row=1, column=1, columnspan=3, sticky="nsew"
                )

        tk.Label(add_girder_instance_frame, text="Host: ").grid(
                row=2, column=0, sticky="nsew"
                )

        tk.Label(add_girder_instance_frame, text="https://").grid(
                row=2, column=1, sticky="nsew"
                )

        tk.Entry(add_girder_instance_frame, textvariable=self._girder_host_var).grid(
                row=2, column=2, sticky="nsew"
                )

        tk.Label(add_girder_instance_frame, text="/api/v1").grid(
                row=2, column=3, sticky="nsew"
                )

        tk.Label(add_girder_instance_frame, text="API Key: ").grid(
                row=3, column=0, sticky="nsew"
                )

        tk.Entry(add_girder_instance_frame, textvariable=self._girder_api_key_var).grid(
                row=3, column=1, columnspan=3, sticky="nsew"
                )

        # add Girder instance button
        tk.Button(
                add_girder_instance_frame,
                image=self._add_img,
                command=lambda: self._add_new_girder_instance(),
                ).grid(row=1, column=4, rowspan=3, sticky="nsew", padx=5)

        add_zotero_instance_frame = tk.Frame(
                self._setting_win, borderwidth=2, relief=tk.GROOVE
                )
        add_zotero_instance_frame.grid(
                row=5, column=0, padx=10, pady=10, ipadx=5, ipady=5, sticky="nsew"
                )
        add_zotero_instance_frame.grid_columnconfigure(1, weight=1)

        tk.Label(add_zotero_instance_frame, text="Add new zotero instance").grid(
                row=0, columnspan=3, sticky="nsew"
                )

        tk.Label(add_zotero_instance_frame, text="Name: ").grid(
                row=1, column=0, sticky="nsew"
                )

        tk.Entry(add_zotero_instance_frame, textvariable=self._zotero_name_var).grid(
                row=1, column=1, sticky="nsew"
                )

        tk.Label(add_zotero_instance_frame, text="Library ID: ").grid(
                row=2, column=0, sticky="nsew"
                )

        tk.Entry(
                add_zotero_instance_frame, textvariable=self._zotero_library_id_var
                ).grid(row=2, column=1, sticky="nsew")

        tk.Label(add_zotero_instance_frame, text="Library Type: ").grid(
                row=3, column=0, sticky="nsew"
                )

        tk.Entry(
                add_zotero_instance_frame, textvariable=self._zotero_library_type_var
                ).grid(row=3, column=1, sticky="nsew")

        tk.Label(add_zotero_instance_frame, text="API Key: ").grid(
                row=4, column=0, sticky="nsew"
                )

        tk.Entry(add_zotero_instance_frame, textvariable=self._zotero_api_key_var).grid(
                row=4, column=1, sticky="nsew"
                )

        # add Zotero instance button
        tk.Button(
                add_zotero_instance_frame,
                image=self._add_img,
                command=lambda: self._add_new_zotero_instance(),
                ).grid(row=1, column=2, rowspan=4, sticky="nsew", padx=5)

        # connect button
        tk.Button(
                self._setting_win, image=self._connect_img, command=lambda: self._connect()
                ).grid(row=4, column=1, rowspan=2, sticky="nsew", pady=10, padx=(0, 10))

        attr.validate(self)
        self._setting_win.mainloop()

    def _add_new_girder_instance(self):
        name = self._girder_name_var.get()
        host = f"https://{self._girder_host_var.get()}/api/v1"
        api_key = self._girder_api_key_var.get()

        if not name:
            tk.messagebox.showerror("Error", f"Please input a name")
        elif not host:
            tk.messagebox.showerror("Error", f"Please input a host name")
        elif not api_key:
            tk.messagebox.showerror("Error", f"Please input an API key")
        else:
            girder_instance = GirderInstance(name=name, host=host, api_key=api_key)
            self._girder_instances.add(girder_instance, dump=True)

    def _add_new_zotero_instance(self):
        name = self._zotero_name_var.get()
        library_id = self._zotero_library_id_var.get()
        library_type = self._zotero_library_type_var.get()
        api_key = self._zotero_api_key_var.get()

        if not name:
            tk.messagebox.showerror("Error", f"Please input a name")
        elif not library_id:
            tk.messagebox.showerror("Error", f"Please input a library id")
        elif not library_type:
            tk.messagebox.showerror("Error", f"Please input an library type")
        elif not api_key:
            tk.messagebox.showerror("Error", f"Please input an api key")
        else:
            zotero_instance = ZoteroInstance(
                    name=name,
                    library_id=library_id,
                    library_type=library_type,
                    api_key=api_key,
                    )
            self._zotero_instances.add(zotero_instance, dump=True)

    def _connect(self):
        girder_iid = self._girder_instances.get_selection()
        zotero_iid = self._zotero_instances.get_selection()
        if girder_iid and zotero_iid:
            try:
                self._girder_instances.connect(girder_iid)
                self._zotero_instances.connect(zotero_iid)
            except:
                e = sys.exc_info()
                tk.messagebox.showerror("Error", e)
                return
            self._setting_win.destroy()
            self.on_connect(
                    self.parent_win, self.girder_connector, self.zotero_connector
                    )
