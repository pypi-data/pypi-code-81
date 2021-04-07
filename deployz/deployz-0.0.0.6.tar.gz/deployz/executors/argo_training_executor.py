# Copyright © 2021 Hashmap, Inc
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
import subprocess
import os

from deployz.executors.training_executor import TrainingExecutor


class ArgoTrainingExecutor(TrainingExecutor):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__namespace = kwargs.get('namespace')

    def run(self, artifact: str, version: int = None, **kwargs):
        execution_file = os.path.join(os.getcwd(), artifact + '.yml')
        self._registry.retrieve_to(name=artifact,
                                   copy_to=execution_file,
                                   version=version)

        return subprocess.run(['argo', 'submit', '-n', self.__namespace, execution_file], check=True, stderr=subprocess.STDOUT)
