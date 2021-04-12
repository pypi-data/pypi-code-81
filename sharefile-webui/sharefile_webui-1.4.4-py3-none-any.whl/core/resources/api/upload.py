import os
from flask_restful import request
from .base import BaseResource
from ..web import app_auth


class Upload(BaseResource):
    RESOURCE_URL = "/api/upload/<path:path>"

    @app_auth.login_required
    def post(self, path: str):
        path = self._unquote_path(path)
        return self.post_chunk_upload(path)

    def post_chunk_upload(self, path: str):
        file = request.files['file']
        file_path = os.path.join(self.root_path, path, file.filename)
        with open(file_path, 'ab') as f:
            f.seek(int(request.form['dzchunkbyteoffset']))
            chunk = file.stream.read()
            f.write(chunk)
        return {
            "status": True,
            "chunkSize": len(chunk),
            "remoteFileSize": os.path.getsize(file_path),
            "filename": file.filename,
        }

    def post_multiupload(self, path: str):
        uploaded = []
        files = request.files
        for file_item in files.items():
            _, file_storage = file_item
            filename = file_storage.filename
            file_path = os.path.join(self.config.SHARE_DIRECTORY, path, filename)
            file_storage.save(file_path)
            uploaded.append(filename)
        return {
            "status": True,
            "filename": uploaded,
        }


class UploadRoot(Upload):
    RESOURCE_URL = "/api/upload/"

    @app_auth.login_required
    def post(self):
        return super().post("")
