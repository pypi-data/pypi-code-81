from flask_restful import Resource
from flask import request, current_app, jsonify


class PathsApi(Resource):

    def get(self):
        return current_app.atlas.paths

    def post(self):
        json_data = request.get_json()
        name = json_data.get("folder_name")
        path = json_data.get("folder_path")
        current_app.atlas.paths[name] = path
        return current_app.atlas.paths

class OpenApi(Resource):

    def detect_os(self):
        import platform
        return platform.system()

    def post(self):
        json_data = request.get_json()
        is_path = json_data.get("is_path")
        path = json_data.get("path")

        if not is_path:
            path = current_app.atlas.paths[path]
        
        if not path:
            return {}
        
        platform = self.detect_os()

        if platform == "Linux":
            import subprocess
            subprocess.Popen(["xdg-open", path])
        
        elif platform == "Windows":
            import os
            os.startfile(path)
        
        elif platform == "Darwin":
            import subprocess
            subprocess.Popen(["open", path])
        
        return {}
