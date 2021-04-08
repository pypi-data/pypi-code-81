from flask_socketio import emit
from flask_restful import Resource, inputs
from flask import request

class BoardStatus(Resource):
    def get(self):
        emit("board-status", {
            "ack": inputs.boolean(request.args.get("ack")),
            "synack": inputs.boolean(request.args.get("synack")),
            "handshake": inputs.boolean(request.args.get("handshake")),
            "message": request.args.get("message"),
            "action": request.args.get("action"),
            "logss": request.args.get("logss")
            }, broadcast=True, namespace="/")
        return {}


class BoardSendData(Resource):
    def get(self):
        name = request.args.get("param")
        message = request.args.get("message", "")
        emit("data-request", {"name": name, "message": message}, broadcast=True, namespace="/")
        return {}

class BoardParameter(Resource):
    def get(self):
        name = request.args.get("name")
        value = request.args.get("value")
        emit("parameter", {"name": name, "value": value}, broadcast=True, namespace="/")