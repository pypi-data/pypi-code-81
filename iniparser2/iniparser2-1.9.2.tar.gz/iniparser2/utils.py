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
	prop = re.split(r'\s*(\=)\s*',string)
	if len(prop) < 3: return
	del prop[1]
	key, val = prop[0], prop[1]
	_key = re.split(r'(^[#])|((.*)\s[#]$)',key)[0]
	val = ''.join(prop[1:])
	val = re.split(r'((.)^[#]$)|\s([#])',val)[0]
	if key == _key:
		return key, val

def parse_section(string):
	if check_comment(string): return
	sec = re.split(r'^\s*\[(.*)\]|[#;]$',string)
	if sec[0] != string:
		for i,s in enumerate(sec):
			if not s: del sec[i]
		_sec = re.split(r'((.*)\s[#])',sec[0])[0]
		if _sec: return _sec

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