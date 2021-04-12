# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2017-2019 European Synchrotron Radiation Facility
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
"""some utils function for executing reprocessing"""


__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "07/18/2019"

import importlib
import logging
from silx.io.utils import h5py_read_dataset

_logger = logging.getLogger(__name__)


def get_process_instance_frm_h5_desc(desc):
    """

    :param dict desc: description of the process to instanciate
    :return: instance of the process to execute, configured from the description
    """
    assert "program" in desc
    assert "class_instance" in desc
    tmp = h5py_read_dataset(desc["class_instance"]).split(".")
    module_name = ".".join(tmp[:-1])
    class_name = tmp[-1]
    try:
        _module = importlib.import_module(module_name)
        instance = getattr(_module, class_name)()
    except Exception as e:
        _logger.warning(
            " ".join(("Fail to instanciate", module_name, class_name, "reason is", e))
        )
        instance = None
    else:
        if "configuration" in desc:
            instance.setConfiguration(desc["configuration"])
    return instance
