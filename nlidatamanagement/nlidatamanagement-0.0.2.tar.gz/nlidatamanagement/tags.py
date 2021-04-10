import csv
from datetime import datetime
import io
import os
from tkinter import messagebox

import attr
import girder_client
import pandas as pd
from pytablewriter import MarkdownTableWriter
from pytablewriter.style import Style

TITLE = ["name", "description", "modified_by", "modified_at"]


@attr.s(kw_only=True)
class Tag(object):
    name = attr.ib(validator=attr.validators.instance_of(str))
    description = attr.ib(validator=attr.validators.instance_of(str), default="")
    modified_by = attr.ib(validator=attr.validators.instance_of(str))
    modified_at = attr.ib(validator=attr.validators.instance_of(datetime))

    def __iter__(self):
        for value in vars(self).values():
            if isinstance(value, datetime):
                value = value.strftime("%m/%d/%y %H:%M:%S")
            yield value

    def __eq__(self, obj):
        return isinstance(obj, Tag) and self.name == obj.name


@attr.s
class TagList(object):
    """A data class for a list of tags."""

    filepath = attr.ib(validator=attr.validators.instance_of(str))
    client = attr.ib(validator=attr.validators.instance_of(girder_client.GirderClient))

    _folder_id = attr.ib(init=False, validator=attr.validators.instance_of(str))
    _csv_id = attr.ib(init=False, validator=attr.validators.instance_of(str))
    _md_id = attr.ib(init=False, validator=attr.validators.instance_of(str))
    _html_id = attr.ib(init=False, validator=attr.validators.instance_of(str))
    _user = attr.ib(init=False, validator=attr.validators.instance_of(dict))
    _tag_list = attr.ib(factory=list)

    def __attrs_post_init__(self):
        # user info
        self._user = self.client.get(path="/user/me")
        # load from system setting
        tag_list_from_sys = self.client.get("/resource/tags")

        # load from csv
        tag_list_from_csv = []

        data_management_collection = None
        for collection in self.client.listCollection():
            if collection["name"] == "Data Management Sys":
                data_management_collection = collection

        if not data_management_collection:
            raise Exception("Can't find Data Management Sys Collection")

        tag_folder = next(
                self.client.listFolder(
                        data_management_collection["_id"],
                        parentFolderType="collection",
                        name="Tags",
                        )
                )
        if tag_folder is None:
            raise Exception(
                    "Can't find Tags Folder under Data Management Sys Collection"
                    )

        self._folder_id = tag_folder["_id"]
        tags_item = next(self.client.listItem(tag_folder["_id"], name="tags"))
        read_me = next(self.client.listItem(tag_folder["_id"], name="README.md"))
        if tags_item is None:
            raise Exception("Can't find tags item undder Tags Folder")

        for file in self.client.listFile(tags_item["_id"]):
            if file["name"] == "tags.csv":
                self._csv_id = file["_id"]
            elif file["name"] == "tags.htm":
                self._html_id = file["_id"]

        for file in self.client.listFile(read_me["_id"]):
            if file["name"] == "README.md":
                self._md_id = file["_id"]

        self.client.downloadFile(self._csv_id, self.filepath)
        with open(self.filepath, "r") as csvfile:
            tag_reader = csv.reader(csvfile)
            next(tag_reader)  # omit field row
            for row in tag_reader:
                tag = Tag(
                        name=row[0],
                        description=row[1],
                        modified_by=row[2],
                        modified_at=datetime.strptime(row[3], "%m/%d/%y %H:%M:%S"),
                        )
                tag_list_from_csv.append(tag)

        tag_name_set_csv = set([tag.name for tag in tag_list_from_csv])
        tag_name_set_sys = set(tag_list_from_sys)

        if tag_name_set_csv != tag_name_set_sys:
            sync = messagebox.askquestion(
                    title="Warning",
                    message="Tag conflict detected. Do you want to synchronize the tag list from system setting?",
                    icon="warning",
                    )
            if sync == "yes" and self._check_access():
                user_name = self._user["firstName"] + " " + self._user["lastName"]
                tag_list_from_csv = [
                    tag for tag in tag_list_from_csv if tag.name in tag_name_set_sys
                    ]

                for tag_name in tag_list_from_sys:
                    if tag_name not in tag_name_set_csv:
                        tag_list_from_csv.append(
                                Tag(
                                        name=tag_name,
                                        modified_by=user_name,
                                        modified_at=datetime.now(),
                                        )
                                )
            else:
                raise Exception("Sync Fail")

        self._tag_list = tag_list_from_csv
        self._sort()
        if self._check_access(showerror=False):
            self._save()
        attr.validate(self)

    @property
    def tags_name(self):
        tags_name_lst = []
        for tag in self._tag_list:
            tags_name_lst.append(tag.name)
        return tags_name_lst

    def __getitem__(self, index: int):
        return self._tag_list[index]

    def _sort(self):
        """Sort tag list by name."""

        def sort_by_name(entry):
            return entry.name

        self._tag_list.sort(key=sort_by_name)

    def add(self, tag_name, tag_description, modified_by):
        if self._check_access():
            tag = Tag(
                    name=tag_name,
                    description=tag_description,
                    modified_by=modified_by,
                    modified_at=datetime.now(),
                    )
            self._tag_list.append(tag)
            self._sort()
            self._save()

    def edit(self, idx, tag_name, tag_des, modified_by):
        if self._check_access():
            tag = self._tag_list[idx]
            tag.name = tag_name
            tag.description = tag_des
            tag.modified_by = modified_by
            tag.modified_at = datetime.now()
            self._sort()
            self._save()

    def delete(self, tag):
        if self._check_access():
            self._tag_list.remove(tag)
            self._sort()
            self._save()

    def index(self, tag_name):
        for i, tag in enumerate(self._tag_list):
            if tag.name == tag_name:
                return i
        return -1

    def _save(self):
        with open(self.filepath, "w") as csvfile:
            tag_writer = csv.writer(csvfile)
            tag_writer.writerow(TITLE)
            tag_writer.writerows(self._tag_list)

        pd_csv = pd.read_csv(self.filepath)
        htm_str = pd_csv.to_html(index=False, justify="center")
        md_writer = MarkdownTableWriter()
        md_writer.column_styles = [Style(align="center") for _ in range(4)]
        md_writer.table_name = "Tags"
        md_writer.from_dataframe(pd_csv)
        md_str = md_writer.dumps()

        self._upload_to_girder(self.tags_name, self.filepath, htm_str, md_str)

    def _check_access(self, showerror=True) -> bool:
        """If current user is admin.

        Admin permission required for tag modification.
        """
        if not self._user["admin"]:
            if showerror:
                messagebox.showerror(
                        title="Error",
                        message="Modification access denied. Please contact the admin.",
                        )
            return False
        return True

    def _upload_to_girder(self, tag_list, csv_file_path, htm_str, md_str):
        """Upload tag files to girder.

        tag_list -- a list of tag name
        csv_file_path -- file path to the csv tag file
        htm_str -- string contains tag info in html
        md_str -- string contains tag info in markdown
        """
        f = open(csv_file_path, "rb")
        size = os.path.getsize(csv_file_path)
        self.client.uploadFileContents(self._csv_id, f, size)

        f = io.StringIO(md_str)
        size = len(md_str)
        self.client.uploadFileContents(self._md_id, f, size)

        f = io.StringIO(htm_str)
        size = len(htm_str)
        self.client.uploadFileContents(self._html_id, f, size)

        parameters = {
            "key": "item_tags.tag_list",
            "value": str(tag_list).replace("'", '"'),
            }
        self.client.put("/system/setting", parameters=parameters)
