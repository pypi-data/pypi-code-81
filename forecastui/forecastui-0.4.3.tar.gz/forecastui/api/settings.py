from flask_restful import Resource
from flask import request, current_app

class Settings(Resource):

    def get(self):
        return current_app.atlas.settings.getAll()

    def post(self):
        json_data = request.get_json()
        section = json_data.get("section", "General")
        option = json_data.get("option")
        value = json_data.get("value")
        current_app.atlas.settings.set(section, option, value)
        return current_app.atlas.settings.getAll()