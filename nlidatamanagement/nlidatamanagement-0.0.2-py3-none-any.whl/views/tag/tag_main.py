import tkinter as tk

import attr

from nlidatamanagement.tags import TagList
from nlidatamanagement.views.common.item_info import ItemInfo
from nlidatamanagement.views.tag.tag_management import TagManagement


@attr.s(kw_only=True)
class TagFrame(object):
    parent_frame = attr.ib(validator=attr.validators.instance_of(tk.Frame))
    tag_list = attr.ib(validator=attr.validators.instance_of(TagList))
    user_name = attr.ib(validator=attr.validators.instance_of(str))

    # view
    _tag_lb = attr.ib(init=False, validator=attr.validators.instance_of(tk.Listbox))
    _tag_management = attr.ib(init=False, validator=attr.validators.instance_of(TagManagement))

    # data
    _tag_lb_var = attr.ib(init=False, validator=attr.validators.instance_of(tk.StringVar))

    def __attrs_post_init__(self):
        tag_label = tk.Label(self.parent_frame, text="Select Tags")
        tag_label.pack(pady=3)
        self._tag_lb_var = tk.StringVar()
        self._tag_lb_var.set(self.tag_list.tags_name)
        self._tag_lb = tk.Listbox(
                self.parent_frame,
                listvariable=self._tag_lb_var,
                selectmode=tk.MULTIPLE,
                relief=tk.RIDGE,
                borderwidth=2,
                width=35
                )
        self._tag_lb.pack(expand=True, padx=3, fill=tk.BOTH)
        self._tag_management = TagManagement(
                parent_frame=self.parent_frame,
                tag_list=self.tag_list,
                user_name=self.user_name,
                tag_list_var=self._tag_lb_var
                )

        def on_right_click(evt):
            w = evt.widget
            index = w.nearest(evt.y)
            if index:
                # w.selection_set(iid)
                item = vars(self.tag_list[index])
                ItemInfo(
                        parent_frame=self.parent_frame,
                        item=item,
                        item_type='Tag'
                        )

        self._tag_lb.bind('<Button-2>', on_right_click)

        tags_management_btn = tk.Button(
                self.parent_frame,
                text='Tags Management',
                command=lambda: self._tag_management.generate_tag_management_win()
                )
        tags_management_btn.pack(pady=3)
        attr.validate(self)

    def enable(self):
        """Enable tag list box selection."""
        self._tag_lb.configure(state=tk.NORMAL)

    def disable(self):
        """Disable tag list box selection."""
        self._tag_lb.configure(state=tk.DISABLED)

    def clear_selection(self):
        """Clear selection in tag list box."""
        self._tag_lb.select_clear(0, tk.END)

    def set_selection(self, index):
        """Highlight the entry at index."""
        self._tag_lb.selection_set(index)

    def get_selection_as_list(self):
        """Return a list of name of selected tags."""
        selected_list = []
        selection = self._tag_lb.curselection()
        for i in selection:
            entry = self._tag_lb.get(i)
            selected_list.append(entry)
        return selected_list

    def get_selection_as_str(self):
        """Return a str of name of selected tags."""
        tag_names = self.get_selection_as_list()
        tags = ""
        for tag in tag_names:
            tags += "[//]: # (" + tag + ")\n"
        return tags
