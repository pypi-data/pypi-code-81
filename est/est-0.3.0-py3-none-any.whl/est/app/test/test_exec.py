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
__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "06/26/2019"


import unittest
import tempfile
import shutil
from est.core.utils import DownloadDataset
from ..process import exec_
from pypushflow.representation.scheme.ows_parser import OwsParser
import os
from est.io.utils.information import InputInformation
from silx.io.url import DataUrl

try:
    import PyMca5
except ImportError:
    has_pymca = False
else:
    has_pymca = True
    from PyMca5.PyMcaDataDir import PYMCA_DATA_DIR


@unittest.skipIf(has_pymca is False, "PyMca5 is not installed")
class TestWorkflowFromOwsFile(unittest.TestCase):
    """test construction of XAS object"""

    def setUp(self):
        self.outputdir = tempfile.mkdtemp()
        file_ = "pymca_workflow_2.ows"
        DownloadDataset(dataset=file_, output_folder=self.outputdir, timeout=10.0)
        self.orange_file = os.path.join(self.outputdir, file_)
        self.input_file1 = os.path.join(PYMCA_DATA_DIR, "EXAFS_Cu.dat")
        self.output_file = os.path.join(self.outputdir, "output.h5")

    def tearDown(self):
        shutil.rmtree(self.outputdir)

    def testPyMcaWorkflow(self):
        """Test regarding the instantiation of the pymcaXAS"""
        exec_(
            scheme=OwsParser.scheme_load(self.orange_file, load_handlers=True),
            input_information=InputInformation(
                spectra_url=DataUrl(
                    file_path=self.input_file1, scheme="PyMca", data_path="Column 1"
                ),
                channel_url=DataUrl(
                    file_path=self.input_file1, scheme="PyMca", data_path="Column 2"
                ),
            ),
            output_=self.output_file,
        )
        self.assertTrue(os.path.exists(self.output_file))
        # TODO: check the values in the output file


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestWorkflowFromOwsFile,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
