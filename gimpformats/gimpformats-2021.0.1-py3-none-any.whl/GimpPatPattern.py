#!/usr/bin/env python3
"""Pure python implementation of a gimp pattern file.
"""
from __future__ import annotations

import argparse

import PIL.Image
from binaryiotools import IO


class GimpPatPattern:
	"""Pure python implementation of a gimp pattern file.

	See:
		https://gitlab.gnome.org/GNOME/gimp/blob/master/devel-docs/pat.txt
	"""

	COLOR_MODES = [None, "L", "LA", "RGB", "RGBA"]

	def __init__(self, fileName=None):
		self.fileName = None
		self.version = 1
		self.width = 0
		self.height = 0
		self.bpp = 4
		self.mode = self.COLOR_MODES[self.bpp]
		self.name = ""
		self._rawImage = None
		self._image = None
		if fileName is not None:
			self.load(fileName)

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
		"""Decode a byte buffer.

		:param data: data buffer to decode
		:param index: index within the buffer to start at
		"""
		ioBuf = IO(data, index)
		headerSize = ioBuf.u32
		self.version = ioBuf.u32
		self.width = ioBuf.u32
		self.height = ioBuf.u32
		self.bpp = ioBuf.u32
		self.mode = self.COLOR_MODES[self.bpp]
		magic = ioBuf.getBytes(4)
		if magic.decode("ascii") != "GPAT":
			raise Exception("File format error.  Magic value mismatch.")
		nameLen = headerSize - ioBuf.index
		self.name = ioBuf.getBytes(nameLen).decode("UTF-8")
		self._rawImage = ioBuf.getBytes(self.width * self.height * self.bpp)
		self._image = None

	def encode(self):
		"""Encode to a byte buffer."""
		ioBuf = IO()
		ioBuf.u32 = 24 + len(self.name)
		ioBuf.u32 = self.version
		ioBuf.u32 = self.width
		ioBuf.u32 = self.height
		ioBuf.u32 = len(self.image.mode)
		ioBuf.addBytes("GPAT")
		ioBuf.addBytes(self.name.encode("utf-8"))
		if self._rawImage is None:
			rawImage = self.image.tobytes(encoder_name="raw")
		else:
			rawImage = self._rawImage
		ioBuf.addBytes(rawImage)
		return ioBuf.data

	@property
	def size(self):
		"""The size of the pattern."""
		return (self.width, self.height)

	@property
	def image(self):
		"""Get a final, compiled image."""
		if self._image is None:
			if self._rawImage is None:
				return None
			self._image = PIL.Image.frombytes(
				self.mode, self.size, self._rawImage, decoder_name="raw"
			)
		return self._image

	@image.setter
	def image(self, image):
		self._image = image
		self._rawImage = None

	def save(self, tofileName=None, toExtension=None):
		"""Save this gimp image to a file."""
		asImage = False
		if toExtension is None:
			if tofileName is not None:
				toExtension = tofileName.rsplit(".", 1)
				if len(toExtension) > 1:
					toExtension = toExtension[-1]
				else:
					toExtension = None
		if toExtension is not None and toExtension != "pat":
			asImage = True
		if asImage:
			self.image.save(tofileName)
		else:
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
		ret.append("Name: " + str(self.name))
		ret.append("Version: " + str(self.version))
		ret.append("Size: " + str(self.width) + " x " + str(self.height))
		ret.append("BPP: " + str(self.bpp))
		ret.append("Mode: " + str(self.mode))
		return "\n".join(ret)


if __name__ == "__main__":
	"""CLI Entry Point."""
	parser = argparse.ArgumentParser("GimpPatPattern.py")
	parser.add_argument("xcfdocument", action="store", help="xcf file to act on")
	group = parser.add_mutually_exclusive_group()
	group.add_argument("--dump", action="store_true", help="dump info about this file")
	group.add_argument("--show", action="store_true", help="show the image")
	group.add_argument("--save", action="store", help="save out the image")
	args = parser.parse_args()

	gimpPatPattern = GimpPatPattern(args.xcfdocument)

	if args.dump:
		print(gimpPatPattern)
	if args.show:
		gimpPatPattern.image.show()
	if args.save:
		gimpPatPattern.image.save(args.save)
