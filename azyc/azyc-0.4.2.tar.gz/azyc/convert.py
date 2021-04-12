import base64
import distutils.util
import logging
import os
import json
from typing import Union

import yaml

import argparse


def merge(source: dict, target: dict):
    for key, value in source.items():
        if isinstance(value, dict):
            node = target.setdefault(key, {})
            merge(value, node)
        else:
            target[key] = value
    return target


def convert_dict(config: dict, base_path: str):
    params = dict()
    for key, value in config.items():
        if type(value) is dict:
            if "array" in value:
                params[key] = {"value": list(value["array"])}
            elif "object" in value:
                params[key] = {"value": dict(value["object"])}
            elif "file" in value:
                with open(base_path + '/' + value['file'], "r", encoding="utf-8") as f:
                    data = str(f.read())
                params[key] = {"value": data}
            elif "binary" in value:
                with open(base_path + '/' + value['binary'], "rb") as f:
                    data = f.read()
                data = base64.b64encode(data)
                params[key] = {"value": data.decode('utf-8')}
            elif "keyVault" in value:
                if not "secretName" in value:
                    raise Warning("'secretName' is required when using a keyVault for deployment")
                reference = {
                    "keyVault": {"id": str(value['keyVault'])},
                    "secretName": str(value["secretName"])
                }

                if "secretVersion" in value:
                    reference["secretVersion"] = str(value["secretVersion"])
                params[key] = {"reference": reference}
            elif "yaml" in value:
                with open(base_path + '/' + value['yaml'], "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                values_to_overwrite = value.get("overwrite")
                if values_to_overwrite is not None:
                    data = merge(values_to_overwrite, data)
                params[key] = {"value": yaml.safe_dump(data)}
            else:
                logging.warning(
                    f"Could not parse section: '{key}'. None of the keys where recognized as arguments: " + str(
                        list(value.keys())))
        else:
            params[key] = {"value": value}
    return params


def write_params(output_file: str, params: dict):
    paramsFile = {
        "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
        "contentVersion": "1.0.0.0",
        "parameters": params
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(paramsFile, f, indent=2)
    print(f"parameter file written to {output_file}")


def convert(input_file: str, output_file: str, extra_params: Union[dict, None] = None):
    if extra_params is None:
        extra_params = dict()

    with open(input_file, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    base_path = os.path.abspath(os.path.dirname(input_file))
    params = convert_dict(config, base_path)

    for key, value in extra_params.items():
        try:
            params[key] = {"value": int(value)}
        except ValueError:
            try:
                params[key] = {"value": bool(distutils.util.strtobool(value))}
            except ValueError:
                params[key] = {"value": value}

    write_params(output_file, params)
