from tkinter import scrolledtext, ttk
import tkinter as tk

import attr

import nlidatamanagement.utils.parser as parser


@attr.s(kw_only=True)
class ItemInfo:
    """Window to show item metadata information. 

    Pop up by right click.
    Required Attributes:
        item: dict. Represent the item metadata
        item_type: str. Tag, Collection, Folder, etc.
        parent_frame: tk.Frame
    """
    item = attr.ib(validator=attr.validators.instance_of(dict))
    item_type = attr.ib(validator=attr.validators.instance_of(str))
    parent_frame = attr.ib(validator=attr.validators.instance_of(tk.Frame))

    _index_value_map = attr.ib(init=False, factory=dict)

    def __attrs_post_init__(self):
        file_info_win = tk.Toplevel(self.parent_frame)
        file_info_win.title(f'{self.item_type} Information')
        file_info_tv = ttk.Treeview(
                file_info_win,
                selectmode='browse',
                columns='Value'
                )
        file_info_tv.pack(padx=3, pady=3)
        file_info_tv.column('#0', width=150, minwidth=150, stretch=True)
        file_info_tv.column('Value', width=250, minwidth=250, stretch=True)
        file_info_tv.heading('#0', text='Key')
        file_info_tv.heading('Value', text='Value')

        for key, value in self.item.items():
            if key == 'created' or key == 'updated':
                value = parser.parse_isoformat_datetime(value)
            elif key == 'size':
                value = parser.parse_size_from_byte(value)
            iid = file_info_tv.insert('', 'end', text=key, values=str(value).replace(' ', r'\ '))
            self._index_value_map[iid] = value

        def on_select(evt):
            """Show item info on select."""
            w = evt.widget
            item_index = w.selection()[0]
            val = self._index_value_map[item_index]
            if val:
                file_info_text_box.delete('1.0', tk.END)
                file_info_text_box.insert('1.0', str(val))

        file_info_tv.bind('<<TreeviewSelect>>', on_select)

        file_info_text_box = scrolledtext.ScrolledText(
                file_info_win,
                wrap=tk.WORD,
                height=10,
                width=50,
                relief=tk.RIDGE,
                borderwidth=2
                )
        file_info_text_box.pack(padx=3, pady=3)

        close_btn = tk.Button(
                file_info_win,
                text='close',
                command=lambda: file_info_win.destroy()
                )
        close_btn.pack()
