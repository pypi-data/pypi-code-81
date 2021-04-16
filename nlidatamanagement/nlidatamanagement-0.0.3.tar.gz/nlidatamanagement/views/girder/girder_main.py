import tkinter as tk

from PIL import ImageTk

from nlidatamanagement.imgs import SETTING_IMG, UPLOAD_IMG
from nlidatamanagement.tags import TagList
from nlidatamanagement.views.girder.girder_choose_file import GirderChooseFile
from nlidatamanagement.views.girder.girder_entry import GirderEntry
from nlidatamanagement.views.girder.girder_file_system import GirderFileSystem
from nlidatamanagement.views.girder.girder_mode import GirderMode, Mode
from nlidatamanagement.views.girder.girder_preview import GirderPreview
from nlidatamanagement.views.tag.tag_main import TagFrame

COLLECTION = 'collection'
FOLDER = 'folder'
ITEM = 'item'
TAG_KEY = 'girder_item_tags'


class GirderUploader:
    def __init__(self, parent_win, girder_connector):
        self.parent_win = parent_win
        self.window = tk.Toplevel(parent_win)
        self.window.title("Upload to Girder")
        self.window.grid_columnconfigure([0, 1, 2], weight=1)
        self.window.grid_rowconfigure(0, weight=1)
        self.girder_connector = girder_connector
        self.girder_client = girder_connector.client

        self.upload_img = ImageTk.PhotoImage(UPLOAD_IMG)
        self.setting_img = ImageTk.PhotoImage(SETTING_IMG)

        tag_frame = tk.Frame(
                master=self.window,
                relief=tk.RAISED,
                borderwidth=1
                )
        tag_frame.grid(row=0, column=0, padx=5, pady=5, rowspan=4, sticky='N' + 'S' + 'W')

        main_frame = tk.Frame(
                master=self.window
                )
        main_frame.grid(row=0, column=1, padx=5, pady=5, sticky='N' + 'W' + 'E' + 'S')
        main_frame.grid_columnconfigure([0, 1], weight=1)

        self.mode_frame = tk.Frame(
                master=main_frame,
                relief=tk.RAISED,
                borderwidth=1
                )
        self.mode_frame.grid(row=0, columnspan=2, padx=5, pady=5, ipadx=3, ipady=3, sticky='N' + 'W' + 'E')

        self.entry_frame = tk.Frame(
                master=main_frame,
                relief=tk.RAISED,
                borderwidth=1
                )
        self.entry_frame.grid(row=1, columnspan=2, padx=5, pady=5, sticky='N' + 'S' + 'E' + 'W')

        self.choose_file_frame = tk.Frame(
                master=main_frame,
                relief=tk.RAISED,
                borderwidth=1
                )
        self.choose_file_frame.grid(row=2, columnspan=2, padx=5, pady=5, sticky='N' + 'S' + 'E' + 'W')

        self.file_sys_frame = tk.Frame(
                master=self.window,
                relief=tk.RAISED,
                borderwidth=1
                )
        self.file_sys_frame.grid(row=0, column=2, padx=5, pady=5, rowspan=4, sticky='N' + 'S' + 'E')

        try:
            self.tag_list = TagList('./tags.csv', self.girder_client)
        except:
            self.window.destroy()
            return

        self.tag_system = TagFrame(
                parent_frame=tag_frame,
                tag_list=self.tag_list,
                user_name=girder_connector.first_name + ' ' + girder_connector.last_name
                )

        self.current_selected_item = None
        self.girder_mode = GirderMode(
                parent_frame=self.mode_frame,
                firstname=girder_connector.first_name,
                lastname=girder_connector.last_name,
                new_item_mode_function=lambda: self.switch_to_new_item_mode(),
                edit_item_mode_function=lambda: self.switch_to_edit_item_mode()
                )

        self.girder_entry = GirderEntry(
                parent_frame=self.entry_frame
                )

        self.girder_choose_file = GirderChooseFile(
                parent_frame=self.choose_file_frame
                )

        self.girder_file_system = GirderFileSystem(
                parent_frame=self.file_sys_frame,
                girder_client=self.girder_client,
                on_item_select=self.on_item_select
                )

        upload_btn = tk.Button(
                master=main_frame,
                image=self.upload_img,
                command=lambda: self.preview_info()
                )
        upload_btn.grid(row=3, column=0, columnspan=2, padx=5, pady=3, sticky='N' + 'S' + 'E' + 'W')

        # setting_btn = tk.Button(
        #     master=main_frame,
        #     image=self.setting_img,
        #     command=lambda: self.setting()
        # )
        # setting_btn.grid(row=3, column=1, padx=5, pady=3, sticky='N'+'S'+'E'+'W')

    def clear(self):
        """Clear all text box and file selections.

        Set all input fields to enable.
        """
        self.current_selected_item = None

        self.tag_system.enable()
        self.tag_system.clear_selection()

        self.girder_entry.enable_item_name_box()
        self.girder_entry.enable_item_description_box()

        self.girder_entry.clear()

        self.girder_choose_file.enable()
        self.girder_choose_file.clear()

        self.girder_file_system.clear()

    def switch_to_new_item_mode(self):
        self.clear()

    def switch_to_edit_item_mode(self):
        self.clear()
        self.girder_entry.disable_item_name_box()

    def on_item_select(self, item_selected):
        """Callback on item selected.
        
        Set item information on girder entry panel.
        """
        self.current_selected_item = item_selected
        current_mode = self.girder_mode.mode
        if not self.current_selected_item:
            if current_mode == Mode.TO_NEW_ITEM:
                self.switch_to_new_item_mode()
            elif current_mode == Mode.TO_EDIT_ITEM:
                self.switch_to_edit_item_mode()
            return

        _id = self.current_selected_item['_id']
        model_type = self.current_selected_item['_modelType']

        if current_mode == Mode.TO_NEW_ITEM:
            if model_type == FOLDER:
                # update folder info
                self.girder_entry.set_folder_id(_id)

        elif current_mode == Mode.TO_EDIT_ITEM:
            if model_type == ITEM:
                folder_id = self.current_selected_item['folderId']
                description = self.current_selected_item['description']
                item_name = self.current_selected_item['name']
                meta = self.current_selected_item['meta']
                if TAG_KEY in meta:
                    tags = meta[TAG_KEY]
                else:
                    tags = []

                self.girder_entry.set_folder_id(folder_id)
                self.girder_entry.set_item_name(item_name)
                self.girder_entry.set_item_description(description)

                self.tag_system.clear_selection()
                for tag in tags:
                    idx = self.tag_list.index(tag)
                    self.tag_system.set_selection(idx)

    def on_item_upload(self):
        """Callback for item uploaded. 
        
        Refresh girder file system.
        """
        self.girder_file_system.refresh()

    def on_connect(self, girder_connector):
        """Destroy the current window and open a new window with the new connector."""
        self.window.destroy()
        GirderUploader(self.parent_win, girder_connector)

    def preview_info(self):
        """Create a new window to preview the information before upload."""
        current_mode = self.girder_mode.mode
        item = self.current_selected_item
        if not item:
            tk.messagebox.showerror('Error', f'Please select an item')
            return
        item_type = item['_modelType']
        item_name = item['name']
        if current_mode == Mode.TO_NEW_ITEM:
            if item_type != FOLDER:
                tk.messagebox.showerror('Error',
                                        f'Please select a Girder {FOLDER}. Current Selected: {item_type} {item_name}')
                return
            GirderPreview(
                    folder_id=item['_id'],
                    folder_name=item_name,
                    item_id='TBD',
                    item_name=self.girder_entry.item_name,
                    item_description=self.girder_entry.item_description,
                    file_paths=self.girder_choose_file.file_paths,
                    file_names=self.girder_choose_file.file_names,
                    chosen_tags=self.tag_system.get_selection_as_list(),
                    mode=current_mode,
                    parent_win=self.window,
                    girder_client=self.girder_client,
                    on_item_upload=self.on_item_upload
                    )
        elif current_mode == Mode.TO_EDIT_ITEM:
            if item_type != ITEM:
                tk.messagebox.showerror('Error',
                                        f'Please select a Girder {ITEM}. Current Selected: {item_type} {item_name}')
                return
            GirderPreview(
                    folder_id=item['folderId'],
                    folder_name='N/A',
                    item_id=item['_id'],
                    item_name=item_name,
                    item_description=self.girder_entry.item_description,
                    file_paths=self.girder_choose_file.file_paths,
                    file_names=self.girder_choose_file.file_names,
                    chosen_tags=self.tag_system.get_selection_as_list(),
                    mode=current_mode,
                    parent_win=self.window,
                    girder_client=self.girder_client,
                    on_item_upload=self.on_item_upload
                    )

    # def setting(self):
    #     GirderSetting(
    #         parent_win=self.window,
    #         girder_connector=self.girder_connector,
    #         on_connect=lambda parent_win, girder_connector: self.on_connect(parent_win, girder_connector)
    #     )
