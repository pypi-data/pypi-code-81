#!/usr/bin/env python3
"""
Pure python implementation of the OLD gimp gpb brush format
"""
from __future__ import annotations

import argparse
from io import BytesIO

from binaryiotools import IO

from .GimpGbrBrush import GimpGbrBrush
from .GimpPatPattern import GimpPatPattern


class GimpGpbBrush:
	"""
	Pure python implementation of the OLD gimp gpb brush format

	See:
		https://gitlab.gnome.org/GNOME/gimp/blob/master/devel-docs/vbr.txt
	"""

	def __init__(self, fileName: BytesIO | str):
		self.brush = GimpGbrBrush()
		self.pattern = GimpPatPattern()
		if hasattr(fileName, "read"):
			self.fileName = fileName.name
		else:
			self.fileName = fileName

	def load(self, fileName: BytesIO | str):
		"""Load a gimp file.

		:param fileName: can be a file name or a file-like object
		"""
		if isinstance(fileName, str):
			self.fileName = fileName
			file = open(fileName, "rb")
		else:
			self.fileName = fileName.name
			file = fileName
		data = file.read()
		file.close()
		self.decode(data)

	def decode(self, data, index=0):
		"""Decode a byte buffer

		:param data: data buffer to decode
		:param index: index within the buffer to start at
		"""
		index = self.brush.decode(data, index)
		# index = self.pattern.decode(data, index)
		return index

	def encode(self):
		"""Encode this object to a byte array."""
		ioBuf = IO()
		ioBuf.addBytes(self.brush.encode())
		ioBuf.addBytes(self.pattern.encode())
		return ioBuf.data

	def save(self, tofileName=None):
		"""Save this gimp image to a file."""
		if hasattr(tofileName, "write"):
			file = tofileName
		else:
			file = open(tofileName, "wb")
		file.write(self.encode())
		file.close()

	def __repr__(self, indent=""):
		"""Get a textual representation of this object."""
		ret = []
		if self.fileName is not None:
			ret.append("fileName: " + self.fileName)
		ret.append(self.brush.__repr__(indent + "\t"))
		ret.append(self.pattern.__repr__(indent + "\t"))
		return ("\n" + indent).join(ret)


if __name__ == "__main__":
	"""CLI Entry Point."""
	parser = argparse.ArgumentParser("GimpGbrBrush.py")
	parser.add_argument("xcfdocument", action="store", help="xcf file to act on")
	parser.add_argument("--dump", action="store_true", help="dump info about this file")
	args = parser.parse_args()

	gimpDocument = GimpGbrBrush(args.xcfdocument)

	if args.dump:
		print(gimpDocument)
