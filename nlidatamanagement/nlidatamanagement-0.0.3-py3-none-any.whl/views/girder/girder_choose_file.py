import tkinter as tk
import tkinter.filedialog as tkfile

import attr
from PIL import ImageTk

from nlidatamanagement.imgs import ADD_IMG, REMOVE_IMG


@attr.s(kw_only=True)
class GirderChooseFile:
    parent_frame = attr.ib(validator=attr.validators.instance_of(tk.Frame))

    # data
    _file_paths = attr.ib(init=False, factory=list)
    _file_values = attr.ib(
            init=False, validator=attr.validators.instance_of(tk.StringVar)
            )

    # imgs
    _add_img = attr.ib(
            init=False, validator=attr.validators.instance_of(ImageTk.PhotoImage)
            )
    _remove_img = attr.ib(
            init=False, validator=attr.validators.instance_of(ImageTk.PhotoImage)
            )

    # view
    _files_lb = attr.ib(init=False, validator=attr.validators.instance_of(tk.Listbox))
    _add_btn = attr.ib(init=False, validator=attr.validators.instance_of(tk.Button))
    _remove_btn = attr.ib(init=False, validator=attr.validators.instance_of(tk.Button))

    def __attrs_post_init__(self):
        self._file_values = tk.StringVar()
        self._add_img = ImageTk.PhotoImage(ADD_IMG)
        self._remove_img = ImageTk.PhotoImage(REMOVE_IMG)

        files_label = tk.Label(self.parent_frame, text="Choose Files to Upload")
        files_label.grid(row=0, column=0, columnspan=2, sticky="N" + "S" + "E" + "W")
        self._files_lb = tk.Listbox(
                self.parent_frame,
                listvariable=self._file_values,
                selectmode=tk.MULTIPLE,
                width=20,
                relief=tk.RIDGE,
                borderwidth=2,
                )
        self._files_lb.grid(
                row=1, column=0, rowspan=2, padx=5, pady=5, sticky="N" + "S" + "E" + "W"
                )
        self._add_btn = tk.Button(
                self.parent_frame, image=self._add_img, command=lambda: choose_file()
                )
        self._add_btn.grid(row=1, column=1, padx=5, sticky="N" + "S" + "E" + "W")
        self._remove_btn = tk.Button(
                self.parent_frame, image=self._remove_img, command=lambda: remove_file()
                )
        self._remove_btn.grid(row=2, column=1, padx=5, sticky="N" + "S" + "E" + "W")

        def choose_file():
            file_paths = list(tkfile.askopenfilenames())
            for file_path in file_paths:
                # skip if file has been selected
                if file_path not in self._file_paths:
                    self._file_paths.append(file_path)
            file_names = [filepath.split("/")[-1] for filepath in self._file_paths]
            self._file_values.set(file_names)

        def remove_file():
            indices = self._files_lb.curselection()
            for idx in sorted(indices, reverse=True):
                self._file_paths.pop(idx)
            file_names = [filepath.split("/")[-1] for filepath in self._file_paths]
            self._file_values.set(file_names)

        attr.validate(self)

    @property
    def file_paths(self):
        return self._file_paths

    @property
    def file_names(self):
        return [filepath.split("/")[-1] for filepath in self._file_paths]

    def clear(self):
        self._file_paths = []
        self._file_values.set([])

    def disable(self):
        self._add_btn.configure(state=tk.DISABLED)
        self._remove_btn.configure(state=tk.DISABLED)
        self._files_lb.configure(state=tk.DISABLED, bg="light grey")

    def enable(self):
        self._add_btn.configure(state=tk.NORMAL)
        self._remove_btn.configure(state=tk.NORMAL)
        self._files_lb.configure(state=tk.NORMAL, bg="white")
