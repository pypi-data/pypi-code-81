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
__date__ = "08/08/2019"


from Orange.widgets.widget import OWWidget
from Orange.widgets.widget import Input, Output
from est.core.types import XASObject
from orangecontrib.est.utils import Converter
import Orange.data


class ConverterOW(OWWidget):
    """
    Offer a conversion from XASObject to Orange.data.Table, commonly used
    from Orange widget
    """

    name = "converter xas_obj -> Table"
    id = "orange.widgets.xas.utils.converter"
    description = "convert a XASObject to a Orange.data.Table"
    icon = "icons/converter.png"
    priority = 5
    category = "esrfWidgets"
    keywords = ["spectroscopy", "signal", "output", "file"]

    want_main_area = False
    resizing_enabled = False
    allows_cycle = False

    class Inputs:
        xas_obj = Input("xas_obj", XASObject, default=True)
        # simple compatibility for some Orange widget and especialy the
        # 'spectroscopy add-on'

    class Outputs:
        res_data_table = Output("Data", Orange.data.Table)
        # by default we want to avoid sending 'Orange.data.Table' to avoid
        # loosing the XASObject flow process and results.

    @Inputs.xas_obj
    def process(self, xas_object):
        if xas_object is None:
            return
        data_table = Converter.toDataTable(xas_object=xas_object)
        self.Outputs.res_data_table.send(data_table)
