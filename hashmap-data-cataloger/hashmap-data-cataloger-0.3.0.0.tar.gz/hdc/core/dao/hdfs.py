#  Copyright © 2020 Hashmap, Inc
#  #
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  #
#      http://www.apache.org/licenses/LICENSE-2.0
#  #
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from hdc.core.dao.filesystem_dao import FileSystemDAO


class Hdfs(FileSystemDAO):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__logger = self._get_logger()

    def get_directory_listing(self, dir_path, format) -> list:
        try:
            import subprocess as sp
            import re

            proc1 = sp.run(['hadoop', 'fs', '-ls', '-R', dir_path], stdout=sp.PIPE)
            file_mask = re.compile(f"{dir_path}/.*{format}")
            return [match.group() for match in re.finditer(file_mask, proc1.stdout.decode())]
        except:
            raise

        return None
