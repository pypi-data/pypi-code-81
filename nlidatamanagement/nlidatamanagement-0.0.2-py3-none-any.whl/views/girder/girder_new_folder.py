import tkinter as tk

import attr
import girder_client


@attr.s(kw_only=True)
class GirderControlAccessView:
    access_read_control_frame = attr.ib(validator=attr.validators.instance_of(tk.Frame))
    access_write_control_frame = attr.ib(validator=attr.validators.instance_of(tk.Frame))
    girder_client = attr.ib(validator=attr.validators.instance_of(girder_client.GirderClient))

    # views
    _group_read_lb = attr.ib(init=False, validator=attr.validators.instance_of(tk.Listbox))
    _group_write_lb = attr.ib(init=False, validator=attr.validators.instance_of(tk.Listbox))

    # data
    _groups = attr.ib(init=False, validator=attr.validators.instance_of(list))
    _group_lb_var = attr.ib(init=False, validator=attr.validators.instance_of(tk.StringVar))

    def __attrs_post_init__(self):
        # load groups info
        self._groups = self.girder_client.get(path='/group')
        group_names = []
        for group in self._groups:
            group_names.append(group['name'])
        self._group_lb_var = tk.StringVar()
        self._group_lb_var.set(group_names)

        # view init
        tk.Label(self.access_read_control_frame, text="Read Access").pack()
        self._group_read_lb = tk.Listbox(
                self.access_read_control_frame,
                listvariable=self._group_lb_var,
                selectmode=tk.MULTIPLE,
                exportselection=False,
                relief=tk.RIDGE,
                borderwidth=2
                )
        self._group_read_lb.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        tk.Label(self.access_write_control_frame, text="Write Access").pack()
        self._group_write_lb = tk.Listbox(
                self.access_write_control_frame,
                listvariable=self._group_lb_var,
                selectmode=tk.MULTIPLE,
                exportselection=False,
                relief=tk.RIDGE,
                borderwidth=2
                )
        self._group_write_lb.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self._group_read_lb.bind("<<ListboxSelect>>", self._on_select)
        self._group_write_lb.bind("<<ListboxSelect>>", self._on_select)
        attr.validate(self)

    def set_public(self):
        """Disable read access for public folder creation."""
        self._group_read_lb.selection_clear(0, tk.END)
        self._group_read_lb.configure(state=tk.DISABLED)

    def set_private(self):
        """Enable read access for private folder creation."""
        self._group_read_lb.configure(state=tk.NORMAL)

    def get_control_group(self) -> dict:
        """Get a json object for current selected control group."""
        control_groups = {}

        me = self.girder_client.get(path='/user/me')
        owner = {'id': me['_id'], 'level': 2}
        control_groups['users'] = [owner]

        control_groups['groups'] = []
        self._get_control_group_from_listbox(self._group_read_lb, control_groups, level=0)
        self._get_control_group_from_listbox(self._group_write_lb, control_groups, level=1)
        return control_groups

    def _get_control_group_from_listbox(self, listbox, control_groups, level):
        for index in listbox.curselection():
            group = self._groups[index]
            control_group = {'id': group['_id'], 'name': group['name'], 'level': level}
            control_groups['groups'].append(control_group)

    def _on_select(self, evt):
        widget = evt.widget
        indices = widget.curselection()
        for index in indices:
            if widget == self._group_read_lb:
                self._group_write_lb.selection_clear(index)
            else:
                self._group_read_lb.selection_clear(index)


