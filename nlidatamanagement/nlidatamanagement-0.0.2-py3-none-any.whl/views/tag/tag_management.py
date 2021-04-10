import tkinter as tk

import attr

from nlidatamanagement.tags import TagList


@attr.s(kw_only=True)
class TagManagement(object):
    parent_frame = attr.ib(validator=attr.validators.instance_of(tk.Frame))
    tag_list = attr.ib(validator=attr.validators.instance_of(TagList))
    tag_list_var = attr.ib(validator=attr.validators.instance_of(tk.StringVar))
    user_name = attr.ib(validator=attr.validators.instance_of(str))

    def generate_tag_management_win(self):
        tags_manage_win = tk.Toplevel(self.parent_frame)
        tags_manage_win.title('Tags Management')
        tags_manage_win.grid_columnconfigure([0, 1], weight=1)

        tags_list_box = tk.Listbox(
                tags_manage_win,
                listvariable=self.tag_list_var,
                selectmode=tk.SINGLE,
                relief=tk.RIDGE,
                borderwidth=2,
                width=35
                )
        tags_list_box.grid(row=0, column=0, padx=5, pady=5, sticky='N' + 'S' + 'W' + 'E')

        def on_select(evt):
            """Tag box on select event listener."""
            w = evt.widget
            indices = w.curselection()

            # prevent the out of range issue
            if len(indices) != 1:
                return
            index = indices[0]
            tag = self.tag_list[index]

            tag_name_box.configure(state=tk.NORMAL)
            tag_name_box.delete('1.0', tk.END)
            tag_name_box.insert(tk.END, tag.name)
            tag_name_box.configure(state=tk.DISABLED)

            tag_author_box.configure(state=tk.NORMAL)
            tag_author_box.delete('1.0', tk.END)
            tag_author_box.insert(tk.END, tag.modified_by)
            tag_author_box.configure(state=tk.DISABLED)

            tag_time_box.configure(state=tk.NORMAL)
            tag_time_box.delete('1.0', tk.END)
            tag_time_box.insert(tk.END, tag.modified_at.strftime('%m/%d/%y %H:%M:%S'))
            tag_time_box.configure(state=tk.DISABLED)

            tag_description_box.configure(state=tk.NORMAL)
            tag_description_box.delete('1.0', tk.END)
            tag_description_box.insert(tk.END, tag.description)
            tag_description_box.configure(state=tk.DISABLED)

        tags_list_box.bind('<<ListboxSelect>>', on_select)

        # ----------------------- tag info frame begin ----------------------- #
        tag_info_frame = tk.Frame(
                master=tags_manage_win,
                relief=tk.RAISED,
                borderwidth=1
                )
        tag_info_frame.grid(row=0, column=1, sticky='N' + 'S' + 'W' + 'E')

        tk.Label(tag_info_frame, text="Modified by: ").grid(row=0, column=0, sticky='N' + 'S' + 'W' + 'E')
        # width, height = 20, 10
        tag_author_box = tk.Text(
                tag_info_frame,
                relief=tk.RIDGE,
                borderwidth=1,
                height=1,
                width=30,
                state=tk.DISABLED
                )
        tag_author_box.grid(row=0, column=1, sticky='N' + 'S' + 'W' + 'E')

        tk.Label(tag_info_frame, text="Modified at: ").grid(row=1, column=0, sticky='N' + 'S' + 'W' + 'E')
        # width, height = 20, 10
        tag_time_box = tk.Text(
                tag_info_frame,
                relief=tk.RIDGE,
                borderwidth=1,
                height=1,
                width=30,
                state=tk.DISABLED
                )
        tag_time_box.grid(row=1, column=1, sticky='N' + 'S' + 'W' + 'E')

        tk.Label(tag_info_frame, text="Tag Name: ").grid(row=2, column=0, sticky='N' + 'S' + 'W' + 'E')
        # width, height = 20, 10
        tag_name_box = tk.Text(
                tag_info_frame,
                relief=tk.RIDGE,
                borderwidth=1,
                height=1,
                width=30,
                state=tk.DISABLED
                )
        tag_name_box.grid(row=2, column=1, sticky='N' + 'S' + 'W' + 'E')

        tk.Label(
                tag_info_frame,
                text="Tag Description"
                ).grid(row=3, column=0, columnspan=2, sticky='NSWE')
        # width, height = 20, 10
        tag_description_box = tk.Text(
                tag_info_frame,
                relief=tk.RIDGE,
                borderwidth=1,
                width=30,
                state=tk.DISABLED
                )
        tag_description_box.grid(row=4, column=0, columnspan=2, sticky='N' + 'S')

        # ----------------------- button frame begin ----------------------- #
        btn_frame = tk.Frame(
                master=tag_info_frame,
                borderwidth=0
                )
        btn_frame.grid(row=5, column=0, columnspan=2, sticky='N' + 'S' + 'W' + 'E')

        btn_frame.columnconfigure([0, 1, 2], weight=1)

        tag_delete_btn = tk.Button(
                btn_frame,
                text='Delete',
                padx=3,
                command=lambda: self._generate_tag_delete_win(tags_manage_win, tags_list_box)
                )
        tag_delete_btn.grid(row=0, column=0, sticky='N' + 'S' + 'W' + 'E')

        tag_edit_btn = tk.Button(
                btn_frame,
                text='Edit',
                padx=3,
                command=lambda: self._generate_tag_edit_win(tags_manage_win, tags_list_box)
                )
        tag_edit_btn.grid(row=0, column=1, sticky='N' + 'S' + 'W' + 'E')

        tag_add_btn = tk.Button(
                btn_frame,
                text='Add',
                padx=3,
                command=lambda: self._generate_tag_add_win(tags_manage_win)
                )
        tag_add_btn.grid(row=0, column=2, sticky='N' + 'S' + 'E' + 'W')
        # ----------------------- button frame end ----------------------- #

        # ----------------------- tag info frame end ----------------------- #

    def _generate_tag_add_win(self, parent):
        tag_add_win = tk.Toplevel(parent)
        tag_add_win.title('Add Tag')
        tk.Label(tag_add_win, text="Tag Name: ").grid(row=0, column=0, sticky='N' + 'S' + 'W' + 'E')
        tag_name_box = tk.Entry(
                tag_add_win,
                relief=tk.RIDGE,
                borderwidth=1,
                width=30
                )
        tag_name_box.grid(row=0, column=1, sticky='N' + 'S' + 'W' + 'E')

        tk.Label(tag_add_win, text="Tag Description: ").grid(row=1, column=0, sticky='NSWE')
        tag_description_box = tk.Text(
                tag_add_win,
                relief=tk.RIDGE,
                borderwidth=1,
                width=30
                )
        tag_description_box.grid(row=1, column=1, sticky='N' + 'S' + 'W' + 'E')

        # generate button
        back_btn = tk.Button(
                tag_add_win,
                text="Back",
                width=15,
                padx=10,
                command=tag_add_win.destroy
                )
        back_btn.grid(row=2, column=0, sticky='N' + 'S' + 'W')

        add_btn = tk.Button(
                tag_add_win,
                text="Add",
                width=15,
                padx=10,
                command=lambda: add_tag()
                )
        add_btn.grid(row=2, column=1, sticky='N' + 'S' + 'E')

        def add_tag():
            tag_name = tag_name_box.get().strip()
            tag_des = tag_description_box.get("1.0", tk.END).strip()
            modified_by = self.user_name
            self.tag_list.add(tag_name, tag_des, modified_by)
            self.tag_list_var.set(self.tag_list.tags_name)

            tag_add_win.destroy()

    def _generate_tag_delete_win(self, parent, tags_list_box):
        tag_delete_win = tk.Toplevel(parent)
        tag_delete_win.title('Delete Tag')
        idx = tags_list_box.curselection()
        if len(idx) == 0:
            tk.messagebox.showerror('Error', 'Make sure you choose one tag.')
            return
        tag = self.tag_list[idx[0]]
        title = tk.Label(
                tag_delete_win,
                text='Are you sure you want to delete ' + tag.name + ' ?'
                )
        title.grid(row=0, column=0, columnspan=2, sticky='N' + 'S' + 'W' + 'E')

        # generate button
        back_btn = tk.Button(
                tag_delete_win,
                text="Back",
                width=15,
                padx=10,
                command=tag_delete_win.destroy
                )
        back_btn.grid(row=1, column=0, sticky='N' + 'S' + 'W')

        delete_btn = tk.Button(
                tag_delete_win,
                text="Delete",
                width=15,
                padx=10,
                command=lambda: delete_tag()
                )
        delete_btn.grid(row=1, column=1, sticky='N' + 'S' + 'E')

        def delete_tag():
            self.tag_list.delete(tag)
            self.tag_list_var.set(self.tag_list.tags_name)

            tag_delete_win.destroy()

    def _generate_tag_edit_win(self, parent, tags_list_box):
        idx = tags_list_box.curselection()
        if len(idx) == 0:
            tk.messagebox.showerror('Error', 'Make sure you choose one tag.')
            return
        tag = self.tag_list[idx[0]]

        tag_edit_win = tk.Toplevel(parent)
        tag_edit_win.title('Edit Tag')
        tk.Label(tag_edit_win, text="Tag Name: ").grid(row=0, column=0, sticky='N' + 'S' + 'W' + 'E')
        tag_name_box = tk.Entry(
                tag_edit_win,
                relief=tk.RIDGE,
                borderwidth=1,
                width=30
                )
        tag_name_box.grid(row=0, column=1, sticky='N' + 'S' + 'W' + 'E')
        tag_name_box.insert(tk.END, tag.name)

        tk.Label(tag_edit_win, text="Tag Description: ").grid(row=1, column=0, sticky='NSWE')
        tag_description_box = tk.Text(
                tag_edit_win,
                relief=tk.RIDGE,
                borderwidth=1,
                width=30
                )
        tag_description_box.grid(row=1, column=1, sticky='N' + 'S' + 'W' + 'E')
        tag_description_box.insert(tk.END, tag.description)

        # generate button
        back_btn = tk.Button(
                tag_edit_win,
                text="Back",
                width=15,
                padx=10,
                command=tag_edit_win.destroy
                )
        back_btn.grid(row=2, column=0, sticky='N' + 'S' + 'W')

        edit_btn = tk.Button(
                tag_edit_win,
                text="Edit",
                width=15,
                padx=10,
                command=lambda: edit_tag()
                )
        edit_btn.grid(row=2, column=1, sticky='N' + 'S' + 'E')

        def edit_tag():
            tag_name = tag_name_box.get().strip()
            tag_des = tag_description_box.get("1.0", tk.END).strip()
            modified_by = self.user_name
            self.tag_list.edit(idx[0], tag_name, tag_des, modified_by)
            self.tag_list_var.set(self.tag_list.tags_name)

            tag_edit_win.destroy()
