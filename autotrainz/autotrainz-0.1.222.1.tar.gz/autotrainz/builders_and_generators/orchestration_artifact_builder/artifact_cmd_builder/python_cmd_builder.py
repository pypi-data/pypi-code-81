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
from autotrainz.builders_and_generators.orchestration_artifact_builder.artifact_cmd_builder.artifact_cmd_builder import ArtifactCmdBuilder


class PythonCmdBuilder(ArtifactCmdBuilder):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _build_part(self, **task):
        cmd_conf = task.get('cmd_config')
        params = [cmd_conf.get('cmd'), task.get("fit").replace("\\", "\\\\")]
        return " ".join(params)
