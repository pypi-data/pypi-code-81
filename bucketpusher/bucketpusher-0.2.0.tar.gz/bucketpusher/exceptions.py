import re
import google.api_core.exceptions as gae

e_msg_regex = re.compile(r'message":\s?"(.*?)"', re.IGNORECASE)


def is_delete_permission_error(e, filename=None):
    if not isinstance(e, gae.Forbidden):
        return False
    try:
        msg = e_msg_regex.search(str(e)).group(1)
        if "storage.objects.delete" in msg:
            return True
    except Exception:
        return False


class UploadError(Exception):
    def __init__(self, filename, message=""):
        self.err = f"Failed to upload {filename}: {message}"
        super().__init__(self.err)


class UploadOverwriteError(UploadError):
    def __init__(self, filename, message="File already exists on remote"):
        super().__init__(filename, message=message)


class UploadCancelled(UploadError):
    def __init__(self, filename, message="Upload cancelled"):
        super().__init__(filename, message=message)
