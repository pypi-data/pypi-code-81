# This file is part of Flatplan.
#
# Flatplan is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Flatplan is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Flatplan.  If not, see <https://www.gnu.org/licenses/>.

from .flattener import Flattener, PlanFlattener, StateFlattener
from .hooks import Hook, HookContext, RemoveResourceByTagHook
from .main import main, run

assert Flattener
assert PlanFlattener
assert StateFlattener
assert Hook
assert HookContext
assert RemoveResourceByTagHook
assert main
assert run
