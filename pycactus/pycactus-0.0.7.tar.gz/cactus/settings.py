"""
Module to look for, and parse, Function and settings.
"""
import os
import json
from . import logger


def is_function(folder: str) -> bool:
	return os.path.isfile("{}/function.json".format(folder))


def get_functions(path: str) -> list:
	functions = []
	for file in os.listdir(path):
		candidate = "{}/{}".format(path, file)
		if os.path.isdir(candidate):
			if is_function(candidate):
				functions.append((candidate, file))
	return functions


def load_json_file(path: str) -> dict:
	with open(path, "r") as file:
		return json.load(file)


def load_function_settings(path: str) -> dict:
	return load_json_file("{}/function.json".format(path))


def load_project_settings(path: str) -> dict:
	return load_json_file("{}/host.json".format(path))


def load_project(path: str) -> dict:
	try:
		project_settings = load_project_settings(path)
	except json.decoder.JSONDecodeError:
		logger.error("Unable to parse host.json: invalid JSON.")
		project_settings = {}
	except FileNotFoundError:
		logger.error("Unable to parse host.json: file not found.")
		project_settings = {}

	functions_settings = []
	functions = get_functions(path)
	for function in functions:
		try:
			functions_settings.append((function[1], load_function_settings(function[0])))
		except json.decoder.JSONDecodeError:
			logger.error("[{}] Unable to parse Function settings: invalid JSON.".format(function[1]))
	return {"project": project_settings, "functions": functions_settings}
