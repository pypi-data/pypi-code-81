import tkinter as tk

import attr


@attr.s(kw_only=True)
class GirderEntry:
    parent_frame = attr.ib(validator=attr.validators.instance_of(tk.Frame))

    # view
    _folder_id_box = attr.ib(init=False, validator=attr.validators.instance_of(tk.Entry))
    _item_name_box = attr.ib(init=False, validator=attr.validators.instance_of(tk.Entry))
    _item_description_box = attr.ib(init=False, validator=attr.validators.instance_of(tk.Text))

    # data
    _folder_id_var = attr.ib(init=False, validator=attr.validators.instance_of(tk.StringVar))
    _item_name_var = attr.ib(init=False, validator=attr.validators.instance_of(tk.StringVar))

    def __attrs_post_init__(self):
        tk.Label(self.parent_frame, text="Girder Folder ID").pack()
        self._folder_id_var = tk.StringVar()
        self._folder_id_box = tk.Entry(
                self.parent_frame,
                textvariable=self._folder_id_var,
                )
        self._folder_id_box.pack()

        item_label = tk.Label(self.parent_frame, text="Item Name")
        item_label.pack()
        self._item_name_var = tk.StringVar()
        self._item_name_box = tk.Entry(
                self.parent_frame,
                textvariable=self._item_name_var
                )
        self._item_name_box.pack()

        tk.Label(self.parent_frame, text="Brief Description of Asset").pack()
        self._item_description_box = tk.Text(
                self.parent_frame,
                height=15,
                width=30,
                relief=tk.RIDGE,
                borderwidth=2
                )
        self._item_description_box.pack()

    @property
    def folder_id(self):
        return self._folder_id_var.get().strip()

    @property
    def item_name(self):
        return self._item_name_var.get().strip()

    @property
    def item_description(self):
        return self._item_description_box.get('1.0', tk.END).strip()

    def set_folder_id(self, folder_id: str):
        self._folder_id_box.configure(state=tk.NORMAL)
        self._folder_id_var.set(folder_id)
        self._folder_id_box.configure(state=tk.DISABLED)

    def set_item_name(self, item_name: str):
        self._item_name_var.set(item_name)

    def set_item_description(self, item_description: str):
        self._item_description_box.delete('1.0', tk.END)
        self._item_description_box.insert(tk.END, item_description)

    def enable_item_name_box(self):
        self._item_name_box.configure(state=tk.NORMAL, bg='white')

    def enable_item_description_box(self):
        self._item_description_box.configure(state=tk.NORMAL, bg='white')

    def disable_item_name_box(self):
        self._item_name_box.configure(state=tk.DISABLED, bg='light grey')

    def disable_item_description_box(self):
        self._item_description_box.configure(state=tk.DISABLED, bg='light grey')

    def clear(self):
        """Clear all data fields."""
        self.set_folder_id('')
        self.set_item_name('')
        self.set_item_description('')
