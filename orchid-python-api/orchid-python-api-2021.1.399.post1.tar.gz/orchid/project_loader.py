#  Copyright 2017-2021 Reveal Energy Services, Inc 
#
#  Licensed under the Apache License, Version 2.0 (the "License"); 
#  you may not use this file except in compliance with the License. 
#  You may obtain a copy of the License at 
#
#      http://www.apache.org/licenses/LICENSE-2.0 
#
#  Unless required by applicable law or agreed to in writing, software 
#  distributed under the License is distributed on an "AS IS" BASIS, 
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
#  See the License for the specific language governing permissions and 
#  limitations under the License. 
#
# This file is part of Orchid and related technologies.
#

import functools

import deal

from orchid import (
    dot_net,
    script_adapter_context as sac,
    validation,
)

# noinspection PyUnresolvedReferences
from System import InvalidOperationException
# noinspection PyUnresolvedReferences
from System.IO import (FileStream, FileMode, FileAccess, FileShare)
# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics.SDKFacade import ScriptAdapter


class OrchidError(Exception):
    pass


@functools.lru_cache()
def native_treatment_calculations():
    """
    Returns a .NET ITreatmentCalculations instance to be adapted.

    Returns:
            An `ITreatmentCalculations` implementation.
    """
    with sac.ScriptAdapterContext():
        result = ScriptAdapter.CreateTreatmentCalculations()
    return result


class ProjectLoader:
    """Provides an .NET IProject to be adapted."""

    @deal.pre(validation.arg_not_none)
    @deal.pre(validation.arg_neither_empty_nor_all_whitespace)
    def __init__(self, project_pathname: str):
        """
        Construct an instance that loads project data from project_pathname

        Args:
            project_pathname: Identifies the data file for the project of interest.
        """
        self._project_pathname = project_pathname
        self._project = None
        self._in_context = False

    def native_project(self):
        """
        Return the native (.NET) Orchid project.

        Returns:
            The loaded `IProject`.
        """
        if not self._project:
            with sac.ScriptAdapterContext():
                reader = ScriptAdapter.CreateProjectFileReader(dot_net.app_settings_path())
                # TODO: These arguments are *copied* from `ProjectFileReaderWriterV2`
                stream_reader = FileStream(self._project_pathname, FileMode.Open, FileAccess.Read, FileShare.Read)
                try:
                    self._project = reader.Read(stream_reader)
                finally:
                    stream_reader.Close()
        return self._project


if __name__ == '__main__':
    import doctest
    doctest.testmod()
