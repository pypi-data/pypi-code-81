import inspect, sys, traceback, functools, re

__privateattributes__ = ["__friendcodes", "__firstdir__", "__firstinitsubclass__"]

__friendcodes__ = []

__oldhook__ = sys.excepthook

def __privateexcepthook__(t, val, tb):
	if tb.tb_next.tb_frame.f_code not in __friendcodes__:
		sys.excepthook = __oldhook__
		return sys.excepthook(t, val, tb)
	e = 'Traceback (most recent call last):\n'
	limit = 0
	tb2 = tb
	while tb2.tb_next != None:
		limit += 1
		tb2 = tb2.tb_next
	for i in traceback.extract_tb(tb, limit):
		e += ' ' * 2 + 'File "{0}", line {1}, in {2}'.format(*i) + '\n'
		e += ' '*4 + i[-1] + '\n'
		tb = tb.tb_next
	e += t.__name__ + ': ' + str(val) + '\n'
	sys.__stderr__.write(e)

def __privategetattr__(self, attribute, private, protected):
	code = inspect.currentframe().f_back.f_code
	if code in __friendcodes__:
		sys.excepthook = __privateexcepthook__
		val = object.__getattribute__(self, attribute)
		return val
	visualattribute = attribute
	if attribute.startswith("__") and not attribute.endswith("__"):
		attribute = "_" + self.__class__.__name__ + attribute
	if (visualattribute.startswith(private) and code not in self.__friendcodes) or attribute in __privateattributes__:
		sys.excepthook = __privateexcepthook__
		raise AttributeError('attribute \'' + visualattribute + '\' is private')
	elif visualattribute.startswith(protected) and code not in self.__protectedfriendcodes:
		sys.excepthook = __privateexcepthook__
		raise AttributeError('attribute \'' + visualattribute + '\' is protected')
	else:
		sys.excepthook = __privateexcepthook__
		val = object.__getattribute__(self, attribute)
		return val
__friendcodes__.append(__privategetattr__.__code__)
def __privatesetattr__(self, attribute, value, private, protected):
	code = inspect.currentframe().f_back.f_code
	sys.excepthook = __privateexcepthook__
	if code in __friendcodes__:
		object.__setattr__(self, attribute, value)
	if (attribute.startswith(private) and code not in self.__friendcodes) or attribute in __privateattributes__:
		raise AttributeError('attribute \'' + attribute + '\' is private')
	elif attribute.startswith(protected) and code not in self.__protectedfriendcodes:
		raise AttributeError('attribute \'' + attribute + '\' is protected')
	else:
		object.__setattr__(self, attribute, value)
__friendcodes__.append(__privatesetattr__.__code__)
def __privatedelattr__(self, attribute, private, protected):
	code = inspect.currentframe().f_back.f_code
	sys.excepthook = __privateexcepthook__
	if code in __friendcodes__:
		object.__delattr__(self, attribute)
	visualattribute = attribute
	if attribute.startswith("__") and not attribute.endswith("__"):
		attribute = "_" + self.__class__.__name__ + attribute
	if (visualattribute.startswith(private) and code not in self.__friendcodes) or attribute in __privateattributes__:
		raise AttributeError('attribute \'' + visualattribute + '\' is private')
	elif visualattribute.startswith(protected) and code not in self.__protectedfriendcodes:
		raise AttributeError('attribute \'' + visualattribute + '\' is protected')
	else:
		object.__delattr__(self, attribute)
__friendcodes__.append(__privatedelattr__.__code__)

def __privatedir__(self, private, protected):
	d = self.__firstdir__()
	r = []
	for a in d:
		if a in __privateattributes__:
			continue
		if a.startswith("__") and a.endswith("__"):
			r.append(a)
			continue
		if a.startswith("_" + self.__class__.__name__):
			a = a[len(self.__class__.__name__) + 1:]
		if a.startswith(private) or a.startswith(protected):
			continue
		r.append(a)
	return r
__friendcodes__.append(__privatedir__.__code__)

@classmethod
def __privateinitsubclass__(cls):
	for base in cls.__bases__:
		if hasattr(base, "__friendcodes"):
			__privateregisterprotectedfriends__(base, list(cls.__dict__.values()))

def __privateregisterfriends__(cls, friends=None):
	if friends == None:
		friends = cls.friends
	for friend in friends:
		if inspect.isclass(friend):
			__privateregisterfriends__(cls, list(friend.__dict__.values()))
		elif inspect.isfunction(friend):
			cls.__friendcodes.append(friend.__code__)
			cls.__protectedfriendcodes.append(friend.__code__)
def __privateregisterprotectedfriends__(cls, friends=None):
	if friends == None:
		friends = cls.friends
	for friend in friends:
		if inspect.isclass(friend):
			__privateregisterprotectedfriends__(cls, list(friend.__dict__.values()))
		elif inspect.isfunction(friend):
			cls.__protectedfriendcodes.append(friend.__code__)

def __privatefields__(cls, pythonStyle=False, updatedSystem=False):
	private   = "__" if pythonStyle else "private_"
	protected = "_"  if pythonStyle else "protected_"
	cls.__friendcodes = []
	cls.__protectedfriendcodes = []
	__privateregisterfriends__(cls, list(cls.__dict__.values()))
	if not hasattr(cls, "friends"):
		cls.friends = []
	__privateregisterfriends__(cls)
	cls.friends = None
	del(cls.friends)
	cls.__firstdir__          = cls.__dir__
	cls.__dir__               = functools.partialmethod(__privatedir__, private=private, protected=protected)
	cls.__firstinitsubclass__ = cls.__init_subclass__
	cls.__init_subclass__     = __privateinitsubclass__
	cls.__getattribute__      = functools.partialmethod(__privategetattr__, private=private, protected=protected)
	cls.__setattr__           = functools.partialmethod(__privatesetattr__, private=private, protected=protected)
	cls.__delattr__           = functools.partialmethod(__privatedelattr__, private=private, protected=protected)
	return cls

def privatefields(pythonStyle=False, updatedSystem=False):
	if updatedSystem:
		import privatefields.__updatedSystem__ # beta
		return __updatedSystem__.__privatefields__
	else:
		if inspect.isclass(pythonStyle):
			return __privatefields__(pythonStyle)
		else:
			return functools.partial(__privatefields__, pythonStyle=pythonStyle, updatedSystem=updatedSystem)
