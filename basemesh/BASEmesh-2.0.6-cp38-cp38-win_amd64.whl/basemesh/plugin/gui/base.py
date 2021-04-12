# A component of the BASEmesh pre-processing toolkit.
# Copyright (C) 2020  ETH Zürich

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Shared base classes for the BASEmesh GUI."""

import datetime
import os
import time
import traceback
from typing import Any, Callable, Deque, Optional, Tuple
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import (QComboBox, QDialog, QFileDialog, QLineEdit,
                             QMessageBox, QPlainTextEdit, QPushButton,
                             QTextEdit)
from PyQt5.uic import loadUi  # type: ignore
from qgis.core import (QgsApplication, QgsMapLayer,  # type: ignore
                       QgsMapLayerType, QgsWkbTypes)
from qgis.gui import QgisInterface  # type: ignore
from ..utils import (add_layers, get_plugin_dir, get_project_dir,
                     get_project_title, layer_is_3d)
from .worker import Worker

try:
    import markdown2
except ModuleNotFoundError:
    import sys
    wheel_dir = os.path.join(get_plugin_dir(), 'packages',
                             'markdown2-2.3.8-py2.py3-none-any.whl')
    sys.path.append(wheel_dir)
    import markdown2  # type: ignore

# Type aliases
_FeedbackSignal = Tuple[Optional[float], Optional[str], bool]


class DialogBase(QDialog):
    """Base class for standalone windows in BASEmesh.

    Any subclasses must overwrite the ui_file name with the name of
    the .ui file to use for their initialisation.
    """

    # NOTE: While it would be nice to turn this into an ABC to ensure certain
    # class attributes are overridden before initialization, this is not
    # possible due to the way Qt wrapper classes are instantiated.
    # I am sure there are workarounds for this, but they would probably cause
    # more confusion and visual clutter than the use-case justifies.

    ui_file: str  # The UI resource to use
    help_file: str  # Markdown file containing help text (optional)

    def __init__(self, iface: QgisInterface) -> None:
        """Set the interface attribute and populate the dialog.

        Parameters
        ----------
        iface : QgisInterface
            The QGIS interface object to load itno

        Raises
        ------
        AttributeError
            Raised if the ui_file attribute has not been overwritten
            with a custom path
        """
        super().__init__()  # Initialize QDialog
        self.iface = iface
        # Load UI resource file
        try:
            src_path = os.path.join(
                get_plugin_dir(), 'plugin', 'gui', 'templates', self.ui_file)
        except AttributeError as err:
            raise AttributeError(f'{self.__class__.__name__} does not provide '
                                 'an ui_file attribute') from err
        loadUi(src_path, self)

    def add_mesh_layers(self, combo_box: QComboBox, *args: QComboBox) -> None:
        """Populate the combo box with mesh layers.

        Use QComboBox.currentData() to retrieve the currently selected
        layer.
        The combo box will be cleared as part of this call.

        Parameters
        ----------
        combo_box : QComboBox
            The combo box to add the mesh layers to
        """
        icon = QgsApplication.getThemeIcon('/mIconMeshLayer.svg')
        add_layers(self.iface.mapCanvas(), combo_box, *args, icon=icon,
                   filter_=lambda x: x.type()  # type: ignore
                   == QgsMapLayerType.MeshLayer)

    def add_point_layers(self, combo_box: QComboBox, *args: QComboBox,
                         has_z: Optional[bool] = None) -> None:
        """Populate the combo box with point vector layers.

        Use QComboBox.currentData() to retrieve the currently selected
        layer.
        The combo box will be cleared as part of this call.

        Parameters
        ----------
        combo_box : QComboBox
            The combo box to add the vector layers to
        """

        def filter_(layer: QgsMapLayer) -> bool:
            if (layer.type() != QgsMapLayerType.VectorLayer
                    or layer.geometryType() != QgsWkbTypes.PointGeometry):
                return False
            return has_z is None or has_z == layer_is_3d(layer)

        icon = QgsApplication.getThemeIcon('/mIconPointLayer.svg')
        add_layers(self.iface.mapCanvas(), combo_box, *args, icon=icon,
                   filter_=filter_)

    def add_polygon_layers(self, combo_box: QComboBox, *args: QComboBox,
                           has_z: Optional[bool] = None) -> None:
        """Populate the combo box with polygon vector layers.

        Use QComboBox.currentData() to retrieve the currently selected
        layer.
        The combo box will be cleared as part of this call.

        Parameters
        ----------
        combo_box : QComboBox
            The combo box to add the vector layers to
        """

        def filter_(layer: QgsMapLayer) -> bool:
            if (layer.type() != QgsMapLayerType.VectorLayer
                    or layer.geometryType() != QgsWkbTypes.PolygonGeometry):
                return False
            return has_z is None or has_z == layer_is_3d(layer)

        icon = QgsApplication.getThemeIcon('/mIconPolygonLayer.svg')
        add_layers(self.iface.mapCanvas(), combo_box, *args, icon=icon,
                   filter_=filter_)

    def add_polyline_layers(self, combo_box: QComboBox, *args: QComboBox,
                            has_z: Optional[bool] = None) -> None:
        """Populate the combo box with polyline vector layers.

        Use QComboBox.currentData() to retrieve the currently selected
        layer.
        The combo box will be cleared as part of this call.

        Parameters
        ----------
        combo_box : QComboBox
            The combo box to add the vector layers to
        """

        def filter_(layer: QgsMapLayer) -> bool:
            if (layer.type() != QgsMapLayerType.VectorLayer
                    or layer.geometryType() != QgsWkbTypes.LineGeometry):
                return False
            return has_z is None or has_z == layer_is_3d(layer)

        icon = QgsApplication.getThemeIcon('/mIconLineLayer.svg')
        add_layers(self.iface.mapCanvas(), combo_box, *args, icon=icon,
                   filter_=filter_)

    def add_raster_layers(self, combo_box: QComboBox, *args: QComboBox) -> None:
        """Populate the combo box with raster layers.

        Use QComboBox.currentData() to retrieve the currently selected
        layer.
        The combo box will be cleared as part of this call.

        Parameters
        ----------
        combo_box : QComboBox
            The combo box to add the raster layers to
        """
        icon = QgsApplication.getThemeIcon('/mIconRasterLayer.svg')
        add_layers(self.iface.mapCanvas(), combo_box, *args, icon=icon,
                   filter_=lambda x: x.type()  # type: ignore
                   == QgsMapLayerType.RasterLayer)

    def browse_for_output(self, file_format: str, line_edit: QLineEdit,
                          name_suffix: Optional[str] = None,
                          caption: str = 'Select output file'
                          ) -> Callable[[], None]:
        """Return the callback for an output file picker button.

        This returns a callable that can be passed to the browse
        button's "clicked" slot. This allows customization of the
        callback without requiring an intermediate method.

        Parameters
        ----------
        file_format : str
            The file extension to use
        line_edit : QLineEdit
            The line edit to paste the result string into
        name_suffix : str, optional
            The auto-generated file name to use, by default None
        caption : str, optional
            The caption displayed in the title bar of the file browser,
            by default 'Select output file'

        Returns
        -------
        Callable[[], None]
            Browse button callback
        """
        file_format = file_format.strip('.')
        # The following names will be accessible from within the returned
        # callback
        filter_ = _filter_from_format(file_format)

        # Generate default file name
        filename = get_project_title()
        if name_suffix is not None:
            filename += f'_{name_suffix}'
        filename += f'.{file_format}'
        file_path = os.path.join(get_project_dir(), filename)

        def callback() -> None:
            line_edit.clear()
            file_dialog = QFileDialog()
            file_dialog.setDefaultSuffix(file_format)
            # NOTE: The second tuple element returned is the file filter used
            output_path, _ = file_dialog.getSaveFileName(
                self, caption, file_path, filter_)
            if output_path == '':
                return

            # Add the file extension if it does not exist
            if not output_path.endswith(f'{file_format}'):
                output_path += f'.{file_format}'
            line_edit.setText(output_path)

        return callback

    def print_error(self, err: BaseException) -> None:
        """Display an error message to the user.

        If the error provided is an instance of InterruptedError, this
        does nothing.

        Parameters
        ----------
        err : BaseException
            The error to display
        """
        if err is None:
            return
        # Ignore user interruption signals
        if isinstance(err, InterruptedError):
            return
        text = ('The BASEmesh worker raised an error.\n'
                'See details for traceback and additional information.')
        msg_box = QMessageBox(QMessageBox.Critical, 'BASEmesh - Error', text,
                              buttons=QMessageBox.Ok, parent=self)
        if err.args:
            err_msg = f'{err.__class__.__name__}: '
            err_msg += ', '.join(str(c) for c in err.args)
            msg_box.setInformativeText(err_msg)
        msg_box.setDetailedText(''.join(traceback.format_exception(
            type(err), err, err.__traceback__)))
        msg_box.exec()

    def export_log(self, prefix: str,
                   text_box: QPlainTextEdit) -> Callable[[], None]:
        """Generate and return the log export button's callback.

        The prefix will be used as the default name for the output
        file, together with the timestamp.
        If the prefix were "elevmesh", the default output filename
        would become "log_elevmesh_YYY-MM-DD_HH-MM-SS.log".

        Parameters
        ----------
        prefix : str
            The prefix to prepend to the log timestamp
        text_box : QPlainTextEdit
            The log window whos contents will be saved to a file

        Returns
        -------
        Callable[[], None]
            The export log button callback
        """
        file_dialog = QFileDialog()
        file_dialog.setDefaultSuffix('log')

        def callback() -> None:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            base_name = f'log_{prefix}_{timestamp}'
            file_path = os.path.join(get_project_dir(), base_name)

            output_path, _ = file_dialog.getSaveFileName(
                self, 'Save log to file', file_path, 'Text file (*.log)')
            if output_path == '':
                return

            text = text_box.toPlainText()
            # Add a final newline if missing
            if not text.endswith('\n'):
                text += '\n'
            with open(output_path, 'w') as out_file:
                out_file.write(text)

        return callback

    def load_help(self, text_edit: QTextEdit) -> None:
        """Populate the help frame with the corresponding HTML text.

        The text will be generated using a markdown file specified by
        the dialog's help_file attribute.

        Parameters
        ----------
        text_edit : QTextEdit
            The help frame to populate

        Raises
        ------
        AttributeError
            Raised if the help_file attribute has not been set
        """
        try:
            help_file = self.help_file
        except AttributeError as err:
            raise AttributeError(f'{self.__class__.__name__} does not provide '
                                 'a help_file attribute') from err
        help_file = os.path.join(
            get_plugin_dir(), 'plugin', 'gui', 'templates', help_file)
        try:
            with open(help_file) as help_markdown:
                html_str: str = markdown2.markdown(help_markdown.read())
        except FileNotFoundError:
            text_edit.setText(
                f'Unable to generate help HTML, file not found:\n{help_file}')
        else:
            text_edit.setHtml(html_str)

    def run_worker(self, *args: Any, log: Optional[QPlainTextEdit] = None,
                   after: Callable[[Any, Optional[BaseException]], None],
                   cancel_btn: QPushButton, **kwargs: Any) -> None:
        """Run the dialog's "worker" method in another thread.

        Any anonymous arguments and keyword arguments passed to this
        function will be passed on to the worker method. Additionally,
        the worker method's first argument will be a Feedback object
        used to communicate with its parent thread.

        Parameters
        ----------
        after : Callable[[Any, Optional[BaseException]], None]
            A function to run after the worker thread exist, the first
            argument is the return value, the second an exception that
            was raised, if any
        cancel_btn : QPushButton
            A button that will signal the worker function to quit
        log : QPlainTextEdit, optional
            An optional log window to display log messages in via the
            feedback object, by default None
        """
        # NOTE: The following functions are callbacks to run based on worker
        # thread status:

        def cancelled() -> None:
            # Run if cancellation was requested by the user
            worker.cancel()

        def done(return_value: Any) -> None:
            # Run when the worker has finished execution
            teardown()
            after(return_value, None)

        def error(err: BaseException) -> None:
            # Run when the worker thread encountered an exception
            teardown()
            after(None, err)

        def print_(deque_: Deque[str]) -> None:
            # Run when the thread wants to print to stdout
            if log is not None:
                # Consolidate all stdout prints into a single block of text to
                # be inserted at once
                merged = ''.join(deque_)
                deque_.clear()
                cursor = log.textCursor()
                log.insertPlainText(merged)
                log.moveCursor(cursor.End)

        def teardown() -> None:
            # Destroy the worker thread
            thread.quit()
            thread.wait()

        # Instantiate the worker object
        worker = Worker(target=self.worker, args=args, kwargs=kwargs)
        # Create a new thread to run the worker in
        thread = QThread(self)
        worker.moveToThread(thread)

        # Hook up signals
        cancel_btn.clicked.connect(cancelled)
        thread.started.connect(worker.run)  # type: ignore
        thread.finished.connect(worker.deleteLater)  # type: ignore
        worker.done.connect(done)
        worker.error.connect(error)
        worker.print.connect(print_)
        worker.status.connect(self._push_status)

        thread.start()

        time.sleep(0.01)  # HACK: The thread will not start unless we do this

    def _push_status(self, status_tuple: _FeedbackSignal) -> None:
        """Update the progress bar and status message.

        The only parameter is a tuple consisting of three values:
        The new progress percentage (None if unchanged), the new status
        message (None if unchanged), and a flag to show whether the
        worker is busy.

        Parameters
        ----------
        status_tuple : Tuple[Optional[float], Optional[str], bool]
            A status reporting tuple sent from the worker thread
        """
        progress, msg, busy = status_tuple
        if msg is not None:
            self.status.setText(msg)
        if busy:
            # Setting the progress bar to 0/0 causes it to play the "busy"
            # animation
            self.progressBar.setMaximum(0)
            self.progressBar.reset()
        else:
            # If it is not busy, make sure the progress bar is ready to
            # update
            if self.progressBar.maximum() == 0:
                self.progressBar.setMaximum(100)
                self.progressBar.setValue(0)
        if progress is not None and not busy:
            if progress < 0.0:
                progress = 0.0
            elif progress > 1.0:
                progress = 1.0
            self.progressBar.setValue(int(progress*100))


def _filter_from_format(file_format: str) -> str:
    """Return a file format filter for the given format string.

    Allowed format strings are "txt", "log", "2dm", "dxf", "shp",
    "bmg", and "g01".

    Parameters
    ----------
    file_format : str
        The format string to use

    Returns
    -------
    str
        The Qt format string used for file selection
    """
    # The following dict maps file extensions to their canonical format names.
    # It acts as a helper to ensure consistency between tools.
    conversion_dict = {'txt': 'Text file',
                       'log': 'Text file',
                       '2dm': 'SMS 2D mesh',
                       'dxf': 'AutoCAD DXF',
                       'shp': 'Shapefile',
                       'bmg': 'BMG file',
                       'g01': 'HECRAS geometry'}
    name = conversion_dict[file_format]
    return f'{name} (*{file_format})'
