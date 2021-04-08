import requests
import threading
import time
from ..utility import Store

class StatusCallback:
	"""
	Debugger class which updates the server on the serial status:
		- handshakes
		- messages
		- current action
	"""
	def __init__(self):
		self._reset()
		self._running = True
		self._thread = threading.Thread(target=self._thread_loop, args=(), daemon=True)
		self._thread.start()

	def update(self, **kwargs):
		for key,value in kwargs.items():
			self.__packet[key] = value

	@property
	def timeout(self):
		return self.__timeout
	@timeout.setter
	def timeout(self, value):
		try:
			self.__timeout = float(value)
		except ValueError:
			print('''ERROR: While setting status callback timeout value,
				couldn't cast {} to float'''.format(value))

	@property
	def logssec(self):
		return self.__packet.get("logss", 0)

	@logssec.setter
	def logssec(self, value):
		self.__packet["logss"] = value

	def _thread_loop(self):
		while self._running:
			self._send_data()

	def _send_data(self):
		requests.get("http://127.0.0.1:{}".format(Store.port) + '/api/board/status', params=self.__packet)
		self.logssec = 0
		time.sleep(self.__timeout)

	def _reset(self):
		self.__packet = {
			"ack": False,
			"synack": False,
			"handshake": False,
			"message": None,
			"action": -1,
			"logss": 0
		}
		self.__timeout = 0.25

	def stop(self):
		self._running = False
		self._thread.join()
		self._reset()
		self._send_data()