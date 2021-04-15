import re
import shlex
import inspect

__version__ = '1.2.0'

class BaseException(Exception):
	def __init__(self, message, *args):
		self.message = message
		self.args = args

	def __str__(self):
		return self.message

class ParsingError(Exception):
	pass

class ProcessError(Exception):
	pass

class MissingRequiredArgument(BaseException):
	pass

def _get_args_type_char(parsed_command, max_args=0):
	argtype = list()

	if max_args == 0:
		for arg in parsed_command['args'][0:parsed_command['args_count']]:
			if not arg: continue

			argtype.append(type(arg).__name__[0]) # get type char
	else:
		for arg in parsed_command['args'][0:max_args]:
			if not arg: continue

			argtype.append(type(arg).__name__[0]) # get type char

	return argtype

def _eval_cmd(parsed_command):
	"""evaluate literal arguments"""
	if type(parsed_command).__name__ != 'dict': return

	eval_code = [
		(r'^[-+]?(\d*[.])\d*$',float),
		(r'^[-+]?\d+$',int)
	]

	for i in range(len(parsed_command['args'])):
		
		if not parsed_command['args'][i]:
			break # empty args

		for ev in eval_code:
			res = re.match(ev[0],parsed_command['args'][i])

			if res:
				parsed_command['args'][i] = ev[1](parsed_command['args'][i])
				break # has found the correct data type

	return parsed_command

class Cmd:
	def __init__(self, command_string, prefix='/', max_args=0):
		self.parsed_command = None
		self.name = None
		self.args = []
		self.args_count = len(self.args)
		self.command_string = command_string
		self.prefix = prefix
		self.max_args = max_args

	def get_dict(self):
		"""return parsed command"""
		return self.parsed_command

	def parse(self, eval=False):
		"""parse string commands, returns command name and arguments"""
		res = re.findall(rf'^{self.prefix}(.*)',self.command_string)
		argres = shlex.split(''.join(res))
		argsc = len(argres[1:])

		if self.max_args == 0:
			self.max_args = argsc

		if argsc > self.max_args:
			raise ParsingError(f"arguments exceeds max arguments: ({self.max_args})")

		for i in range(len(argres), self.max_args): # insert empty arguments
			argres.insert(i,'')

		if argres:
			cmd = {'name': argres[0], 'args': argres[1:], 'args_count': argsc}

			if eval: self.parsed_command = _eval_cmd(cmd) # only returns if command is valid
			else:
				self.parsed_command = cmd

			self.name = self.parsed_command['name']
			self.args = self.parsed_command['args']
			self.args_count = self.parsed_command['args_count']

	def __str__(self):
		return f"<Raw: \"{self.command_string}\", Name: \"{self.name}\", Args: {self.args[0:self.args_count]}>"

def MatchArgs(parsed_command_object, format, max_args = 0):
	"""match argument formats, only works with eval"""

	# format example: 'ssf', arguments: ['hell','o',10.0] matched

	parsed_command = getattr(parsed_command_object, 'parsed_command', None)
	if max_args == 0:
		max_args = getattr(parsed_command_object, 'max_args', 0)

	if parsed_command == None:
		raise TypeError("Command object appear to be not parsed")
	
	if max_args < 0:
		max_args = 0

	if not format:
		raise ValueError("no format specified")

	format = format.replace(' ','')
	format = list(format)

	argtype = _get_args_type_char(parsed_command, max_args)

	if len(format) != len(argtype):
		raise ValueError("format length is not the same as the arguments length")

	matched = 0
	for i,t in enumerate(argtype):
		if t == 'i' or t == 'f':
			if format[i] == 's':
				matched += 1 # allow int or float as 's' format
			elif format[i] == 'c' and len(str(parsed_command['args'][i])) == 1 and t == 'i':
				matched += 1 # and char if only a digit for int
			elif t == format[i]:
				matched += 1
		elif t == 's':
			if format[i] == 'c' and len(str(parsed_command['args'][i])) == 1:
				matched += 1
			elif t == format[i]:
				matched += 1

	if matched == len(format):
		return True

	return False

def ProcessCmd(parsed_command_object, callback, error_handler_callback=None, attr={}):
	"""process command, to tell which function for processing the command, i guess..."""
	
	parsed_command = getattr(parsed_command_object, 'parsed_command', None)

	if parsed_command == None:
		raise TypeError("Command object appear to be not parsed")

	if type(parsed_command).__name__ != 'dict': raise TypeError("parsed_command must be a dict of parsed command")
	if type(callback).__name__ != 'function': raise TypeError("callback is not a function")
	if error_handler_callback and type(error_handler_callback).__name__ != 'function': raise TypeError("error handler callback is not a function")

	if not isinstance(attr, dict): raise TypeError("attributes must be in dict object")

	ret = None
	try:
		callback_argspec = inspect.getfullargspec(callback)
		callback_params = callback_argspec.args
		callback_defaults = callback_argspec.defaults

		if callback_defaults != None:
			if len(callback_defaults) == len(callback_params):
				for cdef in callback_defaults[parsed_command['args_count']:]:
					parsed_command['args_count'] += 1
					parsed_command['args'].insert(parsed_command['args_count'],cdef)
			else:
				for cdef in callback_defaults[parsed_command['args_count']-1:]:
					parsed_command['args_count'] += 1
					parsed_command['args'].insert(parsed_command['args_count'],cdef)

		for a in attr:
			setattr(callback, a, attr[a])
		
		if len(callback_params) > parsed_command['args_count']:
			if callback_defaults != None:
				exc = MissingRequiredArgument(f'missing required argument : {callback_params[parsed_command["args_count"]-1]}',
						callback_params[parsed_command["args_count"]-1]
					)
			else:
				exc = MissingRequiredArgument(f'missing required argument : {callback_params[parsed_command["args_count"]]}',
						callback_params[parsed_command["args_count"]]
					)
			setattr(exc, 'param', callback_params[parsed_command['args_count']])
			raise exc
		
		if callback_argspec.varargs == None:
			ret = callback(*parsed_command['args'][0:len(callback_params)])
		else:
			ret = callback(*parsed_command['args'][0:parsed_command['args_count']])

		for a in attr:
			delattr(callback, a)

	except Exception as exception:
		if error_handler_callback == None:
			raise ProcessError(f"an error occurred during processing callback '{callback.__name__}()' for command '{parsed_command['name']}', no error handler callback specified, exception: ", exception)
		else:
			error_handler_callback(error=exception)

	return ret