#!/usr/bin/env python3
from tkinter import messagebox
import tkinter as tk

from PIL import ImageTk

from nlidatamanagement.imgs import BACK_IMG, GO_IMG, REFRESH_IMG, UPLOAD_IMG
from nlidatamanagement.tags import TagList
from nlidatamanagement.views.tag.tag_main import TagFrame
from nlidatamanagement.views.zotero.zotero_entry import ZoteroEntry
from nlidatamanagement.views.zotero.zotero_file_system import ZoteroFileSystem

COLLECTION = 0
ITEM = 1

zotero_key = "kDBP8t98w36gJ8RwLg6JRJ57"
zotero_lib = "2345225"
zotero_type = "group"


class ZoteroUploader:
    def __init__(self, window, girder_connector, zotero_connector):
        self.window = tk.Toplevel(window)
        self.window.title("Upload literature to Zotero")

        self.go_photo = ImageTk.PhotoImage(GO_IMG)
        self.back_photo = ImageTk.PhotoImage(BACK_IMG)
        self.upload_phote = ImageTk.PhotoImage(UPLOAD_IMG)
        self.refresh_phote = ImageTk.PhotoImage(REFRESH_IMG)

        tag_frame = tk.Frame(master=self.window, relief=tk.RAISED, borderwidth=1)
        tag_frame.grid(row=0, column=0, ipadx=5, ipady=5, padx=5, pady=5, sticky="NSEW")

        btn_frame = tk.Frame(master=self.window)
        btn_frame.grid(row=0, column=1, ipady=5, pady=5, sticky="NSEW")

        main_frame = tk.Frame(master=self.window, relief=tk.RAISED, borderwidth=1)
        main_frame.grid(row=0, column=2, padx=5, pady=5, sticky="NSEW")

        entry_frame = tk.Frame(master=main_frame)
        entry_frame.grid(row=0, column=0, padx=5, pady=5, sticky="NSEW")

        item_btn_frame = tk.Frame(main_frame, borderwidth=0)
        item_btn_frame.columnconfigure([0, 1], weight=1)
        item_btn_frame.grid(row=1, column=0, padx=5, sticky="NSEW")

        item_frame = tk.Frame(master=self.window, relief=tk.RAISED, borderwidth=1)
        item_frame.grid(
                row=0, column=3, ipadx=5, ipady=5, padx=5, pady=5, sticky="NSEW"
                )

        self.zotero_client = zotero_connector.client
        try:
            tag_list = TagList("./tags.csv", girder_connector.client)
        except:
            self.window.destroy()
            return

        self.tag_system = TagFrame(
                parent_frame=tag_frame,
                tag_list=tag_list,
                user_name=girder_connector.first_name + " " + girder_connector.last_name,
                )

        self.zotero_entry = ZoteroEntry(
                parent_frame=entry_frame,
                user_name=f"{girder_connector.first_name} {girder_connector.last_name}",
                )
        self.zotero_file_system = ZoteroFileSystem(
                parent_frame=item_frame,
                zotero_client=self.zotero_client,
                on_item_select=lambda item: self.zotero_entry.set_item_info(item),
                )

        add_btn = tk.Button(
                btn_frame,
                borderwidth=0,
                image=self.go_photo,
                command=lambda: self.zotero_entry.add_item_tags(
                        self.tag_system.get_selection_as_list()
                        ),
                )
        add_btn.pack(expand=True, fill=tk.BOTH)

        remove_btn = tk.Button(
                btn_frame,
                borderwidth=0,
                image=self.back_photo,
                command=lambda: self.zotero_entry.remove_selected_tags(),
                )
        remove_btn.pack(expand=True, fill=tk.BOTH)

        item_refresh_btn = tk.Button(
                item_btn_frame, image=self.refresh_phote, command=lambda: self.refresh()
                )
        item_refresh_btn.grid(row=0, column=0, sticky="NSEW")

        item_upload_btn = tk.Button(
                item_btn_frame, image=self.upload_phote, command=lambda: self.upload_item()
                )
        item_upload_btn.grid(row=0, column=1, sticky="NSEW")

    def refresh(self):
        self.zotero_entry.refresh()
        self.zotero_file_system.refresh()

    def upload_item(self):
        if self.zotero_entry.item:
            try:
                if self.zotero_client.update_item(self.zotero_entry.item):
                    messagebox.showinfo(title="Info", message="Uploaded Successfully")

                # update current item version
                item_id = self.zotero_entry.item["data"]["key"]
                self.zotero_entry.set_item_info(self.zotero_client.item(item_id))
            except Exception as ex:
                messagebox.showerror("Error", str(ex))
        else:
            tk.messagebox.showerror("Error", "Please select an item.")
