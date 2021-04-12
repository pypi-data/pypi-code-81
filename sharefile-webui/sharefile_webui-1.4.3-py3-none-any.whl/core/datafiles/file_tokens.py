import hashlib
from datetime import datetime
from .base import BaseDatafile


class FileTokens(BaseDatafile):
    def check_token(self, filepath: str, token: str):
        if filepath in self.data:
            return self.data.get(filepath) == token
        return False

    def add_file_token(self, filepath: str) -> str:
        datetime_str = str(datetime.now())
        token_prepare = f"{filepath}||{datetime_str}"
        hash_object = hashlib.sha1(bytes(token_prepare, "utf-8"))
        hash_str = hash_object.hexdigest()
        self.data[filepath] = hash_str
        return hash_str

    def remove_file_token(self, filepath: str) -> bool:
        if filepath in self.data:
            del self.data[filepath]
            return True
        return False

    def remove_file_tokes_beginig(self, filepath_beging: str) -> bool:
        items_to_delete = []
        for path, token in self.data.items():
            if path.startswith(filepath_beging):
                items_to_delete.append(path)
        for path in items_to_delete:
            del(self.data[path])
        return len(items_to_delete) > 0
