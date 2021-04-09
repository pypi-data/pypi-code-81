#/*##########################################################################
#
# The PyMca X-Ray Fluorescence Toolkit
#
# Copyright (c) 2021 European Synchrotron Radiation Facility
#
# This file is part of the PyMca X-ray Fluorescence Toolkit developed at
# the ESRF by the Software group.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#############################################################################*/
__author__ = "V.A. Sole - ESRF Data Analysis"
__contact__ = "sole@esrf.fr"
__license__ = "MIT"
__copyright__ = "European Synchrotron Radiation Facility, Grenoble, France"
import sys
import os
import numpy
from PyMca5 import DataObject
from PyMca5.PyMcaIO import TiffIO
if sys.version > '2.9':
    long = int

SOURCE_TYPE = "EdfFileStack"

class VolStackFile(DataObject.DataObject):
    def __init__(self, filename):
        if not isVolStackFile(filename):
            raise IOError("This does not look as a supported .vol file")

        # retrieve the needed information
        infofile = filename + ".info"
        NUM_X = -1
        NUM_Y = -1
        NUM_Z = -1
        voxelSize = -1
        BYTEORDER = -1
        with open(infofile, "rb") as f:
            for line in f:
                if line.startswith(b"NUM_X"):
                    NUM_X = int(line.split(b"=")[1])
                elif line.startswith(b"NUM_Y"):
                    NUM_Y = int(line.split(b"=")[1])
                elif line.startswith(b"NUM_Z"):
                    NUM_Z = int(line.split(b"=")[1])
        if NUM_X < 0 or NUM_Y < 0 or NUM_Z < 0:
            raise IOError("Invalid information in .info file")
        else:
            shape = (NUM_X, NUM_Y, NUM_Z)
        data = numpy.memmap(filename,
                            dtype=numpy.float32,
                            mode="r",
                            shape=shape)
        self.data = data
        self.sourceName = filename
        self.info = {}
        for i in range(len(shape)):
            key = 'Dim_%d' % (i + 1,)
            self.info[key] = shape[i]
        self.info["SourceType"] = SOURCE_TYPE
        self.info["SourceName"] = self.sourceName
        self.info["Size"]       = 1
        self.info["NumberOfFiles"] = 1
        self.info["FileIndex"] = 1
        self.info["McaIndex"] = 0
        if 0:
            self.info["xScale"] = (originX, deltaX)
            self.info["yScale"] = (originY, deltaY)
        

def isVolStackFile(filename):
    if filename.endswith(".vol") and os.path.exists(filename+".info"):
        #mandatory_fields = [b"NUM_X",
        #                    b"NUM_Y",
        #                    b"NUM_Z",
        #                    b"voxelSize",
        #                    b"BYTEORDER"]
        return True
    else:
        return False

if __name__ == "__main__":
    filename = None
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    print("is .vol File?", isVolStackFile(filename))
    instance = VolStackFile(filename)
    print(instance.info)
    print("Size = ", instance.data.size)
    print("Max = ", instance.data.max())
    print("Min = ", instance.data.min())
