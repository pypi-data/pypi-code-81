import tkinter as tk
from tkinter import ttk

import attr
import girder_client

from nlidatamanagement.views.girder.girder_mode import Mode

TAG_KEY = 'girder_item_tags'


@attr.s(kw_only=True)
class GirderPreview:
    """Window for item information preview before upload."""
    folder_id = attr.ib(validator=attr.validators.instance_of(str))
    folder_name = attr.ib(validator=attr.validators.instance_of(str))
    item_id = attr.ib(validator=attr.validators.instance_of(str))
    item_name = attr.ib(validator=attr.validators.instance_of(str))
    item_description = attr.ib(validator=attr.validators.instance_of(str))
    chosen_tags = attr.ib(validator=attr.validators.instance_of(list))
    file_paths = attr.ib(default=[], validator=attr.validators.instance_of(list))
    file_names = attr.ib(default=[], validator=attr.validators.instance_of(list))

    mode = attr.ib(validator=attr.validators.instance_of(Mode))
    parent_win = attr.ib(validator=attr.validators.instance_of(tk.Toplevel))
    girder_client = attr.ib(validator=attr.validators.instance_of(girder_client.GirderClient))

    # callback after upload
    on_item_upload = attr.ib(validator=attr.validators.is_callable())

    def __attrs_post_init__(self):
        if len(self.chosen_tags) < 1:
            tk.messagebox.showerror('Error', 'Make sure you choose at least one tag.')
        if len(self.file_paths) < 1 and self.mode == Mode.TO_NEW_ITEM:
            tk.messagebox.showerror('Error', 'Make sure you choose at least one file.')
        elif self.folder_id == "" or self.item_description == "":
            tk.messagebox.showerror('Error', 'Make sure you select a Folder and input a description')
        else:
            preview_win = tk.Toplevel(self.parent_win)
            preview_win.title('Confirm your info')
            preview_win.grid_columnconfigure([0, 1], weight=1)
            preview_win.grid_rowconfigure([0, 1, 2, 3], weight=1)

            # set files info
            file_frame = tk.Frame(
                    master=preview_win
                    )
            file_frame.grid(row=0, column=0, padx=3, pady=3, sticky='N' + 'S' + 'W' + 'E')

            tk.Label(file_frame, text='Files').pack()
            file_lb = tk.Listbox(
                    file_frame,
                    relief=tk.RIDGE,
                    borderwidth=2,
                    width=30,
                    height=20
                    )
            file_lb.insert(tk.END, *self.file_names)
            file_lb.pack()

            # set tags info
            tag_frame = tk.Frame(
                    master=preview_win
                    )
            tag_frame.grid(row=0, column=1, padx=3, pady=3, sticky='N' + 'S' + 'E' + 'W')
            tk.Label(tag_frame, text='Tags').pack()
            tag_lb = tk.Listbox(
                    tag_frame,
                    relief=tk.RIDGE,
                    borderwidth=2,
                    width=30,
                    height=20
                    )
            tag_lb.insert(tk.END, *self.chosen_tags)
            tag_lb.pack()

            girder_entry_tv = ttk.Treeview(
                    preview_win,
                    selectmode='browse',
                    columns='Value'
                    )
            girder_entry_tv.grid(row=1, column=0, sticky='E' + 'W', columnspan=2, padx=3, pady=3)
            girder_entry_tv.column('#0', width=100, minwidth=100, stretch=True)
            girder_entry_tv.column('Value', width=300, minwidth=300, stretch=True)

            girder_entry_tv.insert('', 'end', text='Folder ID', values=str(self.folder_id).replace(' ', r'\ '))
            girder_entry_tv.insert('', 'end', text='Folder Name', values=str(self.folder_name).replace(' ', r'\ '))
            girder_entry_tv.insert('', 'end', text='Item ID', values=str(self.item_id).replace(' ', r'\ '))
            girder_entry_tv.insert('', 'end', text='Item Name', values=str(self.item_name).replace(' ', r'\ '))
            girder_entry_tv.insert('', 'end', text='Item Description',
                                   values=str(self.item_description).replace(' ', r'\ '))

            # generate button
            back_btn = tk.Button(
                    preview_win,
                    text="Back",
                    command=preview_win.destroy
                    )
            back_btn.grid(row=2, column=0)

            upload_btn = tk.Button(
                    preview_win,
                    text="Confirm",
                    command=lambda: self._upload_to_girder(preview_win)
                    )
            upload_btn.grid(row=2, column=1)

    def _upload_to_girder(self, parent):
        for filepath in self.file_paths:
            try:
                with open(filepath) as f:
                    # throwaway test to ensure readability
                    f.read(1)
            except IOError:
                tk.messagebox.showerror('Error', f"File {filepath} does not exist or has not been chosen.")
                return

        item_id = self.item_id
        try:
            if self.mode == Mode.TO_NEW_ITEM:
                # create item
                item = self.girder_client.createItem(
                        parentFolderId=self.folder_id,
                        name=self.item_name,
                        description=self.item_description
                        )
                item_id = item['_id']
            elif self.mode == Mode.TO_EDIT_ITEM:
                # edit description
                self.girder_client.put(f'/item/{item_id}', parameters={'description': self.item_description})

            metadata = {TAG_KEY: self.chosen_tags}
            self.girder_client.addMetadataToItem(item_id, metadata)
        except girder_client.HttpError as e:
            tk.messagebox.showerror('Error', str(e))
            return

        # file upload
        if len(self.file_names):
            progress_win = tk.Toplevel(parent)
            tk.Label(progress_win, text='Uploading...')
            progress = ttk.Progressbar(
                    progress_win,
                    orient=tk.HORIZONTAL,
                    length=100,
                    mode='determinate'
                    )
            progress.pack()
            step = 100 / len(self.file_names)
            for filepath, filename in zip(self.file_paths, self.file_names):
                res = self.girder_client.uploadFileToItem(
                        item_id,
                        filepath=filepath,
                        reference=None,
                        mimeType=None,
                        filename=filename
                        )
                if res is None:
                    tk.messagebox.showwarning('Warning', 'File ' + filename + ' already exist.')
                progress['value'] += step
            progress['value'] = 100
            progress_win.destroy()
        parent.destroy()
        self.on_item_upload()
