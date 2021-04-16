#!/usr/bin/env python3
"""Pure python implementation of the gimp gbr brush format.
"""
from __future__ import annotations

import argparse
from io import BytesIO
from typing import Union

import PIL.Image
from binaryiotools import IO


class GimpGbrBrush:
	"""Pure python implementation of the gimp gbr brush format.

	See:
		https://gitlab.gnome.org/GNOME/gimp/blob/master/devel-docs/gbr.txt
	"""

	COLOR_MODES = [None, "L", "LA", "RGB", "RGBA"]  # only L or RGB allowed

	def __init__(self, fileName=None):
		self.fileName = None
		self.version = 2
		self.width = 0
		self.height = 0
		self.bpp = 1
		self.mode = self.COLOR_MODES[self.bpp]
		self.name = ""
		self.rawImage = None
		self.spacing = 0
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

	def decode(self, data: bytes, index: int = 0) -> int:
		"""Decode a byte buffer.

		:param data: data buffer to decode
		:param index: index within the buffer to start at
		"""
		ioBuf = IO(data, index)
		headerSize = ioBuf.u32
		self.version = ioBuf.u32
		if self.version != 2:
			raise Exception("ERR: unknown brush version " + str(self.version))
		self.width = ioBuf.u32
		self.height = ioBuf.u32
		self.bpp = ioBuf.u32  # only allows grayscale or RGB
		self.mode = self.COLOR_MODES[self.bpp]
		magic = ioBuf.getBytes(4)
		if magic.decode("ascii") != "GIMP":
			raise Exception(
				'"'
				+ magic.decode("ascii")
				+ '" '
				+ str(index)
				+ " File format error.  Magic value mismatch."
			)
		self.spacing = ioBuf.u32
		nameLen = headerSize - ioBuf.index
		self.name = ioBuf.getBytes(nameLen).decode("UTF-8")
		self.rawImage = ioBuf.getBytes(self.width * self.height * self.bpp)
		return ioBuf.index

	def encode(self) -> bytearray:
		"""
		encode this object to byte array
		"""
		ioBuf = IO()
		ioBuf.u32 = 28 + len(self.name)
		ioBuf.u32 = self.version
		ioBuf.u32 = self.width
		ioBuf.u32 = self.height
		ioBuf.u32 = self.bpp
		ioBuf.addBytes("GIMP")
		ioBuf.u32 = self.spacing
		ioBuf.addBytes(self.name)
		ioBuf.addBytes(self.rawImage)
		return ioBuf.data

	@property
	def size(self) -> tuple[int, int]:
		"""Get the size."""
		return (self.width, self.height)

	@property
	def image(self) -> PIL.Image.Image | None:
		"""	get a final, compiled image."""
		if self.rawImage is None:
			return None
		return PIL.Image.frombytes(self.mode, self.size, self.rawImage, decoder_name="raw")

	def save(self, tofileName: str, toExtension: str | None = None):
		"""	save this gimp image to a file."""
		asImage = False
		if toExtension is None:
			if tofileName is not None:
				extParts = tofileName.rsplit(".", 1)
				if len(extParts) > 0:
					toExtension = extParts[-1]
				else:
					toExtension = None
		if toExtension is not None and toExtension != "gbr":
			asImage = True
		if asImage:
			self.image.save(tofileName)
			self.image.close()
		else:
			if hasattr(tofileName, "write"):
				file = tofileName
			else:
				file = open(tofileName, "wb")
			file.write(self.encode())
			file.close()

	def __repr__(self, indent=""):
		"""	Get a textual representation of this object."""
		ret = []
		if self.fileName is not None:
			ret.append("fileName: " + self.fileName)
		ret.append("Name: " + str(self.name))
		ret.append("Version: " + str(self.version))
		ret.append("Size: " + str(self.width) + " x " + str(self.height))
		ret.append("Spacing: " + str(self.spacing))
		ret.append("BPP: " + str(self.bpp))
		ret.append("Mode: " + str(self.mode))
		return ("\n" + indent).join(ret)


if __name__ == "__main__":
	"""CLI Entry Point."""
	parser = argparse.ArgumentParser("GimpGbrBrush.py")
	parser.add_argument("xcfdocument", action="store", help="xcf file to act on")
	group = parser.add_mutually_exclusive_group()
	group.add_argument("--dump", action="store_true", help="dump info about this file")
	group.add_argument("--show", action="store_true", help="show the brush image")
	group.add_argument("--save", action="store", help="save out the brush image")
	args = parser.parse_args()

	gimpDocument = GimpGbrBrush(args.xcfdocument)

	if args.dump:
		print(gimpDocument)
	if args.show:
		gimpDocument.image.show()
	if args.save:
		gimpDocument.image.save(args.save)
