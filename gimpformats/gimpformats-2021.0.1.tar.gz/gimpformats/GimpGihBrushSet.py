#!/usr/bin/env python3
"""Gimp Image Pipe Format.

The gih format is use to store a series of brushes, and some extra info
for how to use them.
"""
from __future__ import annotations

import argparse
from io import BytesIO

from binaryiotools import IO

from .GimpGbrBrush import GimpGbrBrush


class GimpGihBrushSet:
	"""Gimp Image Pipe Format.

	The gih format is use to store a series of brushes, and some extra info
	for how to use them.

	See:
		https://gitlab.gnome.org/GNOME/gimp/blob/master/devel-docs/gih.txt
	"""

	def __init__(self, fileName=None):
		self.fileName = None
		self.name = ""
		self.params = {}
		self.brushes = []
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

	def decode(self, data: bytearray, index: int = 0):
		"""Decode a byte buffer.

		:param data: data buffer to decode
		:param index: index within the buffer to start at
		"""
		ioBuf = IO(data, index)
		self.name = ioBuf.textLine
		secondLine = ioBuf.textLine.split(" ")
		self.params = {}
		numBrushes = int(secondLine[0])
		# everything that's left is a gimp-image-pipe-parameters parasite
		for i in range(1, len(secondLine)):
			param = secondLine[i].split(":", 1)
			self.params[param[0].strip()] = param[1].strip()
		self.brushes = []
		for _ in range(numBrushes):
			brush = GimpGbrBrush()
			ioBuf.index = brush.decode(
				ioBuf.data, ioBuf.index
			)  # TODO: broken.  For some reason there is extra data between brushes!
			self.brushes.append(brush)
		return ioBuf.index

	def encode(self):
		"""Encode this object to a byte array."""
		ioBuf = IO()
		ioBuf.textLine = self.name
		# add the second line of data
		secondLine = [str(len(self.brushes))]
		for key in self.params:
			secondLine.append(key + ":" + str(self.params[key]))
		ioBuf.textLine = " ".join(secondLine)
		# add the brushes
		for brush in self.brushes:
			ioBuf.addBytes(brush.encode())
		return ioBuf.data

	def save(self, tofileName: str):
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
		ret.append("Name: " + str(self.name))
		for k, val in list(self.params.items()):
			ret.append(k + ": " + str(val))
		for i in range(len(self.brushes)):
			ret.append("Brush " + str(i))
			ret.append(self.brushes[i].__repr__(indent + "\t"))
		return ("\n" + indent).join(ret)


if __name__ == "__main__":
	"""CLI Entry Point."""
	parser = argparse.ArgumentParser("GimpGihBrushSet.py")
	parser.add_argument("xcfdocument", action="store", help="xcf file to act on")
	group = parser.add_mutually_exclusive_group()
	group.add_argument("--dump", action="store_true", help="dump info about this file")
	group.add_argument(
		"--show", action="store", help="show the brush image (n or * for all layers)"
	)
	group.add_argument("--save", action="store", help="save out the brush set (n,out-file.png)")
	args = parser.parse_args()

	gimpGihBrushSet = GimpGihBrushSet(args.xcfdocument)

	if args.dump:
		print(gimpGihBrushSet)
	if args.show:
		if args.show == "*":
			for iterationM in range(len(gimpGihBrushSet.brushes)):
				gimpGihBrushSet.brushes[iterationM].image.show()
		else:
			gimpGihBrushSet.brushes[int(args.show)].image.show()
	if args.save:
		indexM, fileNameM = args.save.split(",", 1)
		if fileNameM.find("*") < 0:
			fileNameM = "*.".join(fileNameM.split(".", 1))
		if indexM == "*":
			for iterationM in range(len(gimpGihBrushSet.brushes)):
				fn2 = fileNameM.replace("*", str(iterationM))
				gimpGihBrushSet.brushes[iterationM].image.save(fn2)
		else:
			fn2 = fileNameM.replace("*", iterationM)
			gimpGihBrushSet.brushes[int(indexM)].image.save(fn2)
