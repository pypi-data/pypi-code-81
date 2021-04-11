import os
from .base import BaseResource
from ..web import app_auth


class FileContent(BaseResource):
    RESOURCE_URL = "/api/filecontent/<path:path>"
    ALLOWED_EXTENSIONS = ["txt", "md", "log"]
    MAX_FILE_SIZE = 10 * 1024

    def __init__(self):
        super().__init__()
        self._add_argument("content", str, "File content to store", location_="form")

    @app_auth.login_required
    def get(self, path):
        path = self._unquote_path(path)
        full_path = os.path.join(self.root_path, path)
        if not self.check_file_ext(full_path):
            self._abort_error("Unsupported file extension to get file content")
        if filesize := os.path.getsize(full_path) > self.MAX_FILE_SIZE:
            self._abort_error(f"File size reached max size {filesize} > {self.MAX_FILE_SIZE} Bytes")
        with open(full_path, "r") as f:
            content = f.read()
        return {
            "status": True,
            "content": content,
            "name": os.path.basename(path),
            "path": path,
            "fullpath": full_path
        }

    @app_auth.login_required
    def post(self, path):
        path = self._unquote_path(path)
        full_path = os.path.join(self.root_path, path)
        file_tail: str = ""
        tail_counter: int = 1
        while os.path.exists(full_path_tail := f"{full_path}{file_tail}.txt"):
            file_tail = f" {tail_counter}"
            tail_counter += 1
        os.mknod(full_path_tail)
        return {
            "status": True,
            "fullpath": full_path_tail
        }

    @app_auth.login_required
    def put(self, path):
        path = self._unquote_path(path)
        full_path = os.path.join(self.root_path, path)
        if not self.check_file_ext(full_path):
            self._abort_error("Unsupported file extension to get file content")

        content = self.args.get("content")
        if content is not None:
            with open(full_path, "w") as f:
                f.write(content)
            return {
                "status": True,
                "file": full_path,
            }
        self._abort_error(f"Content of request for file '{path}' is empty.")

    @classmethod
    def check_file_ext(cls ,path: str) -> bool:
        file_extension = os.path.splitext(path)[-1].lower().replace(".", "")
        return file_extension in cls.ALLOWED_EXTENSIONS
