from flask_restful import Resource
from flask import request, current_app, jsonify
import os
from ..utility import Store


class Ports(Resource):
    def get(self):
        from serial.tools.list_ports import comports
        return [port.device for port in comports()]

class Connection(Resource):

    def post(self):
        json = request.get_json()
        Store.device = json.get("device")
        Store.baudrate = json.get("baudrate")
        Store.filename = json.get("filename")
        return jsonify(result=True)

class StopConnection(Resource):

    def post(self):
        serial, message = current_app.atlas.stop_serial()
        response = {
            "success": serial,
            "message": message,
            "last_run": current_app.atlas.history
        }
        return response

class StartConnection(Resource):

    def post(self):
        device = Store.device
        baudrate = Store.baudrate
        serial, message = current_app.atlas.start_serial(device, baudrate)
        response = {
            "success": serial,
            "message": message
        }
        return response

class StartExperiment(Resource):

    def post(self):
        json = request.get_json()
        index = json.get("index", 0)
        success = current_app.atlas.start_experiment(index)
        return jsonify(result=success)

class StopExperiment(Resource):

    def post(self):
        success = current_app.atlas.stop_experiment()
        return jsonify(result=success)
