from enum import Enum
import tkinter as tk

import attr


class Mode(Enum):
    TO_NEW_ITEM = 0
    TO_EXIST_ITEM = 1
    TO_EDIT_ITEM = 2


@attr.s(kw_only=True)
class GirderMode:
    """Frame to switch mode."""
    firstname = attr.ib(validator=attr.validators.instance_of(str))
    lastname = attr.ib(validator=attr.validators.instance_of(str))
    parent_frame = attr.ib(validator=attr.validators.instance_of(tk.Frame))

    # event trigger function on mode change
    new_item_mode_function = attr.ib(validator=attr.validators.is_callable())
    edit_item_mode_function = attr.ib(validator=attr.validators.is_callable())

    # data
    _current_mode_var = attr.ib(init=False, validator=attr.validators.instance_of(tk.IntVar))

    def __attrs_post_init__(self):
        welcome_msg = 'Welcome ' + self.firstname + ' ' + self.lastname
        tk.Label(self.parent_frame, text=welcome_msg).pack()

        self._current_mode_var = tk.IntVar()
        new_item_rbtn = tk.Radiobutton(
                self.parent_frame,
                text="New Item",
                variable=self._current_mode_var,
                value=Mode.TO_NEW_ITEM.value,
                command=self.new_item_mode_function
                )
        new_item_rbtn.pack(fill=tk.X, padx=40)
        new_item_rbtn.select()

        edit_item_rbtn = tk.Radiobutton(
                self.parent_frame,
                text="Edit Item",
                variable=self._current_mode_var,
                value=Mode.TO_EDIT_ITEM.value,
                command=self.edit_item_mode_function
                )
        edit_item_rbtn.pack(fill=tk.X, padx=40)
        attr.validate(self)

    @property
    def mode(self):
        return Mode(self._current_mode_var.get())
