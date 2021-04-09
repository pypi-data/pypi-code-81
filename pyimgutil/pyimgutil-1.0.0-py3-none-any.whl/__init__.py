"""Configure application-wide logging to the command-line.

Notes
-----
When a module in this package is imported, this __init__.py file is
implicitly executed (as in the case of the entry point). If this code
is not executed (as in the case of `python -m pyimgutil`), no logging
will be performed.

This logging setup is here, as opposed to elsewhere, because it greatly
simplifies using `__name__` to name individual loggers.

Copyright (C) 2021 emerac

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
import logging

# Each module's logger inherits its configuration from this logger.
# The level will be set and the handlers added by other functions.
logger = logging.getLogger(__name__)
formatter = logging.Formatter(
    "%(name)-32s %(relativeCreated)6d %(levelname)-8s %(message)s"
)
# Used when the 'verbose' option is set.
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
# Used when the 'quiet' option is set.
null_handler = logging.NullHandler()
