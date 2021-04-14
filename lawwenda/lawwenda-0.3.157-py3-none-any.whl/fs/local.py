# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

"""
Local filesystem implementation.
"""

import datetime
import os
import shutil

import lawwenda._aux.PiMetadataInterpreter.pimetadatainterpreter as pimetadatainterpreter

import lawwenda.fs


# pylint: disable=too-many-public-methods
class LocalFilesystem(lawwenda.fs.Filesystem):
    """
    A :py:class:`Filesystem` implementation that resembles a particular subtree of your real local filesystem.
    """

    def __init__(self, rootpath: str):
        super().__init__()
        self.__rootpath = rootpath

    def __path_to_fullpath(self, path: str) -> str:
        result = self.sanitize_abspath(f"{self.__rootpath}/{path}")
        if not f"{result}/".startswith(f"{self.__rootpath}/"):
            raise PermissionError(f"path '{path}' is outside of the specified filesystem.")
        return result

    def try_get_fullpath(self, handle, *, writable):
        return self.__path_to_fullpath(handle.writable_node.path if writable else handle.readable_node.path)

    def child_nodes(self, handle):
        result = []
        hpath = handle.readable_node.path
        for cname in os.listdir(self.__path_to_fullpath(hpath)):
            result.append(self.node_by_path(f"{hpath}/{cname}"))
        return result

    def is_hidden(self, handle):
        return handle.readable_node.name.startswith(".")

    def is_dir(self, handle):
        return os.path.isdir(self.__path_to_fullpath(handle.readable_node.path))

    def is_file(self, handle):
        return os.path.isfile(self.__path_to_fullpath(handle.readable_node.path))

    def is_link(self, handle):
        return os.path.islink(self.__path_to_fullpath(handle.readable_node.path))

    def exists(self, handle):
        return os.path.lexists(self.__path_to_fullpath(handle.readable_node.path))

    def size(self, handle):
        return os.path.getsize(self.__path_to_fullpath(handle.readable_node.path))

    def mtime(self, handle):
        nmtime = os.path.getmtime(self.__path_to_fullpath(handle.readable_node.path))
        return datetime.datetime.fromtimestamp(nmtime)

    def comment(self, handle):
        return pimetadatainterpreter.get_interpreter(self.__path_to_fullpath(handle.readable_node.path)).comment()

    def rating(self, handle):
        return pimetadatainterpreter.get_interpreter(self.__path_to_fullpath(handle.readable_node.path)).rating()

    def tags(self, handle):
        return [tg.tagname() for tg in pimetadatainterpreter.get_interpreter(self.__path_to_fullpath(
            handle.readable_node.path)).tags()]

    def geo(self, handle):
        return pimetadatainterpreter.get_interpreter(self.__path_to_fullpath(handle.readable_node.path)).geo()

    def delete(self, handle):
        hfullpath = self.__path_to_fullpath(handle.writable_node.path)
        if handle.writable_node.is_link:
            os.unlink(hfullpath)
        elif handle.writable_node.is_dir:
            shutil.rmtree(hfullpath)
        else:
            os.unlink(hfullpath)

    def mkdir(self, handle):
        os.makedirs(self.__path_to_fullpath(handle.writable_node.path), exist_ok=True)

    def copy_to(self, srchandle, desthandle):
        # TODO metadata, xattr, ... (also for dirs!)
        # TODO what with links
        srcreadnode = srchandle.readable_node
        destwritenode = desthandle.writable_node
        if srcreadnode.is_dir:
            destwritenode.mkdir()
            for child in srcreadnode.child_nodes:
                self.copy_to(self.get_readhandle(child), self.get_writehandle(destwritenode.child_by_name(child.name)))
        else:
            shutil.copyfile(self.__path_to_fullpath(srcreadnode.path),
                            self.__path_to_fullpath(destwritenode.path))

    def move_to(self, srchandle, desthandle):
        os.rename(self.__path_to_fullpath(srchandle.writable_node.path),
                  self.__path_to_fullpath(desthandle.writable_node.path))

    def set_comment(self, handle, comment):
        pimetadatainterpreter.get_interpreter(self.__path_to_fullpath(handle.writable_node.path)).set_comment(comment)

    def set_geo(self, handle, geo):
        pimetadatainterpreter.get_interpreter(self.__path_to_fullpath(handle.writable_node.path)).set_geo(geo)

    def set_rating(self, handle, rating):
        pimetadatainterpreter.get_interpreter(self.__path_to_fullpath(handle.writable_node.path)).set_rating(rating)

    def add_tag(self, handle, tag):
        pimetadatainterpreter.get_interpreter(self.__path_to_fullpath(handle.writable_node.path)).add_tag(tagname=tag)

    def remove_tag(self, handle, tag):
        pimetadatainterpreter.get_interpreter(self.__path_to_fullpath(handle.writable_node.path)).remove_tag(tag)

    def read_file(self, handle):
        return open(self.__path_to_fullpath(handle.readable_node.path), "rb")

    def write_file(self, handle, content):
        handle.writable_node.parent_node.mkdir()
        with open(self.__path_to_fullpath(handle.writable_node.path), "wb") as f:
            if isinstance(content, bytes):
                f.write(content)
            else:
                while True:
                    buf = content.read(8096)
                    if len(buf) == 0:
                        break
                    f.write(buf)

    def known_tags(self):
        return ["foo", "bar", "baz"]
