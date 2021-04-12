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
__date__ = "24/01/2017"

import logging
import os
import shutil
import tempfile
import unittest
from silx.gui import qt
from orangecontrib.est.test.OrangeWorkflowTest import OrangeWorflowTest

try:
    import PyMca5
except ImportError:
    has_pymca = False
else:
    has_pymca = True
    from PyMca5.PyMcaDataDir import PYMCA_DATA_DIR
from est.gui.qtapplicationmanager import QApplicationManager


logging.disable(logging.INFO)

_logger = logging.getLogger(__file__)

app = QApplicationManager()


@unittest.skipIf(has_pymca is False, "PyMca5 is not installed")
class TestSimplePyMcaWorkflow(OrangeWorflowTest):
    """Test the following workflow:
    - XASInputOW
    - NormalizationOW

    - XASOutputOW
    """

    def setUp(self):
        OrangeWorflowTest.setUp(self)
        # set input file
        data_file = os.path.join(PYMCA_DATA_DIR, "EXAFS_Cu.dat")
        self.xasInputWidget.setFileSelected(data_file)
        # set output file
        self.outputdir = tempfile.mkdtemp()
        self.output_file = os.path.join(self.outputdir, "output.h5")
        self.xasOutputWidget.setFileSelected(self.output_file)

    def tearDow(self):
        if os.path.isdir(self.outputdir):
            shutil.rmtree(self.outputdir)
        OrangeWorflowTest.tearDown(self)

    @classmethod
    def setUpClass(cls):
        OrangeWorflowTest.setUpClass()
        # create widgets
        xasInputNode = cls.addWidget(
            cls, "orangecontrib.est.widgets.utils.xas_input.XASInputOW"
        )
        xasNormalizationNode = cls.addWidget(
            cls, "orangecontrib.est.widgets.pymca.normalization.NormalizationOW"
        )
        xasEXAFSNode = cls.addWidget(
            cls, "orangecontrib.est.widgets.pymca.exafs.ExafsOW"
        )
        xasKWeightNode = cls.addWidget(
            cls, "orangecontrib.est.widgets.pymca.k_weight.KWeightOW"
        )
        xasFTNode = cls.addWidget(cls, "orangecontrib.est.widgets.pymca.ft.FTOW")
        xasOutputNode = cls.addWidget(
            cls, "orangecontrib.est.widgets.pymca.utils.xas_output.XASOutputOW"
        )

        cls.processOrangeEvents(cls)

        cls.link(cls, xasInputNode, "xas_obj", xasNormalizationNode, "xas_obj")
        cls.link(cls, xasNormalizationNode, "xas_obj", xasEXAFSNode, "xas_obj")
        cls.link(cls, xasEXAFSNode, "xas_obj", xasKWeightNode, "xas_obj")
        cls.link(cls, xasKWeightNode, "xas_obj", xasFTNode, "xas_obj")
        cls.link(cls, xasFTNode, "xas_obj", xasOutputNode, "xas_obj")
        cls.processOrangeEvents(cls)

        cls.xasInputWidget = cls.getWidgetForNode(cls, xasInputNode)
        cls.xasNormalizationWidget = cls.getWidgetForNode(cls, xasNormalizationNode)
        cls.xasEXAFSWidget = cls.getWidgetForNode(cls, xasEXAFSNode)
        cls.xasKWeightWidget = cls.getWidgetForNode(cls, xasKWeightNode)
        cls.xasFTWidget = cls.getWidgetForNode(cls, xasFTNode)
        cls.xasOutputWidget = cls.getWidgetForNode(cls, xasOutputNode)

    @classmethod
    def tearDownClass(cls):
        cls.xasInputWidget = None
        cls.xasNormalizationWidget = None
        cls.xasEXAFSWidget = None
        cls.xasKWeightWidget = None
        cls.xasFTWidget = None
        cls.xasOutputWidget = None
        OrangeWorflowTest.tearDownClass()

    def test(self):
        """Make sure the workflow is valid and end on the data transfert"""
        # start processing
        self.xasInputWidget.restart()
        # wait until end
        app = qt.QApplication.instance()
        while app.hasPendingEvents():
            app.processEvents()
            self.processOrangeEventsStack()

        # check plot have been updated
        self.assertEqual(self.xasNormalizationWidget._window.getNCurves(), 4)
        self.assertEqual(self.xasEXAFSWidget._window.getNCurves(), 3)
        self.assertEqual(self.xasKWeightWidget._window.getNCurves(), 2)
        self.assertEqual(self.xasFTWidget._window.getNCurves(), 2)

        #  check if file as been saved
        self.assertTrue(os.path.exists(self.output_file))


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestSimplePyMcaWorkflow,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite
