# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
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
# ###########################################################################*/

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "06/11/2019"


from .process import Process
from est.core.types import XASObject
from est.core.process.process import _input_desc
from est.core.process.process import _output_desc
import pkg_resources


class DumpXasObject(Process):

    inputs = [
        _input_desc(name="xas_obj", type=XASObject, handler="process", doc=""),
    ]

    outputs = [
        _output_desc(name="xas_obj", type=XASObject, doc=""),
    ]

    def __init__(self):
        super().__init__(name="dump xas object")
        self._output_file = None

    @property
    def output_file(self):
        return self._output_file

    @output_file.setter
    def output_file(self, output_file):
        self._output_file = output_file

    def program_name(self):
        """Name of the program used for this processing"""
        return "xas writer"

    def program_version(self):
        """version of the program used for this processing"""
        return pkg_resources.get_distribution("est").version

    def definition(self):
        """definition of the process"""
        return "write xas object to a file"

    def process(self, xas_object):
        if isinstance(xas_object, dict):
            xas_object = XASObject.from_dict(xas_object)
        if not isinstance(xas_object, XASObject):
            raise TypeError(
                "xas_object should be a convertable dict or an" "instance of XASObject"
            )

        if self.output_file is None:
            raise ValueError("output file not provided")
        else:
            xas_object.dump(self.output_file)

    def set_properties(self, properties):
        self.setConfiguration(properties)

    def setConfiguration(self, configuration):
        super().setConfiguration(configuration=configuration)
        self._read_output_file()

    def update_properties(self, properties):
        super().update_properties(properties=properties)
        self._read_output_file()

    def _read_output_file(self):
        if "output_file" in self._settings:
            self.output_file = self._settings["output_file"]
        elif "_output_file_setting" in self._settings:
            self.output_file = self._settings["_output_file_setting"]

    __call__ = process
