from requests.utils import unquote
from .base import BaseResource
from ..web import app_auth


class FileToken(BaseResource):
    @app_auth.login_required
    def post(self, path: str):
        path = unquote(path)
        token = self.config.FILE_TOKENS.add_file_token(path)
        self.config.FILE_TOKENS.save_json()
        return {
            "status": True,
            "token": token
        }

    @app_auth.login_required
    def delete(self, path: str):
        path = unquote(path)
        self.config.FILE_TOKENS.remove_file_token(path)
        self.config.FILE_TOKENS.save_json()
        return {
            "status": True
        }
