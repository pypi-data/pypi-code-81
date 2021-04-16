#!/usr/bin/env python3
"""
Stuff related to vectors/paths within a gimp document
"""
#from .GimpIOBase import GimpIOBase
from __future__ import annotations
from binaryiotools import IO
from .GimpParasites import GimpParasite

class GimpVector:
	"""
	A gimp brush stroke vector
	"""
	def __init__(self, parent):
		#GimpIOBase.__init__(self, parent)
		self.name = ''
		self.uniqueId = 0
		self.visible = True
		self.linked = False
		self.parasites = []
		self.strokes = []

	def decode(self, data, index=0):
		"""
		decode a byte buffer

		:param data: data buffer to decode
		:param index: index within the buffer to start at
		"""
		ioBuf = IO(data, index, boolSize=32)
		self.name = ioBuf.sz754
		self.uniqueId = ioBuf.u32
		self.visible = ioBuf.bool
		self.linked = ioBuf.bool
		numParasites = ioBuf.u32
		numStrokes = ioBuf.u32
		for _ in range(numParasites):
			p = GimpParasite()
			ioBuf.index = p.decode(ioBuf.data, ioBuf.index)
			self.parasites.append(p)
		for _ in range(numStrokes):
			gs = GimpStroke(self)
			ioBuf.index = gs.decode(ioBuf.data, ioBuf.index)
			self.strokes.append(p)
		return ioBuf.index

	def encode(self):
		"""
		encode to binary data
		"""
		ioBuf = IO(boolSize=32)
		ioBuf.sz754 = self.name
		ioBuf.u32 = self.uniqueId
		ioBuf.bool = self.visible
		ioBuf.bool = self.linked
		ioBuf.u32 = len(self.parasites)
		ioBuf.u32 = len(self.strokes)
		for p in self.parasites:
			ioBuf.addBytes(p.encode())
		for gs in self.strokes:
			ioBuf.addBytes(gs.encode())
		return ioBuf.data

	def __repr__(self, indent: str='') -> str:
		"""
		Get a textual representation of this object
		"""
		ret = []
		ret.append('Name: ' + str(self.name))
		ret.append('Unique ID (tattoo): ' + str(self.uniqueId))
		ret.append('Visible: ' + str(self.visible))
		ret.append('Linked: ' + str(self.linked))
		if self.parasites:
			ret.append('Parasites: ')
			for item in self.parasites:
				ret.append(item.__repr__(indent + '\t'))
		if self.strokes:
			ret.append('Strokes: ')
			for item in self.strokes:
				ret.append(item.__repr__(indent + '\t'))
		return indent + (('\n' + indent).join(ret))


class GimpStroke:
	"""
	A single stroke within a vector
	"""

	STROKE_TYPES = ['None', 'Bezier']

	def __init__(self, parent):
		#GimpIOBase.__init__(self, parent)
		self.strokeType = 1 # one of self.STROKE_TYPES
		self.closedShape = True
		self.points = []

	def decode(self, data, index=0):
		"""
		decode a byte buffer

		:param data: data buffer to decode
		:param index: index within the buffer to start at
		"""
		ioBuf = IO(data, index, boolSize=32)
		self.strokeType = ioBuf.u32
		self.closedShape = ioBuf.bool
		numFloatsPerPoint = ioBuf.u32
		numPoints = ioBuf.u32
		for _ in range(numPoints):
			gp = GimpPoint(self)
			ioBuf.index = gp.decode(ioBuf.data, ioBuf.index, numFloatsPerPoint)
			self.points.append(gp)
		return ioBuf.index

	def encode(self):
		"""
		encode to binary data
		"""
		ioBuf = IO(boolSize=32)
		ioBuf.u32 = self.strokeType
		ioBuf.bool = self.closedShape
		#ioBuf.u32 = numFloatsPerPoint
		#ioBuf.u32 = numPoints
		for gp in self.points:
			ioBuf.addBytes(gp.encode())
		return ioBuf.data

	def __repr__(self, indent=''):
		"""
		Get a textual representation of this object
		"""
		ret = []
		ret.append('Stroke Type: ' + self.STROKE_TYPES[self.strokeType])
		ret.append('Closed: ' + str(self.closedShape))
		ret.append('Points: ')
		for point in self.points:
			ret.append(point.__repr__(indent + '\t'))
		return indent + (('\n' + indent).join(ret))


class GimpPoint:
	"""
	A single point within a stroke
	"""

	POINT_TYPES = ['Anchor', 'Bezier control point']

	def __init__(self, parent):
		#GimpIOBase.__init__(self, parent)
		self.x = 0
		self.y = 0
		self.pressure = 1.0
		self.xTilt = 0.5
		self.yTilt = 0.5
		self.wheel = 0.5
		self.pointType = 0

	def decode(self, data, index=0, numFloatsPerPoint=0):
		"""
		decode a byte buffer

		:param data: data buffer to decode
		:param index: index within the buffer to start at
		:param numFloatsPerPoint: required so we know
			how many different brush dynamic measurements are
			inside each point
		"""
		ioBuf = IO(data, index, boolSize=32)
		self.pressure = 1.0
		self.xTilt = 0.5
		self.yTilt = 0.5
		self.wheel = 0.5
		self.pointType = ioBuf.u32
		if numFloatsPerPoint < 1:
			numFloatsPerPoint = (len(ioBuf.data) - ioBuf.index) / 4
		self.x = ioBuf.float
		self.y = ioBuf.float
		if numFloatsPerPoint > 2:
			self.pressure = ioBuf.float
			if numFloatsPerPoint > 3:
				self.xTilt = ioBuf.float
				if numFloatsPerPoint > 4:
					self.yTilt = ioBuf.float
					if numFloatsPerPoint > 5:
						self.wheel = ioBuf.float
		return ioBuf.index

	def encode(self):
		"""
		encode to binary data
		"""
		ioBuf = IO(boolSize=32)
		ioBuf.u32 = self.pointType
		ioBuf.float = self.x
		ioBuf.float = self.y
		if self.pressure is not None:
			ioBuf.float = self.pressure
			if self.xTilt is not None:
				ioBuf.float = self.xTilt
				if self.yTilt is not None:
					ioBuf.float = self.yTilt
					if self.wheel is not None:
						ioBuf.float = self.wheel
		return ioBuf.data

	def __repr__(self, indent=''):
		"""
		Get a textual representation of this object
		"""
		ret = []
		ret.append('Location: (' + str(self.x) + ',' + str(self.y) + ')')
		ret.append('Pressure: ' + str(self.pressure))
		ret.append('Location: (' + str(self.xTilt) + ',' + str(self.yTilt) + ')')
		ret.append('Wheel: ' + str(self.wheel))
		return indent + (('\n' + indent).join(ret))
