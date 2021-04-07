# uhh... ¯\_(ツ)_/¯

class ParsingError(Exception):
	pass

class INI:
	def __init__(self, filename):
		self.filename = str(filename)

	def __enter__(self):
		return INI(self.filename)

	def __exit__(*args,**kwargs): #hmm...
		pass

	def read(self):
		"""read sections and properties"""
		return parse(open(self.filename,'r').read())

	def write(self,sets):
		"""write properties and sections to file"""
		from .utils import dump
		if not isinstance(sets,dict): raise TypeError("INI properties must be a dict object")
		dump(self.filename,sets); return True

class INI_BIN:
	def __init__(self, filename):
		self.filename = str(filename)

	def __enter__(self):
		return INI_BIN(self.filename)

	def __exit__(*args,**kwargs): #hmm...
		pass

	def read(self):
		"""read sections and properties in binary format"""
		import marshal, io
		data = marshal.load(open(self.filename,'rb')).decode('utf-8')
		_data = io.StringIO(data).readlines()
		if _data[0].strip() != "INI": return TypeError("Binary file is not an INI format")
		return parse(data)

	def write(self,sets):
		"""write properties and sections to file in binary format"""
		from .utils import dump_bin; import marshal
		if not isinstance(sets,dict): raise TypeError("INI properties must be a dict object")
		dump_bin(self.filename,sets)
		raw_data = open(self.filename,'r').read().encode('utf-8')
		marshal.dump(raw_data,open(self.filename,'wb'))

def parse(string):
	"""beans for everyone, haha... :|"""
	from .utils import parse_section,parse_property,is_section,is_property,check_comment
	import io
	
	ret = dict()
	lines,point,anchor,fsec=io.StringIO(string).readlines(),0,0,False

	for idx, line, in enumerate(lines):
		if line.strip() == 'INI': continue # skip INI file format for binary, i guess...

		if is_section(line.strip()) or fsec:
			fsec=True
			_section = parse_section(line.strip())
			point,anchor=idx+1,idx+1

			for i in range(anchor,len(lines)):
				anchor += 1
				if is_section(lines[i].strip()):
					break
			
			if _section: ret.update({_section: {}})
			
			for i in range(point,anchor):
				if is_property(lines[i].strip()):
					key, val = parse_property(lines[i].strip())

					if not key:
						raise ParsingError("invalid property key name at line {lineno}".format(lineno=i+1))

					if _section != None: ret[_section].update({key:val})
				else:
					if not check_comment(lines[i].strip()): raise ParsingError("error parsing property at line {lineno}".format(lineno=i+1))

		if not fsec:
			if is_property(line.strip()):
				key, val = parse_property(line.strip())

				if not key:
					raise ParsingError("invalid property key name at line {lineno}".format(lineno=idx+1))

				ret.update({key: val})
			else:
				if not check_comment(line.strip()): raise ParsingError("error parsing property at line {lineno}".format(lineno=idx+1))
	
	return ret