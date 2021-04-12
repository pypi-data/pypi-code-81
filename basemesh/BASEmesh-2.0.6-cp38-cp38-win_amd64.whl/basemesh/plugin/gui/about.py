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

"""Python implementation of the about widget GUI."""

import os
from typing import Optional

from PyQt5.QtGui import QPixmap, QResizeEvent
from PyQt5.QtWidgets import QLabel, QPushButton, QTextBrowser
from qgis.gui import QgisInterface  # type: ignore

from .. import utils
from .base import DialogBase

try:
    import markdown2
except ModuleNotFoundError:
    import sys
    wheel_dir = os.path.join(utils.get_plugin_dir(), 'packages',
                             'markdown2-2.3.8-py2.py3-none-any.whl')
    sys.path.append(wheel_dir)
    import markdown2  # type: ignore


class AboutDialog(DialogBase):
    """GUI implementation of the elevation meshing utility."""

    # NOTE: Qt uses camelCase for its attributes - too bad!
    # pylint: disable=invalid-name

    ui_file = 'ui_about.ui'

    def __init__(self, iface: QgisInterface) -> None:
        """Connect signal callbacks and populate widgets.

        Parameters
        ----------
        iface : QgisInterface
            The QGIS interface to create the dialog for

        """
        super().__init__(iface)  # Initialize DialogBase

        # NOTE: The following are attribute type hints used to inform supported
        # IDEs of the attribute types defined in the Qt UI file. This code is
        # executed during runtime, but does not do anything as far as the
        # Python interpreter is concerned.
        self.banner: QLabel
        self.textBrowser: QTextBrowser
        self.linkRepo: QLabel
        self.linkWebsite: QLabel
        self.closeBtn: QPushButton

        # Load about text
        about_file = os.path.join(utils.get_plugin_dir(), 'plugin', 'gui',
                                  'templates', 'about_basemesh.md')
        try:
            with open(about_file) as about_markdown:
                html_str: str = markdown2.markdown(about_markdown.read())
        except FileNotFoundError:
            self.textBrowser.setText(
                f'Unable to generate help HTML, file not found:\n{about_file}')
        else:
            self.textBrowser.setHtml(html_str)

        # Apply size constraints
        self.pixmap = QPixmap(
            ':/plugins/basemesh/plugin/icons/basemesh_logo_with_text.png')
        self.resizeEvent()

    def resizeEvent(self, _: Optional[QResizeEvent] = None) -> None:
        """Event hook for the dialog being resized by the user."""
        # NOTE: Qt Designer does not support any form of "keep aspect ratio"
        # constraint, so this is set up in code instead.
        scaled = self.pixmap.scaledToHeight(self.banner.height())
        self.banner.setPixmap(scaled)
