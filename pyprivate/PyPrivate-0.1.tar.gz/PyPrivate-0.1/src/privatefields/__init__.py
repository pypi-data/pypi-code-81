import inspect, sys, traceback

__privateattributes__ = ["__friendcodes"]

__friendcodes__ = []

def __privateexcepthook__(t, val, tb):
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

def __privategetattr__(self, attribute):
	code = inspect.currentframe().f_back.f_code
	oldhook = sys.excepthook
	sys.excepthook = __privateexcepthook__
	if code in __friendcodes__:
		val = object.__getattribute__(self, attribute)
		sys.excepthook = oldhook
		return val
	if (attribute.startswith("private_") and code not in self.__friendcodes) or attribute in __privateattributes__:
		raise AttributeError('\'' + self.__class__.__name__ + '\' object has no attribute \'' + attribute + '\'')
	elif attribute.startswith("protected_") and code not in self.__protectedfriendcodes:
		raise AttributeError('\'' + self.__class__.__name__ + '\' object has no attribute \'' + attribute + '\'')
	else:
		val = object.__getattribute__(self, attribute)
		sys.excepthook = oldhook
		return val
__friendcodes__.append(__privategetattr__.__code__)
def __privatesetattr__(self, attribute, value):
	code = inspect.currentframe().f_back.f_code
	oldhook = sys.excepthook
	sys.excepthook = __privateexcepthook__
	if code in __friendcodes__:
		object.__setattribute__(self, attribute, value)
		sys.excepthook = oldhook
	if (attribute.startswith("private_") and code not in self.__friendcodes) or attribute in __privateattributes__:
		raise AttributeError('\'' + self.__class__.__name__ + '\' object has no attribute \'' + attribute + '\'')
	elif attribute.startswith("protected_") and code not in self.__protectedfriendcodes:
		raise AttributeError('\'' + self.__class__.__name__ + '\' object has no attribute \'' + attribute + '\'')
	else:
		object.__setattribute__(self, attribute, value)
		sys.excepthook = oldhook
__friendcodes__.append(__privatesetattr__.__code__)

def __privatedir__(self):
	d = self.__firstdir__()
	r = []
	for a in d:
		if a.startswith("private_") or a.startswith("protected_") or a in __privateattributes__:
			continue
		r.append(a)
	return r

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

def privatefields(cls):
	cls.__friendcodes = []
	cls.__protectedfriendcodes = []
	__privateregisterfriends__(cls, list(cls.__dict__.values()))
	if not hasattr(cls, "friends"):
		cls.friends = []
	__privateregisterfriends__(cls)
	cls.friends = None
	del(cls.friends)
	cls.__firstdir__          = cls.__dir__
	cls.__dir__               = __privatedir__
	cls.__firstinitsubclass__ = cls.__init_subclass__
	cls.__init_subclass__     = __privateinitsubclass__
	cls.__getattribute__      = __privategetattr__
	cls.__setattribute__      = __privatesetattr__
	return cls
