import sys
import tkinter as tk

import attr
from PIL import ImageTk

from nlidatamanagement.imgs import ADD_IMG, CONNECT_IMG, DELETE_IMG
from nlidatamanagement.utils.girder_connector import GirderConnector
from nlidatamanagement.utils.girder_instance import GirderInstance
from nlidatamanagement.views.common.setting import GirderInstanceTreeView


@attr.s(kw_only=True)
class GirderSetting:
    """Window for girder client config. 

    Required Attributes:
        parent_frame: tk.Frame
        girder_connector: current connected girder connector
        on_connect: callback for reconnection. require new connector for parameter.
    """
    parent_win = attr.ib(validator=attr.validators.instance_of((tk.Toplevel, tk.Tk)))
    girder_connector = attr.ib(validator=attr.validators.instance_of(GirderConnector))
    on_connect = attr.ib(validator=attr.validators.is_callable())

    # img
    _connect_img = attr.ib(init=False, validator=attr.validators.instance_of(ImageTk.PhotoImage))
    _add_img = attr.ib(init=False, validator=attr.validators.instance_of(ImageTk.PhotoImage))
    _delete_img = attr.ib(init=False, validator=attr.validators.instance_of(ImageTk.PhotoImage))

    # view
    _setting_win = attr.ib(init=False, validator=attr.validators.instance_of(tk.Toplevel))
    _girder_instances = attr.ib(init=False, validator=attr.validators.instance_of(GirderInstanceTreeView))

    # data
    _name_var = attr.ib(init=False, validator=attr.validators.instance_of(tk.StringVar))
    _host_var = attr.ib(init=False, validator=attr.validators.instance_of(tk.StringVar))
    _api_key_var = attr.ib(init=False, validator=attr.validators.instance_of(tk.StringVar))

    def __attrs_post_init__(self):
        self._connect_img = ImageTk.PhotoImage(CONNECT_IMG)
        self._add_img = ImageTk.PhotoImage(ADD_IMG)
        self._delete_img = ImageTk.PhotoImage(DELETE_IMG)

        self._name_var = tk.StringVar()
        self._host_var = tk.StringVar()
        self._api_key_var = tk.StringVar()

        self._setting_win = tk.Toplevel(self.parent_win)
        self._setting_win.title('Setting')

        tk.Label(
                self._setting_win,
                text="Select Girder Instance"
                ).grid(row=0, columnspan=2, sticky='nsew')

        self._girder_instances = GirderInstanceTreeView(
                parent_frame=self._setting_win,
                girder_connector=self.girder_connector
                )
        self._girder_instances.girder_instance_tv.grid(row=1, columnspan=2, padx=5, pady=5)

        add_instance_frame = tk.Frame(
                self._setting_win,
                borderwidth=2,
                relief=tk.GROOVE
                )
        add_instance_frame.grid(row=2, column=0, padx=10, pady=10, ipadx=5, ipady=5, sticky='nsew')
        add_instance_frame.grid_columnconfigure(2, weight=1)

        tk.Label(
                add_instance_frame,
                text="Add new Girder instance"
                ).grid(row=0, columnspan=5, sticky='nsew')

        tk.Label(
                add_instance_frame,
                text="Name: "
                ).grid(row=1, column=0, sticky='nsew')

        tk.Entry(
                add_instance_frame,
                textvariable=self._name_var
                ).grid(row=1, column=1, columnspan=3, sticky='nsew')

        tk.Label(
                add_instance_frame,
                text="Host: "
                ).grid(row=2, column=0, sticky='nsew')

        tk.Label(
                add_instance_frame,
                text="https://"
                ).grid(row=2, column=1, sticky='nsew')

        tk.Entry(
                add_instance_frame,
                textvariable=self._host_var
                ).grid(row=2, column=2, sticky='nsew')

        tk.Label(
                add_instance_frame,
                text="/api/v1"
                ).grid(row=2, column=3, sticky='nsew')

        tk.Label(
                add_instance_frame,
                text="API Key: "
                ).grid(row=3, column=0, sticky='nsew')

        tk.Entry(
                add_instance_frame,
                textvariable=self._api_key_var
                ).grid(row=3, column=1, columnspan=3, sticky='nsew')

        # add instance button
        tk.Button(
                add_instance_frame,
                image=self._add_img,
                command=lambda: self._add_new_instance()
                ).grid(row=1, column=4, rowspan=3, sticky='nsew', padx=5)

        # connect button
        tk.Button(
                self._setting_win,
                image=self._connect_img,
                command=lambda: self._connect()
                ).grid(row=2, column=1, sticky='nsew', padx=(0, 10), pady=10)

        attr.validate(self)
        self._setting_win.mainloop()

    def _add_new_instance(self):
        name = self._name_var.get()
        host = f'https://{self._host_var.get()}/api/v1'
        api_key = self._api_key_var.get()

        if not name:
            tk.messagebox.showerror('Error', f'Please input a name')
        elif not host:
            tk.messagebox.showerror('Error', f'Please input a host name')
        elif not api_key:
            tk.messagebox.showerror('Error', f'Please input an API key')
        else:
            girder_instance = GirderInstance(
                    name=name,
                    host=host,
                    api_key=api_key
                    )
            self._girder_instances.add(girder_instance, dump=True)

    def _connect(self):
        iid = self._girder_instances.get_selection()
        if iid:
            try:
                self._girder_instances.connect(iid)
            except:
                e = sys.exc_info()
                tk.messagebox.showerror('Error', e)
                return
            self._setting_win.destroy()
            self.on_connect(self.parent_win, self.girder_connector)

    def _remove_instance(self):
        iid = self._girder_instances.get_selection()
        if iid:
            self._girder_instances.remove(iid)
