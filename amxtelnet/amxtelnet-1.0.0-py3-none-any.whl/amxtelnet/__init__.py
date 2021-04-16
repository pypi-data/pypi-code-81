import asyncio
from logging import debug, info, warning, error
import asyncio
import re


class AMXTelnet:
	def __init__(self) -> None:
		self.scanned_systems = []


	def set_systems(self, systems):
		self.systems = systems
		info(f"added {len(self.systems)} systems")


	def config(self, user_name, password, alt_username='administrator', alt_password='password', write_results=True, path='systems/hard coded/'):
		self.user_name = user_name
		self.password = password
		self.alt_username = alt_username
		self.alt_password = alt_password
		self.write_results = write_results
		self.path = path
		return


	def set_requests(self, *requests):
		self.requests = [request for request in requests]
		info(f"requests = {requests}")
		return


	def _write_to_file(self, master, telnet_text):
		from os import mkdir, path
		# write each telnet rx to individual .txt file
		if not path.exists(self.path):
			mkdir(self.path)
			info(f'amxtelnet.py created {self.path}')

		header = f"full_name={master['full_name']}\nmaster_ip={master['master_ip']}\nfailed_attemps={master['master_failed_attempts']}\nlogin_failure={master['master_login_failure']}\n"

		file_path = f"{self.path}{master['full_name']} telnet.txt"
		with open(file_path, 'w+') as f:
			info(f'amxtelnet.py created {file_path}')
			f.write(header + telnet_text)


	async def _telnet_master_login(self, tn, master):
		if not self.user_name: error('user_name was not provided')
		if not self.password: error('password was not provided')
		master['master_user'] = self.user_name
		master['master_password'] = self.password
		# create ['master_failed_attempts'] if it doesn't exist
		try:
			master['master_failed_attempts']
		except KeyError:
			master['master_failed_attempts'] = 0

		# attempt to login
		tn.write(f"{self.user_name}\r\n".encode())
		tn.read_until(b'\r\nPassword : ')
		tn.write(f"{self.password}\r\n".encode())
		login_result = tn.read_until(b'Welcome to ', timeout=2)

		# login successful, throw back to _telnet_scan_master() to send commands
		if 'Welcome to' in login_result.decode():
			master['master_login_failure'] = None
			info(f"{master['full_name']} login success")
			return master

		# login failed, throw back to _telnet_scan_master() to try the default login
		elif 'Invalid' in login_result.decode():
			master['master_failed_credentials'] = f"{master['master_user']} {master['master_password']}"
			master['master_login_failure'] = 'invalid login'
			master['master_failed_attempts'] += 1
			return master


	async def _telnet_scan_master(self, master):
		from amxtelnetlib import Telnet

		info(f"connecting to {master['full_name']}")

		# avoid key errors later on
		master['master_telnet_failure'] = None
		master['master_login_failure'] = None

		try:
			with Telnet(master['master_ip'], timeout=10) as tn:
				telnet_text = ""

				# keep attempting login until success, unknown login, or timeout
				tn.read_until(b'\r\nLogin : ')
				master = await self._telnet_master_login(tn, master)

				# check login results
				while True:
					# success
					if master['master_login_failure'] is None:
						tn = await self._poll_master(tn)
						if 'NX' in master['master_model']:
							# close on echo of last command sent
							telnet_text = tn.read_until(
								f'{self.requests[-1]}\r\n'.encode()).decode()
							tn.close()
						else:
							tn.write(b"exit\r\n")
							telnet_text = tn.read_all().decode('ascii')
						break

					# failure, try amx default
					elif master['master_user'] != self.alt_username:
						self.user_name = self.alt_username
						self.password = self.alt_password
						warning(f" trying {self.user_name} {master['full_name']}")
						master = await self._telnet_master_login(tn, master)
						# default login attempted, loop through again to see if it worked
						continue

					# default didn't work either, move on to the next system
					else:
						error(f"""Unable to login to {master['full_name']} {master['master_ip']}
								after {master['master_failed_attempts']} failed attempts""")
						tn.close()
						break
				
				if self.write_results: self._write_to_file(master, telnet_text)

		# NX masters throw this error when using 'exit'
		# instead of .close(), but NI needs 'exit'
		except ConnectionResetError:
			warning(f'amxtelnet.py: _telnet_scan_master() NX false connection error')

		except Exception as e:
			if master is not None:
				warning(f"{master['full_name']} {master['master_ip']} {e}")
			else: error(f"amxtelnet.py: _telnet_scan_master() no master: {master} {e}")

		self.scanned_systems.append(master)
		return


	async def _poll_master(self, tn):
		for request in self.requests:
			tn.write(f"{request}\r\n".encode())
			await asyncio.sleep(0)
		return tn


	async def _gather_connections(self, systems, simultaneous=65535):
		tasks = []
		skip_remainder = True
		master_count = len(systems)
		if master_count <= simultaneous: simultaneous = master_count
		else: skip_remainder = False
		master_chunks = int(master_count / simultaneous)
		master_remainder = master_count % simultaneous

		for i in range(master_chunks):
			tasks = []
			scan_start = (i * simultaneous)
			scan_end = (scan_start + simultaneous)
			for x in range(scan_start, scan_start + simultaneous):
				tasks.append(self._telnet_scan_master(systems[x]))
			await asyncio.gather(*tasks)

		# remainder
		if not skip_remainder:
			tasks = []
			scan_start = master_chunks * simultaneous
			scan_end = master_chunks * simultaneous + master_remainder
			for i in range(scan_start, scan_end):
				tasks.append(self._telnet_scan_master(systems[i]))
			await asyncio.gather(*tasks)
		return


	async def run(self):
		import time
		# scan time begins to increase when simultaneous is set to 50 or lower
		start = time.perf_counter()
		await(self._gather_connections(self.systems))
		elapsed = time.perf_counter() - start
		info(f"amxtelnet.py AMXTelnet() complete in {elapsed:0.2f} seconds")
		# 'RoomName telnet.txt' was created for every room
		return


