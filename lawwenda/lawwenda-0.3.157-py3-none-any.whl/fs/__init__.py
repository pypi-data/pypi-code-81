# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

"""
Lawwenda abstract filesystem.

Lawwenda usually shows a subtree of the local filesystem, but could also work with something completely different. This
module implements the basic infrastructure for that.
"""

import datetime
import logging
import mimetypes
import os
import traceback
import typing as t

import lawwenda._aux.PiMetadataInterpreter.pimetadatainterpreter as pimetadatainterpreter

import lawwenda.fs.data
import lawwenda.previewer.commonimages
import lawwenda.previewer.commonvideos


# pylint: disable=no-self-use,too-many-public-methods
class Filesystem:
    """
    Base class for a filesystem source implementation.

    Subclasses implement different kinds of filesystems, e.g. :py:class:`lawwenda.fs.local.LocalFilesystem`.

    You should not use this interface directly for much more than getting its :py:attr:`rootnode`. It provides a
    friendlier and equally powerful interface. The interface of this class is relevant for implementing custom
    filesystems only.

    |dontconstruct|
    """

    class ReadHandle:
        """
        Read and write handles are just a stupid container that hold one :py:class:`Filesystem.Node`.

        This looks stupid at first, because you could just use this node directly instead. The added value of handles
        are a central mechanism for access control, which would be a bit less obvious and more scattered in code without
        this indirection.

        Of course it cannot avoid a way around it in code. An attacker that can change the code has won anyway. It just
        simplifies writing correct code that hopefully does not provide ways around it for the client.

        See :py:meth:`Filesystem.get_readhandle` and :py:meth:`Filesystem.get_writehandle`.
        """

        def __init__(self, node: "Filesystem.Node"):
            self.readable_node = node

    class WriteHandle(ReadHandle):
        """
        See :py:class:`Filesystem.ReadHandle`.
        """

        def __init__(self, node: "Filesystem.Node"):
            super().__init__(node)
            self.writable_node = node

    def __init__(self):
        self.__previewers = [lawwenda.previewer.commonimages.CommonImagesPreviewer(),
                             lawwenda.previewer.commonvideos.CommonVideosPreviewer()]
        # TODO text, pdf, libreoffice, audio (without thumbnails though), ... ?!

    @staticmethod
    def sanitize_abspath(path: str) -> str:
        """
        Sanitize slashes in a path and returns a path in the form `/foo/bar`.

        Precisely:

        - with a slash in the beginning
        - without a slash at the end (exception: root path)
        - without double slashes
        - with `..` and `.` resolved
        - root path: `/`

        :param path: The input path.
        """
        path = os.path.abspath(f"/{path}")
        while "//" in path:
            path = path.replace("//", "/")
        while path[1:].endswith("/"):
            path = path[:-1]
        return path

    @property
    def rootnode(self) -> "Filesystem.Node":
        """
        The root node of this filesystem.
        """
        return self.node_by_path("")

    def node_by_path(self, path: str) -> "Filesystem.Node":
        """
        Return a node by a given path.

        It will not fail, even if there is no such file or access would be denied.

        :param path: The path of the node to return, relative to the filesystem's root node.
        """
        return Filesystem.Node(path, filesystem=self)

    def get_readhandle(self, node: "Filesystem.Node") -> "Filesystem.ReadHandle":
        """
        Return a read handle for a node.

        Such handles are needed for executing read actions on that node. See also :py:class:`Filesystem.ReadHandle`.

        :param node: The node to read from later.
        """
        return self.ReadHandle(node)

    def get_writehandle(self, node: "Filesystem.Node") -> "Filesystem.WriteHandle":
        """
        Return a write handle for a node.

        Such handles are needed for executing write actions on that node. See also :py:class:`Filesystem.WriteHandle`.

        :param node: The node to write from later.
        """
        return self.WriteHandle(node)

    def try_get_fullpath(self, handle: t.Union["Filesystem.ReadHandle", "Filesystem.WriteHandle"], *,
                         writable: bool) -> t.Optional[str]:
        """
        Try to return an absolute path in the local filesystem for a node (in a handle).

        This is optional and the default implementation returns `None`.

        :param handle: The read or write handle to a node.
        :param writable: Whether you might do any write accesses to the result path.
        """
        # pylint: disable=unused-argument
        return None

    def child_nodes(self, handle: "Filesystem.ReadHandle") -> t.List["Filesystem.Node"]:
        """
        Return all child nodes for a node (in a handle).

        :param handle: The read handle to a node.
        """
        raise NotImplementedError()

    def is_hidden(self, handle: "Filesystem.ReadHandle") -> bool:
        """
        Return whether a node (in a handle) is hidden.

        :param handle: The read handle to a node.
        """
        raise NotImplementedError()

    def is_dir(self, handle: "Filesystem.ReadHandle") -> bool:
        """
        Return whether a node (in a handle) is a directory.

        This is also `True` for link nodes (see :py:meth:`is_link`) that point to a directory!

        :param handle: The read handle to a node.
        """
        raise NotImplementedError()

    def is_file(self, handle: "Filesystem.ReadHandle") -> bool:
        """
        Return whether a node (in a handle) is a regular file.

        This is also `True` for link nodes (see :py:meth:`is_link`) that point to a file!

        :param handle: The read handle to a node.
        """
        raise NotImplementedError()

    def is_link(self, handle: "Filesystem.ReadHandle") -> bool:
        """
        Return whether a node (in a handle) is a link. If this is a resolvable link, some of the other `is_` flags are
        `True` as well.

        Resolving links is always done internally by the filesystem implementation. It is usually not required to know
        the link target in order to use the node.

        :param handle: The read handle to a node.
        """
        raise NotImplementedError()

    def exists(self, handle: "Filesystem.ReadHandle") -> bool:  # TODO xx noh review complete module
        """
        Return whether a node (in a handle) points to something that actually exists.

        This can e.g. be `False` for nodes coming from :py:meth:`node_by_path`.

        :param handle: The read handle to a node.
        """
        raise NotImplementedError()

    def size(self, handle: "Filesystem.ReadHandle") -> int:
        """
        Return the size of a node (in a handle) in bytes.

        :param handle: The read handle to a node.
        """
        raise NotImplementedError()

    def mimetype(self, handle: "Filesystem.ReadHandle") -> str:
        """
        Return the mimetype of a node (in a handle).

        :param handle: The read handle to a node.
        """
        return mimetypes.guess_type(handle.readable_node.name, strict=False)[0] or ""

    def mtime(self, handle: "Filesystem.ReadHandle") -> datetime.datetime:
        """
        Return the 'last modified' time of a node (in a handle).

        :param handle: The read handle to a node.
        """
        raise NotImplementedError()

    def has_thumbnail(self, handle: "Filesystem.ReadHandle") -> bool:
        """
        Return whether there could be a thumbnail available for a node (in a handle).

        See also :py:meth:`thumbnail`.

        There might be cases when it returns `True` but the thumbnail generation will fail.

        :param handle: The read handle to a node.
        """
        if not handle.readable_node.is_file:
            return False
        iar = lawwenda.previewer.IsAbleRequest(handle.readable_node.name, handle.readable_node.mimetype)
        for previewer in self.__previewers:
            try:
                if previewer.is_thumbnailable(iar):
                    return True
            except Exception:  # pylint: disable=broad-except
                logging.error(traceback.format_exc())
        return False

    def has_preview(self, handle: "Filesystem.ReadHandle") -> bool:
        """
        Return whether there could be a html preview snippet available for a node (in a handle).

        See also :py:meth:`preview_html`.

        There might be cases when it returns `True` but the preview generation will fail.

        :param handle: The read handle to a node.
        """
        if not handle.readable_node.is_file:
            return False
        iar = lawwenda.previewer.IsAbleRequest(handle.readable_node.name, handle.readable_node.mimetype)
        for previewer in self.__previewers:
            try:
                if previewer.is_previewable(iar):
                    return True
            except Exception:  # pylint: disable=broad-except
                logging.error(traceback.format_exc())
        return False

    def comment(self, handle: "Filesystem.ReadHandle") -> str:
        """
        Return the comment assigned to a node (in a handle).

        :param handle: The read handle to a node.
        """
        raise NotImplementedError()

    def rating(self, handle: "Filesystem.ReadHandle") -> int:
        """
        Return the rating assigned to a node (in a handle).

        :param handle: The read handle to a node.
        """
        raise NotImplementedError()

    def tags(self, handle: "Filesystem.ReadHandle") -> t.List[str]:
        """
        Return the tags that are assigned to a node (in a handle).

        :param handle: The read handle to a node.
        """
        raise NotImplementedError()

    def geo(self, handle: "Filesystem.ReadHandle") -> t.Union["lawwenda.fs.data.GeoLocation", t.Dict[str, t.Any]]:
        """
        Return the geographic location associated to a node (in a handle).

        :param handle: The read handle to a node.
        """
        raise NotImplementedError()

    def preview_html(self, handle: "Filesystem.ReadHandle") -> str:
        """
        Return an html snippet that shows a preview of a node (in a handle).

        This is larger and richer in terms of flexibility than thumbnails, and is typically used by the file details
        panel.

        See also :py:meth:`has_preview`.

        :param handle: The read handle to a node.
        """
        iar = lawwenda.previewer.IsAbleRequest(handle.readable_node.name, handle.readable_node.mimetype)
        for previewer in self.__previewers:
            try:
                if previewer.is_previewable(iar):
                    return previewer.preview_html(handle.readable_node)
            except Exception:  # pylint: disable=broad-except
                logging.error(traceback.format_exc())
        return ""

    def thumbnail(self, handle: "Filesystem.ReadHandle") -> bytes:
        """
        Return a thumbnail for a node (in a handle) in PNG format.

        See also :py:meth:`has_thumbnail`.

        :param handle: The read handle to a node.
        """
        iar = lawwenda.previewer.IsAbleRequest(handle.readable_node.name, handle.readable_node.mimetype)
        for previewer in self.__previewers:
            try:
                if previewer.is_thumbnailable(iar):
                    return previewer.thumbnail(handle.readable_node)
            except Exception:  # pylint: disable=broad-except
                logging.error(traceback.format_exc())
        return b""

    def delete(self, handle: "Filesystem.WriteHandle") -> None:
        """
        Delete a node (in a handle).

        :param handle: The write handle to a node.
        """
        raise NotImplementedError()

    def mkdir(self, handle: "Filesystem.WriteHandle") -> None:
        """
        Make a node (in a handle) an existing directory.

        :param handle: The write handle to a node.
        """
        raise NotImplementedError()

    def copy_to(self, srchandle: "Filesystem.ReadHandle", desthandle: "Filesystem.WriteHandle") -> None:
        """
        Copy a node (in a handle) to another node (in a handle).

        After copying, the destination node has similar characteristics as the source node, i.e. either is a file
        with the same content, or is a directory with the same subitems as the source.

        :param srchandle: The read handle to the source node.
        :param desthandle: The write handle to the destination node.
        """
        raise NotImplementedError()

    def move_to(self, srchandle: "Filesystem.WriteHandle", desthandle: "Filesystem.WriteHandle") -> None:
        """
        Move a node (in a handle) to another node (in a handle).

        This is similar to :py:meth:`copy_to`; see there for more details.

        :param srchandle: The write handle to the source node.
        :param desthandle: The write handle to the destination node.
        """
        raise NotImplementedError()

    def set_comment(self, handle: "Filesystem.WriteHandle", comment: str) -> None:
        """
        Set the comment for a node (in a handle).

        :param handle: The write handle to a node.
        :param comment: The new comment.
        """
        raise NotImplementedError()

    def set_geo(self, handle: "Filesystem.WriteHandle", geo: str) -> None:
        """
        Set the geographic location for a node (in a handle).

        :param handle: The write handle to a node.
        :param geo: The new geographic location (as encoded string).
        """
        raise NotImplementedError()

    def set_rating(self, handle: "Filesystem.WriteHandle", rating: int) -> None:
        """
        Set the rating for a node (in a handle).

        :param handle: The write handle to a node.
        :param rating: The new rating.
        """
        raise NotImplementedError()

    def add_tag(self, handle: "Filesystem.WriteHandle", tag: str) -> None:
        """
        Add a tag to a node (in a handle).

        :param handle: The write handle to a node.
        :param tag: The tag to add.
        """
        raise NotImplementedError()

    def remove_tag(self, handle: "Filesystem.WriteHandle", tag: str) -> None:
        """
        Remove a tag from a node (in a handle).

        :param handle: The write handle to a node.
        :param tag: The tag to remove.
        """
        raise NotImplementedError()

    def read_file(self, handle: "Filesystem.ReadHandle") -> t.BinaryIO:
        """
        Return a file-like object for reading content of a node (in a handle).

        The caller must ensure that it gets closed after usage, usually by means of the Python `with` keyword.

        :param handle: The read handle to a node.
        """
        raise NotImplementedError()

    def write_file(self, handle: "Filesystem.WriteHandle", content: t.Union[bytes, t.BinaryIO]) -> None:
        """
        Write content to a node (in a handle).

        This will overwrite its original content.

        :param handle: The write handle to a node.
        :param content: The binary content to write to the node.
        """
        raise NotImplementedError()

    def known_tags(self) -> t.List[str]:
        """
        TODO.
        """
        raise NotImplementedError()

    class Node:  # TODO __eq__ method
        """
        TODO.
        """

        def __init__(self, path: str, *, filesystem: "Filesystem"):
            self.__path = filesystem.sanitize_abspath(path)
            self.__filesystem = filesystem

        @property
        def path(self) -> str:
            """
            The path of this node.

            This is similar to a Unix filesystem path, i.e. path segments are separated by `"/"`.

            This path will always be considered as relative to the root node of the :py:attr:`_filesystem` it is part
            of. It is not relative to '`/`' of your real filesystem (unless you have actually set up a
            :py:class:`Filesystem` that resembles your entire real filesystem).
            """
            return self.__path

        @property
        def _filesystem(self) -> "Filesystem":
            return self.__filesystem

        @property
        def name(self) -> str:
            """
            The file name of the node.

            This is the last segment of :py:attr:`path`.
            """
            return os.path.basename(self.__path)

        @property
        def dirpath(self) -> str:
            """
            The directory path of the node.

            This is all but the last segment of :py:attr:`path`. Same as :py:attr:`path` of :py:attr:`parent_node`.
            """
            return os.path.dirname(self.__path)

        @property
        def is_writable(self) -> bool:
            """
            Whether the node is writable.
            """
            try:
                self.__filesystem.get_writehandle(self)
                return True
            except Exception:  # pylint: disable=broad-except
                return False

        @property
        def is_hidden(self) -> bool:
            """
            Whether the node is hidden.
            """
            return self.__filesystem.is_hidden(self.__filesystem.get_readhandle(self))

        @property
        def is_dir(self) -> bool:
            """
            Whether the node is a directory.

            This is also `True` for link nodes (see :py:meth:`is_link`) that point to a directory!
            """
            return self.__filesystem.is_dir(self.__filesystem.get_readhandle(self))

        @property
        def is_file(self) -> bool:
            """
            Whether the node is a regular file.

            This is also `True` for link nodes (see :py:meth:`is_link`) that point to a directory!
            """
            return self.__filesystem.is_file(self.__filesystem.get_readhandle(self))

        @property
        def is_link(self) -> bool:
            """
            Whether the node is a link. If this is a resolvable link, some of the other `is_` flags are `True` as well.

            Resolving links is always done internally by the filesystem implementation. It is usually not required to
            know the link target in order to use the node.
            """
            return self.__filesystem.is_link(self.__filesystem.get_readhandle(self))

        @property
        def exists(self) -> bool:
            """
            Whether a node points to something that actually exists.

            This can e.g. be `False` for nodes coming from :py:meth:`child_by_name`.
            """
            return self.__filesystem.exists(self.__filesystem.get_readhandle(self))

        @property
        def size(self) -> int:
            """
            The size of this node in bytes.
            """
            return self.__filesystem.size(self.__filesystem.get_readhandle(self))

        @property
        def mimetype(self) -> str:
            """
            The mimetype of this node.
            """
            return self.__filesystem.mimetype(self.__filesystem.get_readhandle(self)) or "application/octet-stream"

        @property
        def mtime(self) -> datetime.datetime:
            """
            The 'last modified' time of this node.
            """
            return self.__filesystem.mtime(self.__filesystem.get_readhandle(self))

        @property
        def mtime_ts(self) -> float:
            """
            Same as :py:attr:`mtime`, but as Unix timestamp.
            """
            return self.mtime.timestamp()

        @property
        def icon_name(self) -> t.Optional[str]:
            """
            The recommended icon name for this node.
            """
            if self.has_thumbnail:
                return None
            if self.is_dir:
                return "dir"
            return "file"

        @property
        def has_thumbnail(self) -> bool:
            """
            Whether there could be a thumbnail available for this node.

            See also :py:meth:`thumbnail`.

            There might be cases when it returns `True` but the thumbnail generation will fail.
            """
            return self.__filesystem.has_thumbnail(self.__filesystem.get_readhandle(self))

        @property
        def has_preview(self) -> bool:
            """
            Whether there could be a html preview snippet available for this node.

            See also :py:attr:`preview_html`.

            There might be cases when it returns `True` but the preview generation will fail.
            """
            return self.__filesystem.has_preview(self.__filesystem.get_readhandle(self))

        @property
        def comment(self) -> str:
            """
            The node comment text.
            """
            return self.__filesystem.comment(self.__filesystem.get_readhandle(self))

        @property
        def rating(self) -> int:
            """
            The node rating.
            """
            return self.__filesystem.rating(self.__filesystem.get_readhandle(self))

        @property
        def tags(self) -> t.List[str]:
            """
            The tags assigned to this node.
            """
            return self.__filesystem.tags(self.__filesystem.get_readhandle(self))

        @property
        def tagstring(self) -> str:
            """
            The tags assigned to this node, encoded in one string.
            """
            return pimetadatainterpreter.TagAssignments.tags_to_tagstring(self.tags)

        @property
        def geo(self) -> str:
            """
            The geographic location associated to this node, encoded in a string.
            """
            geoobj = self.geo_obj
            return geoobj.to_geostring() if geoobj else ""

        @property
        def geo_obj(self) -> "lawwenda.fs.data.GeoLocation":
            """
            The geographic location associated to this node.
            """
            return self.__filesystem.geo(self.__filesystem.get_readhandle(self))

        @property
        def basics_as_dict(self):
            """
            Basic node data as dict.

            This is solely used internally for serialization.
            """
            return {k: getattr(self, k) for k in ["name", "dirpath", "is_dir", "is_file", "is_link", "size", "mtime_ts",
                                                  "icon_name"]}

        @property
        def full_as_dict(self):
            """
            Complete node data as dict.

            This is solely used internally for serialization.
            """
            return {**{k: getattr(self, k) for k in ["comment", "rating", "tags", "geo", "preview_html"]},
                    **self.basics_as_dict}

        @property
        def preview_html(self) -> str:
            """
            An html snippet that shows a preview of this node.

            This is larger and richer in terms of flexibility than thumbnails, and is typically used by the file details
            panel.

            See also :py:attr:`has_preview`.
            """
            return self.__filesystem.preview_html(self.__filesystem.get_readhandle(self))

        @property
        def child_nodes(self) -> t.List["Filesystem.Node"]:
            """
            The list of child nodes, i.e. nodes for all files and sub-directories inside this node.

            This only makes sense on directory nodes and will be empty otherwise.
            """
            if not self.is_dir:
                return []
            return self.__filesystem.child_nodes(self.__filesystem.get_readhandle(self))

        @property
        def parent_node(self) -> "Filesystem.Node":
            """
            The parent node.

            This is `None` for the root node.
            """
            return self.child_by_name("..")

        def traverse_dir(self, *, raise_on_circle: bool,
                         param_path: str = "") -> t.Iterable[t.Tuple["Filesystem.Node", str]]:
            """
            Return paths from this node and all descendants (i.e. the sub-tree).

            :param raise_on_circle: If to raise an exception when there is a circle (due to links), instead of silently
                                    skipping and continuing.
            :param param_path: Prefix for all output paths.
            """
            nodes = [(self, self.__filesystem.sanitize_abspath(param_path))]
            seen = set()
            while nodes:
                node, nparampath = nodes.pop()
                seenkey = node.path, node._filesystem  # pylint: disable=protected-access
                if seenkey in seen:
                    if raise_on_circle:
                        raise CircularTraversalError()
                    continue
                seen.add(seenkey)
                yield node, nparampath
                for cnode in node.child_nodes:
                    nodes.append((cnode, self.__filesystem.sanitize_abspath(f"{nparampath}/{cnode.name}")))

        def try_get_fullpath(self, *, writable: bool) -> t.Optional[str]:
            """
            Try to return an absolute path in the local filesystem for this node.

            You should usually not need this method, you should avoid to use it as good as you can, and when you use it,
            you must be very careful! This is due to the following reasons:

            - It allows you to get a path from a filesystem that is shared in a read-only way, but then accidentally
              make write accesses to it. Such a bug would obviously lead to a disastrous security hole. Avoid that by
              taking care of the `writable` argument!
            - Some :py:class`Filesystem`s might not support that at all and return `None`.
            - The method signature could change in later versions due to new access control features.

            :param writable: Whether you might do any write accesses to the result path. Never set to `False` without
                             understanding the security implications mentioned above.
            """
            handle = self.__filesystem.get_writehandle(self) if writable else self.__filesystem.get_readhandle(self)
            return self.__filesystem.try_get_fullpath(handle, writable=writable)

        def child_by_name(self, name: str) -> t.Optional["Filesystem.Node"]:
            """
            Return a child node by name.

            This will not fail for names that do not exist yet, but return a node that could be used for creating it.

            :param name: The file name of the child.
            """
            result = self.__filesystem.node_by_path(f"{self.path}/{name}")  # TODO raise on invalid name (e.g. with "/")
            return None if (result.path == self.path) else result

        def read_file(self) -> t.BinaryIO:
            """
            Return a file-like object for reading content of this node.

            The caller must ensure that it gets closed after usage, usually by means of the Python `with` keyword.
            """
            return self.__filesystem.read_file(self.__filesystem.get_readhandle(self))

        def thumbnail(self) -> bytes:
            """
            The thumbnail for this node in PNG format.

            See also :py:attr:`has_thumbnail`.
            """
            return self.__filesystem.thumbnail(self.__filesystem.get_readhandle(self))

        def delete(self) -> None:
            """
            Delete this node.
            """
            self.__filesystem.delete(self.__filesystem.get_writehandle(self))

        def mkdir(self) -> None:
            """
            Make this node an existing directory.
            """
            self.__filesystem.mkdir(self.__filesystem.get_writehandle(self))

        def copy_to(self, newpath: str) -> None:
            """
            Copy this node to a destination path.

            After copying, the destination has similar characteristics as this node, i.e. either is a file with the same
            content, or is a directory with the same subitems.

            :param newpath: The destination path.
            """
            self.__filesystem.copy_to(self.__filesystem.get_readhandle(self),
                                      self.__filesystem.get_writehandle(self.__filesystem.node_by_path(newpath)))

        def move_to(self, newpath: str) -> None:
            """
            Move this node to a destination path.

            After moving, the destination has similar characteristics as this node had, i.e. either is a file with the
            same content, or is a directory with the same subitems.

            :param newpath: The destination path.
            """
            self.__filesystem.move_to(self.__filesystem.get_writehandle(self),
                                      self.__filesystem.get_writehandle(self.__filesystem.node_by_path(newpath)))

        def set_comment(self, comment: str) -> None:
            """
            Set the comment for this node.

            :param comment: The new comment.
            """
            self.__filesystem.set_comment(self.__filesystem.get_writehandle(self), comment)

        def set_geo(self, geo: str) -> None:
            """
            Set the geographic location for this node.

            :param geo: The new geographic location (as encoded string).
            """
            self.__filesystem.set_geo(self.__filesystem.get_writehandle(self), geo)

        def set_rating(self, rating: int) -> None:
            """
            Set the rating for this node.

            :param rating: The new rating.
            """
            self.__filesystem.set_rating(self.__filesystem.get_writehandle(self), rating)

        def add_tag(self, tag: str) -> None:
            """
            Add a tag to this node.

            :param tag: The tag to add.
            """
            self.__filesystem.add_tag(self.__filesystem.get_writehandle(self), tag)

        def remove_tag(self, tag: str) -> None:
            """
            Remove a tag from this node.

            :param tag: The tag to remove.
            """
            self.__filesystem.remove_tag(self.__filesystem.get_writehandle(self), tag)

        def write_file(self, content: t.Union[bytes, t.BinaryIO]) -> None:
            """
            Write content to this node.

            This will overwrite its original content.

            :param content: The binary content to write to the node.
            """
            self.__filesystem.write_file(self.__filesystem.get_writehandle(self), content)


class CircularTraversalError(IOError):
    """
    Raised when traversing a tree that has a circle (i.e. that is not really a tree), usually by an 'unfortunate' link.
    """


str(""" # TODO xx
def link_target(self, node: FilesystemNode, *, recursive: bool) -> t.Optional[FilesystemNode]:
    if not node.is_link:        return node
    lnktgt = os.readlink(self._path_to_fullpath(node.path))
    rlnktgt = os.path.relpath(lnktgt if os.path.isabs(lnktgt) else f"{node.dirpath}/{lnktgt}", self.__rootpath)
    result = self.node(rlnktgt)
    if recursive:        result = self.link_target(result, recursive=True)
    return result
""")
# TODO xx umask 007 ?!
# TODO i18n
# TODO noh py&js: docstrings
# TODO occassionally crashes (at least with firefox dev tools open)
# TODO bytes instead of str for paths and filenames ?!
