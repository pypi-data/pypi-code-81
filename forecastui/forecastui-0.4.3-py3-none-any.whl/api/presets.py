from flask_restful import Resource
from flask import request, current_app, jsonify
import glob
import os
import math
from ..utility import Store

class PresetsApi(Resource):

    def get(self):
        paths = current_app.atlas.paths
        preset_path = paths.get("presets")
        req = request.args.get("preset_name", None)
        if req is None:
            files = glob.glob(os.path.join(preset_path, "*.*"))
            files = [os.path.split(file)[1] for file in files]
            return {
                "presets": files
            }
        else:
            path = os.path.join(preset_path, req)
            Store.preset = Preset(path)
            data = Store.preset.getDict()
            keys = data.keys()
            return {
                "configurations": list(keys),
                "configurations_dict": data
            }

    def post(self):
        json_data = request.get_json()
        get_from_file = json_data.get("get_from_file")
        configuration_name = json_data.get("configuration_name")
        configuration = json_data.get("configuration")

        if get_from_file:
            file = Store.preset.getDict()
            configuration = file.get(configuration_name)

        try:

            enable_transparency = list()
            damp_fact = configuration.get("tracking").get("environment").get("damping_factor")
            ke = configuration.get("tracking").get("environment").get("k_e_vect")
            je = configuration.get("tracking").get("environment").get("j_e_vect")
            ke_temp = list()
            je_temp = list()
            de = list()
            filenames = list()

            if ke and je:
                for k in ke:
                    for j in je:
                        ke_temp.append(k)
                        je_temp.append(j)
                        de.append(damp_fact * 2 * math.sqrt(j*k))
                        filenames.append("{},ke={},je={},tsettling=0.0end".format(configuration.get("config_name", "log_error"), k, j))
                        enable_transparency.append(0.0)

            enable_transparency.append(1.0)
            enable_transparency.append(2.0)

            configuration["tracking"]["environment"]["k_e_vect"] = ke_temp
            configuration["tracking"]["environment"]["j_e_vect"] = je_temp
            configuration["tracking"]["environment"]["d_e_vect"] = de
            configuration["transparency"]["enable_transparency"] = enable_transparency
            Store.filename = filenames

        except Exception as e:
            print(e)

        result, loops = Store.preset.pickPreset(configuration)
        return jsonify(result=result, loops=loops)



class Preset:

    def __init__(self, path=None):
        self.__file = {}
        self.__path = path
        self.__preset = {}

    def getDict(self):
        if self.__path is not None:
            self.__file = self.__load(self.__path)
        return self.__file

    def pickPreset(self, configuration):

        def walk(d):
            max = 1
            loops = 1
            for value in d.values():
                if isinstance(value, dict):
                    loops = walk(value)
                elif isinstance(value, list):
                    loops = len(value)
                if loops > max:
                    max = loops
            return max

        if isinstance(configuration, dict):
            self.__preset = configuration
            loops = walk(self.__preset)
        else:
            return (False, 0)

        # Let's make all keys lower case to ease the search
        self.__preset = dict((key.lower(), value) for key, value in self.__preset.items())
        print(self.__preset)
        return (True, loops)

    def __call__(self, name):
        name = self.__strip(name)
        return self.__search(name)

    def __load(self, path):
        _, file_extension = os.path.splitext(path)
        if file_extension in (".yaml", ".yml"):
            return self.__load_yaml(path)
        elif file_extension in (".json"):
            return self.__load_json(path)
        elif file_extension in (".xml"):
            return self.__load_xml(path)
        else:
            return {}

    def __load_yaml(self, path):
        import yaml
        with open(path, "r") as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        return data

    def __load_json(self, path):
        import json
        with open(path, "r") as file:
            data = json.load(file)
        return data

    def __load_xml(self, path):
        return {}

    def __validate(self, configuration_name):
        config = self.__file.get(configuration_name)
        return isinstance(config, dict)

    def __strip(self, parameter):
        return parameter.rstrip("\x00 ").lower()

    def __search(self, parameter):

        splitted = parameter.split()

        def walk(d, keys):

            try:
                current_key = keys.pop(0)
            except IndexError as e:
                return None

            value = d.get(current_key, None)
            if isinstance(value, dict):
                return walk(value, keys)
            return value

        val = walk(self.__preset, splitted)
        if val is not None:
            return val

        other = self.__preset.get("other", None)
        if other is not None:
            return other.get(parameter, None)
        return None