class ParseAMXResponse:
	def __init__(self, input_path):
		if input_path:
			self.input_path = input_path
		else: self.input_path = 'telnet responses/'


	async def _parse_master_telnet(self, data_in, telnet_master):
		full_text = data_in.split('\n')

		master_line = '00000  ('
		device_line = '05001 '
		massio_line = '08001 '
		tp_line = '10001 '
		version_match = r' v(\d.\S+)'
		serial_match = r"Serial='?(\w+)"

		telnet_master['tp_generation'] = 'None'
		telnet_master['tp_model'] = 'None'
		telnet_master['tp_firmware'] = 'None'
		telnet_master['tp_serial'] = 'None'
		telnet_master['tp_ip'] = 'None'

		for i, line in enumerate(full_text):
			if master_line in line:
				telnet_master['master_firmware'] = re.search(
					version_match, line).group(1)
				telnet_master['master_serial'] = re.search(
					serial_match, full_text[i+1]).group(1)

			elif device_line in line:
				model_match = r'\)N([\w.-]+)'
				telnet_master['master_model'] = f"N{re.search(model_match, line).group(1)}"
				telnet_master['device_firmware'] = re.search(
					version_match, line).group(1)

			elif (massio_line in line) or (tp_line in line):
				tp_match = r'((08001|10001)  \(\d+\))([\w-]+)'
				tp_match_obj = re.search(tp_match, data_in)
				if tp_match_obj: telnet_master['tp_model'] = tp_match_obj.group(3)

				try:
					telnet_master['tp_firmware'] = re.search(
						version_match, line).group(1)
					telnet_master['tp_serial'] = re.search(
						serial_match, full_text[i+1]).group(1)
					tp_ip_match = r'Physical Address=IP (\d.+)'
					telnet_master['tp_ip'] = re.search(
						tp_ip_match, full_text[i+2]).group(1)
				except Exception as e:
					error(f"amxtelnet.py _parse_master_telnet({telnet_master['full_name']}) tp_firmware {e}")
					pass

		re_list = [
			r'(?<=#)(?P<system_number>\d+)',
			# r'(?<=\)N)(?P<master_model>[\w.-]+)',
			r'(?<=HostName    )(?P<master_hostname>[\w.-_]+)',
			r'(?<=IP Address  )(?P<master_ip>[\d.]+)',
			r'(?<=Subnet Mask )(?P<master_subnet>[\d.]+)',
			r'(?<=Gateway IP  )(?P<master_gateway>[\d.]+)',
			r'(?<=IPv4 Address  )(?P<master_ip>[\d.]+)',
			r'(?<=IPv4 Subnet Mask )(?P<master_subnet>[\d.]+)',
			r'(?<=IPv4 Gateway IP  )(?P<master_gateway>[\d.]+)',
			r'(?<=MAC Address )(?P<master_mac>[\w:]+)',
			r'(?<=1  Name is )(?P<program_name>[\w, .]+)',
			r'(?<=Rev )(?P<program_version>[\w, .]+)',
		]

		for item in re_list:
			telnet_master = await self._re_search(item, data_in, telnet_master)

		# Not reading logs, just seeing if they exist
		telnet_master['error_log'] = '.log' in data_in.lower()  # true/false
		telnet_master['camera_log'] = 'camera_log.txt' in data_in.lower()  # true/false

		return telnet_master


	async def _re_search(self, _re, data_in, telnet_master):
		if re.search(_re, data_in) is not None:
			telnet_master = {**telnet_master, **re.search(_re, data_in).groupdict()}
		return telnet_master


	async def run(self) -> list:
		from os import scandir
		telnet_info = []

		with scandir(self.input_path) as file_list:
			for file in file_list:
				telnet_master = {}
				telnet_master['full_name'] = file.name.split(' ')[0]
				with open(file, 'r') as f:
					file_text = f.read()
					telnet_master = await self._parse_master_telnet(file_text, telnet_master)
				telnet_info.append(telnet_master)
		return telnet_info
