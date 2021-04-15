import re

def exists(filename):
	"""check whether the file is exists or not"""
	import os
	if os.path.exists(filename): return True
	else: return False

def create(filename):
	"""creates new file"""
	import os
	if not os.path.exists(filename):
		with open(filename,'x') as f:
			pass
		return True
	else: return False

def flush(filename,stream=False):
	"""flush file"""
	if not stream:
		import os
		if os.path.exists(filename):
			os.remove(filename)
			with open(filename,'x') as f:
				pass
			return True
		else: return False
	elif stream:
		with open(filename,'w') as f:
			f.write('')
		return True

def remove(filename):
	"""remove/deletes file"""
	import os
	if os.path.exists(filename):
		os.remove(filename)
		return True
	else: return False

def dump(filename,set):
	"""dump a dictionary or a set to INI file format"""
	with open(filename,'w+') as f:
		for ns in set:
			if isinstance(set[ns], dict):
				f.write(f'[{ns}]\n')
				for ps in set[ns]:
					if isinstance(set[ns][ps], dict) or isinstance(set[ns][ps], list): continue
					f.write(f'{ps}={set[ns][ps]}\n')
			else:
				f.write(f"{ns}={set[ns]}\n")

def dump_bin(filename,set):
	"""dump a dictionary or a set to INI file format"""
	with open(filename,'w+') as f:
		f.write('INI\n') # ini format binary
		for ns in set:
			if isinstance(set[ns], dict):
				f.write(f'[{ns}]\n')
				for ps in set[ns]:
					if isinstance(set[ns][ps], dict) or isinstance(set[ns][ps], list): continue
					f.write(f'{ps}={set[ns][ps]}\n')
			else:
				f.write(f"{ns}={set[ns]}\n")

def parse_property(string):
	if check_comment(string): return
	prop = re.findall(r'^\s*(.+?)\s*\=\s*(.+?)\s*$',string)
	if not prop: return
	if len(prop[0]) < 2: return
	key, val = prop[0][0], prop[0][1]
	_key = re.match(r'^\s*(\#)|((.*)\s[#])',key)
	if _key: return
	val = re.split(r'((.)^[#]$)|\s([#])',val)[0]

	return key, val

def parse_section(string):
	if check_comment(string): return
	sec = re.findall(r'^\s*\[(.*)\]\s*?(.*)$',string)
	if not sec: return
	if sec[0][1] and not re.match(r'^[#;]',sec[0][1]): return
	_sec = re.match(r'(.*)\s[#]',sec[0][0])
	if not _sec: return sec[0][0]

def check_comment(string):
	sec = re.match(r'^[#;]',string)
	if sec: return True
	return False

def is_property(string):
	if parse_property(string) != None: return True
	return False

def is_section(string):
	if parse_section(string) != None: return True
	return False

def is_ini(filename):
	return filename.endswith('.ini')