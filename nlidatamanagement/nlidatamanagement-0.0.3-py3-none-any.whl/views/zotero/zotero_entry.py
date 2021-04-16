import tkinter as tk

import attr


@attr.s(kw_only=True)
class ZoteroEntry:
    parent_frame = attr.ib(validator=attr.validators.instance_of(tk.Frame))
    user_name = attr.ib(validator=attr.validators.instance_of(str))

    # data
    _item_id_var = attr.ib(
            init=False, validator=attr.validators.instance_of(tk.StringVar)
            )
    _item_type_var = attr.ib(
            init=False, validator=attr.validators.instance_of(tk.StringVar)
            )
    _item_title_var = attr.ib(
            init=False, validator=attr.validators.instance_of(tk.StringVar)
            )
    _item_tag_var = attr.ib(
            init=False, validator=attr.validators.instance_of(tk.StringVar)
            )
    _current_item = attr.ib(init=False, factory=dict)
    _current_tags = attr.ib(init=False, factory=list)

    # view
    _item_tag_box = attr.ib(
            init=False, validator=attr.validators.instance_of(tk.Listbox)
            )

    def __attrs_post_init__(self):
        welcome_msg = f"Welcome {self.user_name}"
        tk.Label(self.parent_frame, text=welcome_msg).pack()

        self._item_id_var = tk.StringVar()
        self._item_type_var = tk.StringVar()
        self._item_title_var = tk.StringVar()
        self._item_tag_var = tk.StringVar()

        item_id_label = tk.Label(self.parent_frame, text="Item ID")
        item_id_label.pack()
        item_id_box = tk.Entry(self.parent_frame, textvariable=self._item_id_var)
        item_id_box.pack()

        item_type_label = tk.Label(self.parent_frame, text="Item Type")
        item_type_label.pack()
        item_type_box = tk.Entry(self.parent_frame, textvariable=self._item_type_var)
        item_type_box.pack()

        item_title_label = tk.Label(self.parent_frame, text="Item Title")
        item_title_label.pack()
        item_title_box = tk.Entry(self.parent_frame, textvariable=self._item_title_var)
        item_title_box.pack()

        item_tag_label = tk.Label(self.parent_frame, text="Item Tags")
        item_tag_label.pack()
        self._item_tag_box = tk.Listbox(
                self.parent_frame,
                listvariable=self._item_tag_var,
                selectmode=tk.MULTIPLE,
                width=25,
                )
        self._item_tag_box.pack()

    @property
    def item(self):
        return self._current_item

    @property
    def tags(self):
        return self._current_tags

    def set_item_info(self, item: dict):
        """Set the current selected item."""
        item_info = item["data"]
        item_id = item_info["key"]
        if "title" in item_info:
            item_title = item_info["title"]
        else:
            item_title = "N/A"

        item_type = item_info["itemType"]
        self._item_id_var.set(item_id)
        self._item_type_var.set(item_type)
        self._item_title_var.set(item_title)
        self._current_tags = []
        for tag in item_info["tags"]:
            self._current_tags.append(tag["tag"])
        self._item_tag_var.set(self._current_tags)
        self._current_item = item

    def add_item_tags(self, tags: list):
        if self._current_item:
            for tag in tags:
                if tag not in self._current_tags:
                    self._current_tags.append(tag)
            self._sync_tags()
        else:
            tk.messagebox.showerror("Error", "Please select an item.")

    def remove_selected_tags(self):
        if self._current_item:
            indices = self._item_tag_box.curselection()
            for index in indices:
                tag = self._item_tag_box.get(index)
                if tag in self._current_tags:
                    self._current_tags.remove(tag)
            self._item_tag_box.selection_clear(0, tk.END)
            self._sync_tags()
        else:
            tk.messagebox.showerror("Error", "Please select an item.")

    def _sync_tags(self):
        """Sync the displayed tag list with the item."""
        self._item_tag_var.set(self._current_tags)
        new_tags = []
        for tag in self._current_tags:
            tag_dict = {"tag": tag}
            new_tags.append(tag_dict)
        self._current_item["data"]["tags"] = new_tags

    def refresh(self):
        """Clear the current item."""
        self._item_id_var.set("")
        self._item_type_var.set("")
        self._item_title_var.set("")
        self._item_tag_var.set("")
        self._current_item.clear()
        self._current_tags.clear()
