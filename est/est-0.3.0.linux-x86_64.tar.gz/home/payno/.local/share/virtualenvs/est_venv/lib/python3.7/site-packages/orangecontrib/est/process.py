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
__date__ = "06/07/2019"


from silx.gui import qt
from Orange.widgets import gui
import logging

_logger = logging.getLogger(__file__)


class _ProcessForOrangeMixIn(object):
    """
    Group processing and progress display in a common class for xasObject
    process.

    If this process own a widget to display the xas object then this one should
    be named '_window'
    """

    def __init__(self):
        # progress
        self._progress = gui.ProgressBar(self, 100)
        """progress bar"""
        self.__processingThread = None
        """Thread for processing"""
        # progress
        self._progress = gui.ProgressBar(self, 100)

    def _startProcess(self):
        if hasattr(self, "_window"):
            self._window.setEnabled(False)
        self._progress.widget.progressBarInit()

    def _endProcess(self, xas_obj):
        if hasattr(self, "_window"):
            self._window.setEnabled(True)
        if self._callback_finish:
            try:
                self.getProcessingThread()._process_obj._advancement.sigProgress.disconnect(
                    self._setProgressValue
                )
            except ... as e:
                _logger.error(str(e))

            self.getProcessingThread().finished.disconnect(self._callback_finish)
            self._callback_finish = None
        if xas_obj is None:
            return
        else:
            if hasattr(self, "_window") and hasattr(self._window, "setXASObj"):
                self._window.setXASObj(xas_obj=xas_obj)
            elif hasattr(self, "_window") and hasattr(self._window, "xasObjViewer"):
                if hasattr(self._window.xasObjViewer, "setXASObj"):
                    self._window.xasObjViewer.setXASObj(xas_obj=xas_obj)
            # emit signal for the plot
            self.Outputs.res_xas_obj.send(xas_obj)

    def _canProcess(self):
        return (
            self.__processingThread is None or not self.__processingThread.isRunning()
        )

    def getProcessingThread(self):
        if self.__processingThread is None:
            self.__processingThread = ProcessQThread(parent=self)
        return self.__processingThread

    def _setProgressValue(self, value):
        self._progress.widget.progressBarSet(value)


class ProcessRunnable(qt.QRunnable):
    """
    qt Runnable for standard process.
    process function should take as input(spectrum, configuration, overwrite)

    :param function pointer fct: process function
    :param :class:`.Spectrum`: spectrum to process
    :param dict configuration: configuration of the process
    :param function pointer callback: optional callback to execute at the end of
                                      the run. Should take no parameter
    """

    def __init__(self, fct, spectrum, configuration, callback=None):
        qt.QRunnable.__init__(self)
        self._spectrum = spectrum
        self._configuration = configuration
        self._callback = callback
        self._function = fct

    def run(self):
        try:
            self._configuration, self._spectrum = self._function(
                spectrum=self._spectrum,
                configuration=self._configuration,
                overwrite=True,
            )
        except (KeyError, ValueError) as e:
            _logger.error(e)
        if self._callback:
            self._callback()


class ProcessQThread(qt.QThread):
    """
    Thread dedicated to process execution.
    """

    def __init__(self, parent=None):
        qt.QThread.__init__(self, parent)

    def init(self, xas_obj, process_obj):
        """
        Initialize the thread for processing xas_obj from proces_obj

        :param :class:`.XASObject` xas_obj: object to process
        :param :class:`.Process` process_obj: object to process xas_obj
        """
        self._xas_obj = xas_obj
        self._process_obj = process_obj

    def run(self):
        self._xas_obj = self._process_obj.process(self._xas_obj)
