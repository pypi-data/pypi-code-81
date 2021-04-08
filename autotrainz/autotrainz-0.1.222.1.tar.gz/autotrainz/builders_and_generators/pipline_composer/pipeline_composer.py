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
from autotrainz.builders_and_generators.build_step import BuildStep
from autotrainz.exceptions.flow_build_error import FlowBuildError


class PipelineComposer(BuildStep):

    def __init__(self, **kwargs):
        super().__init__()
        self._pipelines: list = []

    def build_part(self, **kwargs):
        self._log_start()
        _res = self._build(flows=kwargs.get("workflows"))
        self._log_stop()
        if not _res:
            raise FlowBuildError()

    def get_results(self):
        self._log_start()
        result = dict()
        if self._pipelines:
            result = {
                "pipelines": self._pipelines
            }
        self._log_stop()
        return result

    def _build(self, flows: dict) -> bool:
        raise NotImplementedError(f'Method not implemented for {type(self).__name__}.')
