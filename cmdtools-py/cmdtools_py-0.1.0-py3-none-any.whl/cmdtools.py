import re
import shlex

__version__ = '0.1.0'

def ParseCmd(command_string, prefix='/', max_args=64,eval=False):
	"""parse string commands, returns command name and arguments"""
	res = re.findall(rf'^{prefix}(.*)',command_string)
	argres = shlex.split(''.join(res))
	argsc = -1
	for arg in argres:
		if not arg:
			break
		argsc += 1

	for i in range(len(argres),max_args): # insert empty arguments
		argres.insert(i,'')

	if argres[0]:
		cmd = {'name': argres[0], 'args': argres[1:], 'args_count': argsc}

		if eval: return _EvalCmd(cmd) # only returns if command is valid
		return cmd


def _EvalCmd(parsed_command: ParseCmd):
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
				break # has found correct data type

	return parsed_command

def MatchArgs(parsed_command: ParseCmd, format, max_args=0):
	"""match argument formats, only works with eval"""

	# format example: 'ssf', arguments: ['hell','o',10.0] matched

	argtype = []
	
	if max_args < 0:
		max_args = 0

	if max_args == 0:
		for arg in parsed_command['args'][0:parsed_command['args_count']]:
			argtype.append(type(arg).__name__[0]) # get type char
	else:
		for arg in parsed_command['args'][0:max_args]:
			argtype.append(type(arg).__name__[0]) # get type char

	format = format.replace(' ','')
	format = list(format)

	matched = 0
	for i,t in enumerate(argtype):
		if t == 'i' or t == 'f':
			if format[i] == 's':
				matched += 1 # allow int or float as 's' format
		if t == format[i]:
			matched += 1

	if matched == len(format):
		return True

	return False

def ProcessCmd(parsed_command: ParseCmd, callback, attr={}):
	"""process command, to tell which function for processing the command, i guess..."""
	if type(parsed_command).__name__ != 'dict': raise TypeError("parsed_command must be a dict of parsed command")
	if type(callback).__name__ != 'function': raise TypeError("callback is not a function")

	if callback.__name__ != parsed_command['name']: raise NameError("callback name must be the same as command name") # callback name can be anything but yeah you can disable this if you want

	if not isinstance(attr, dict): raise TypeError("attributes must be in dict object")

	for a in attr:
		setattr(callback, a, attr[a])
		
	ret = callback(raw_args=parsed_command['args'],args=parsed_command['args'][0:parsed_command['args_count']])

	for a in attr:
		delattr(callback, a)

	return ret