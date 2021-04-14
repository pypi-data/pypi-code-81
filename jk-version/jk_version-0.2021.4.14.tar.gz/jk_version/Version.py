


import typing
import re
import datetime





################################################################################################################################
## class Version
################################################################################################################################


class Version(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor
	#
	# @param		int[]|str version				The version string this object should represent
	#
	def __init__(self, version:typing.Union[str,list,tuple] = "0"):
		self.__epoch = 0

		if isinstance(version, (list, tuple)):

			if len(version) == 0:
				raise Exception("Invalid version number: \"" + str(version) + "\"")

			for i in version:
				assert isinstance(i, int)

			self.__numbers = tuple(version)

		elif isinstance(version, str):

			numbers = []
			try:
				# parse epoch if present

				pColon = version.find(":")
				if pColon == 0:
					raise Exception("Failed to parse version number: \"" + version + "\"")
				elif pColon > 0:
					self.__epoch = int(version[:pColon])
					version = version[pColon + 1:]

				# extract regular version number, strip additional information away

				m = re.match("^[0-9\.]+", version)
				if m:
					version = version[:m.end()]
					if version.endswith("."):
						version = version[:-1]
				else:
					# can't parse this
					raise Exception()

				if len(version) == 0:
					# can't parse this
					raise Exception()

				# parse regular version number

				for s in version.split("."):
					while (len(s) > 1) and (s[0] == "0"):		# remove trailing zeros of individual version components to allow accidental specification of dates as version information
						s = s[1:]
					numbers.append(int(s))

				# ----

				self.__numbers = tuple(numbers)

			except Exception:
				raise Exception("Failed to parse version number: \"" + version + "\"")

		else:
			raise Exception("Value of invalid type specified: " + str(type(version)))
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def length(self) -> int:
		return len(self.__numbers)
	#

	@property
	def numbers(self) -> list:
		return list(self.__numbers)
	#

	@property
	def isDateBase(self) -> bool:
		if len(self.__numbers) < 4:
			return False
		if self.__numbers[0] != 0:
			return False
		if (self.__numbers[1] < 2010) or (self.__numbers[1] > 2100):
			return False
		if (self.__numbers[2] < 1) or (self.__numbers[2] > 12):
			return False
		if (self.__numbers[3] < 1) or (self.__numbers[3] > 31):
			return False

		# everything seems to be plausible.

		return True
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def __hash__(self):
		return hash(self.__numbers)
	#

	def __str__(self):
		if (self.__epoch is None) or (self.__epoch == 0):
			ret = ""
		else:
			ret = str(self.__epoch) + ":"

		bFirst = True
		for v in self.__numbers:
			if bFirst:
				bFirst = False
			else:
				ret += "."
			ret += str(v)

		return ret
	#

	def __repr__(self):
		return self.__str__()
	#

	def compareTo(self, other):
		if isinstance(other, str):
			other = Version(other)

		if isinstance(other, Version):
			aNumbers = [ self.__epoch ] + list(self.__numbers)
			bNumbers = [ other.__epoch ] + list(other.__numbers)

			length = len(bNumbers)
			if len(aNumbers) < length:
				while len(aNumbers) < length:
					aNumbers.append(0)
			else:
				length = len(aNumbers)
				while len(bNumbers) < length:
					bNumbers.append(0)

			for i in range(0, length):
				na = aNumbers[i]
				nb = bNumbers[i]
				x = (na > nb) - (na < nb)
				# print("> " + str(na) + "  " + str(nb) + "  " + str(x))
				if x != 0:
					return x
			return 0
		
		else:
			raise Exception("Incompatible types: 'Version' and " + repr(type(other).__name__))
	#

	def __cmp__(self, other):
		n = self.compareTo(other)
		return n
	#

	def __lt__(self, other):
		n = self.compareTo(other)
		#print "???? a=" + str(self)
		#print "???? b=" + str(other)
		#print "???? " + str(n)
		return n < 0
	#

	def __le__(self, other):
		n = self.compareTo(other)
		#print "???? a=" + str(self)
		#print "???? b=" + str(other)
		#print "???? " + str(n)
		return n <= 0
	#

	def __gt__(self, other):
		n = self.compareTo(other)
		return n > 0
	#

	def __ge__(self, other):
		n = self.compareTo(other)
		return n >= 0
	#

	def __eq__(self, other):
		n = self.compareTo(other)
		return n == 0
	#

	def __ne__(self, other):
		n = self.compareTo(other)
		return n != 0
	#

	@staticmethod
	def now():
		dt = datetime.datetime.now()
		return Version([ 0, dt.year, dt.month, dt.day ])
	#

	@staticmethod
	def fromTimeStamp(t):
		dt = datetime.datetime.fromtimestamp(t)
		return Version([ 0, dt.year, dt.month, dt.day ])
	#

#

