@attr.s(kw_only=True)
class GirderNewFolder:
    """Window to create new folder."""
    parent_win = attr.ib(validator=attr.validators.instance_of(tk.Frame))
    girder_client = attr.ib(validator=attr.validators.instance_of(girder_client.GirderClient))
    parent_item = attr.ib(validator=attr.validators.instance_of(dict))
    # callback after upload
    folder_on_upload = attr.ib(validator=attr.validators.is_callable())

    # data
    _is_public = attr.ib(init=False)

    # view
    _new_folder_win = attr.ib(init=False, validator=attr.validators.instance_of(tk.Toplevel))
    _folder_name_box = attr.ib(init=False, validator=attr.validators.instance_of(tk.Entry))
    _folder_description_box = attr.ib(init=False, validator=attr.validators.instance_of(tk.Text))
    _control_access_view = attr.ib(init=False, validator=attr.validators.instance_of(GirderControlAccessView))

    def __attrs_post_init__(self):
        parent_item_name = self.parent_item['name']
        parent_item_type = self.parent_item['_modelType']
        if parent_item_type != 'collection' and parent_item_type != 'folder':
            tk.messagebox.showerror('Error', f"Please select a collection or folder instead of an {parent_item_type}")
            return

        new_folder_win = tk.Toplevel(self.parent_win)
        new_folder_win.title('Create new folder')
        new_folder_win.grid_columnconfigure([0, 1], weight=1)
        self._new_folder_win = new_folder_win

        tk.Label(
                new_folder_win,
                text=f"Creating a new folder under {parent_item_type} {parent_item_name}",
                wraplength=200,
                justify="center",
                borderwidth=2,
                relief=tk.GROOVE
                ).grid(row=0, column=0, columnspan=4, pady=10, ipadx=10, ipady=5)

        tk.Label(new_folder_win, text="Folder Name").grid(row=1, column=0, columnspan=2, pady=3)
        self._folder_name_box = tk.Entry(
                new_folder_win
                )
        self._folder_name_box.grid(row=2, column=0, columnspan=2)

        self._is_public = tk.BooleanVar()
        public_rbtn = tk.Radiobutton(
                new_folder_win,
                text="Public",
                variable=self._is_public,
                value=True,
                command=lambda: self._control_access_view.set_public()
                )
        public_rbtn.grid(row=3, column=0, pady=3)

        private_rbtn = tk.Radiobutton(
                new_folder_win,
                text="Private",
                variable=self._is_public,
                value=False,
                command=lambda: self._control_access_view.set_private()
                )
        private_rbtn.grid(row=3, column=1, pady=3)

        tk.Label(new_folder_win, text="Folder Description").grid(row=4, column=0, columnspan=2, pady=3)
        self._folder_description_box = tk.Text(
                new_folder_win,
                height=15,
                width=30,
                relief=tk.RIDGE,
                borderwidth=2
                )
        self._folder_description_box.grid(row=5, column=0, columnspan=2, padx=5)

        access_read_control_frame = tk.Frame(
                new_folder_win,
                relief=tk.RAISED,
                borderwidth=1
                )
        access_read_control_frame.grid(row=1, column=2, rowspan=5, padx=3, pady=3, sticky='nwes')

        access_write_control_frame = tk.Frame(
                new_folder_win,
                relief=tk.RAISED,
                borderwidth=1
                )
        access_write_control_frame.grid(row=1, column=3, rowspan=5, padx=3, pady=3, sticky='nwes')
        self._control_access_view = GirderControlAccessView(
                access_read_control_frame=access_read_control_frame,
                access_write_control_frame=access_write_control_frame,
                girder_client=self.girder_client
                )

        # generate button
        button_frame = tk.Frame(
                new_folder_win
                )
        button_frame.grid(row=6, column=0, columnspan=4, padx=3, pady=3, sticky='nwes')
        button_frame.grid_columnconfigure([0, 1], weight=1)
        back_btn = tk.Button(
                button_frame,
                text="Back",
                command=new_folder_win.destroy
                )
        back_btn.grid(row=0, column=0, sticky='nwes')

        upload_btn = tk.Button(
                button_frame,
                text="Confirm",
                command=lambda: self._upload_to_girder()
                )
        upload_btn.grid(row=0, column=1, sticky='nwes')

        public_rbtn.select()
        public_rbtn.invoke()
        attr.validate(self)

    def _upload_to_girder(self):
        try:
            folder = self.girder_client.createFolder(
                    parentId=self.parent_item['_id'],
                    parentType=self.parent_item['_modelType'],
                    name=self._folder_name_box.get(),
                    description=self._folder_description_box.get('1.0', tk.END),
                    public=self._is_public.get()
                    )
        except girder_client.HttpError as e:
            tk.messagebox.showerror('Error', str(e))
            return

        access = self._control_access_view.get_control_group()

        self.girder_client.setFolderAccess(
                folderId=folder['_id'],
                access=access,
                public=self._is_public.get()
                )
        self.folder_on_upload()
        self._new_folder_win.destroy()
