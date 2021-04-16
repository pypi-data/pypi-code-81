__version__ = "1.5.0"

from deriva.qt.common.async_task import async_execute, Task
from deriva.qt.common.log_widget import QPlainTextEditLogger
from deriva.qt.common.table_widget import TableWidget
from deriva.qt.common.json_editor import JSONEditor

from deriva.qt.auth_agent.ui.auth_window import AuthWindow
from deriva.qt.auth_agent.ui.embedded_auth_window import EmbeddedAuthWindow

from deriva.qt.upload_gui.ui.upload_window import UploadWindow
from deriva.qt.upload_gui.deriva_upload_gui import DerivaUploadGUI

import os
import sys

if sys.platform == "darwin":
    if getattr(sys, "frozen", False) and getattr(sys, "executable", False):
        executableDir = os.path.join(os.path.dirname(sys.executable))
        webEngineProcessLocation = os.path.join(executableDir, 'lib', 'PyQt5', 'Qt5', 'lib',
                                                'QtWebEngineCore.framework', 'Helpers', 'QtWebEngineProcess.app',
                                                'Contents', 'MacOS', 'QtWebEngineProcess')
        os.environ['QTWEBENGINEPROCESS_PATH'] = webEngineProcessLocation
