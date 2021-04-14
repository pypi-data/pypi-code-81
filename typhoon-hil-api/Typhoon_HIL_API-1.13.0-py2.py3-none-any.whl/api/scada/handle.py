# coding=utf-8

#
# SCADA API handle module.
#
#
# This file is a part of Typhoon HIL API library.
#
# Typhoon HIL API is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import print_function, unicode_literals


class WidgetHandle(object):
    """
    Identifier for SCADA Widget on the server side
    exchangeable between client and server API side.
    """

    def __init__(self, item_type, item_fqid,
                 item_name, item_fqn, **kwargs):
        """
        Initialize handle object that carry out info about entity on the
        server side.

        Args:
            item_type (str): Widget type constant.
            item_fqid (str): Widget identifier (Widget ID)
            item_fqn (str): Widget fully qualified name (Widget FQN)
            item_name (str): Widget regular name
        """
        super().__init__()

        self.item_type = item_type
        self.item_fqid = item_fqid
        self.item_name = item_name
        self.item_fqn = item_fqn

    def __str__(self):
        """
        Custom string representation.
        """
        return "{0}: {1}".format(self.item_type, self.item_fqid)

    def __repr__(self):
        """
        Custom repr representation.
        """
        return "WidgetHandle('{}', '{}', '{}', '{}')".format(
            self.item_type, self.item_fqid, self.item_name, self.item_fqn)

    def __hash__(self):
        return hash((self.item_type, self.item_fqid,
                     self.item_name, self.item_fqn))

    def __eq__(self, other):
        return self.item_fqid == other.item_fqid \
            and self.item_type == other.item_type \
            and self.item_fqn == other.item_fqn \
            and self.item_name == other.item_name
