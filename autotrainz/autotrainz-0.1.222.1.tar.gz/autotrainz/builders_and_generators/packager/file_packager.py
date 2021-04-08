# Copyright © 2020 Hashmap, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import traceback

from autotrainz.builders_and_generators.packager.packager import Packager
from autotrainz.exceptions.packager_error import PackagerError
from autotrainz.utilities.parser.config_parser import ConfigParser
from autotrainz.utilities.parser.cmd_config_parser import CmdConfigParser


class FilePackager(Packager):

    # ---------------------------------------- #
    # ------------- Construction ------------- #
    # ---------------------------------------- #

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__root_path: str = os.path.abspath(kwargs.get('project_path'))
        self.__workflows_path: str = os.path.join(kwargs.get('project_path'), 'workflows')

        self._workflows: list = list()
        self._pacified_tasks: list = list()
        self._file_list = []
        config_parser = ConfigParser()
        config_parser.parse()
        __cmd_config_obj = CmdConfigParser()
        __cmd_config_obj.parse()
        self.__cmd_config = __cmd_config_obj.configuration()

    def build_part(self, **kwargs):

        try:
            self._log_start()
            if 'pipelines' not in kwargs.keys():
                error_message = f"In {__name__}.build_part 'pipelines' was not found in build_part. " \
                                f"The parameters passed were: {' - '.join(kwargs.keys())}."
                raise ValueError(error_message)

            self._build(pipelines=kwargs.get("pipelines"))
            self._log_stop()
        except:
            self._handle_error(traceback.format_exc(), RuntimeError)

    def _build(self, pipelines: list) -> None:
        self._log_start()
        self._workflows = []
        for pipeline in pipelines:
            updated_pipes: list = list()
            while len(pipeline['workflow']) > 0:
                for pipe in pipeline['workflow']:
                    _res = self.__build_file(pipe=pipe)
                    if _res['successful']:
                        # Update dependencies pacified
                        self._pacified_tasks.append(pipe['stage_name'])
                        # Make a copy of the new pipes
                        updated_pipes.append(pipe)
                        # Remove old pipe
                        pipeline['workflow'].remove(pipe)

            self._build_flows.append(
                {
                    'name': pipeline['name'],
                    'workflow': self._file_list
                }
            )
            self._log_stop()

    def __build_file(self, pipe: dict) -> dict:
        self._log_start()
        if pipe.get("cmd_type"):
            pipe.update(self.__cmd_config[pipe["cmd_type"]])

        if os.path.exists(self.__root_path):
            for root, dirs, files in os.walk(self.__root_path):
                for file in files:
                    selected_file = os.path.join(root, file)
                    self._file_list.append(selected_file)

            self._logger.info('File list built.')
            try:

                return dict(
                    successful=True
                )

            except:
                self._handle_error(traceback.format_exc(), PackagerError)
        else:
            self._handle_error(f"File {self.__root_path} does not exist", RuntimeError)
        self._log_stop()

    def __are_dependencies_pacified(self, dependencies: list) -> bool:
        return len([1 for dependency in dependencies if dependency in self._pacified_tasks]) == len(dependencies)
