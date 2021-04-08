import os
import threading
import requests
from ..utility import Store

"""
By design all callbacks must include a stop() method which
ensures that all threads can safely join and not halting the execution
"""

class PresetCallback:

	def __init__(self, preset):
		self._paramName = None
		self._value = None
		self._preset = preset
		self._lock = threading.Event()

	def __call__(self, paramName):
		self._value = None
		self._paramName = paramName
		if self._preset is not None:
			self._value = self._preset(paramName)
		if self._value is None:
			self._lock = threading.Event()
			requests.get("http://127.0.0.1:{}".format(Store.port) + '/api/board/send-data', params={"param": self._paramName})
			self._lock.wait()
		return self._value

	def unlock(self, value):

		if value is None:
			self._lock.set()
			return

		try:
			value = float(value)
			self._value = value
		except:
			pass

		if self._value is None:
			requests.get("http://127.0.0.1:{}".format(Store.port) + '/api/board/send-data', params={"param": self._paramName})
		elif self.__filter(self._paramName, value):
			requests.get("http://127.0.0.1:{}".format(Store.port) + '/api/board/send-data', params={"param": self._paramName, "message": "Incorrect value! Retry"})
			return
		else:
			self._lock.set()

	def stop(self):
		self.unlock(None)

	def __filter(self, name, value):
		try:
			if name.lower() == "loop frequency":
				if value <= 0:
					return True
			elif "duration" in name.lower():
				if value <= 0:
					return True 
		except:
			return True
		return False
