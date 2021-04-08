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

from autotrainz.builders_and_generators.orchestration_artifact_builder.artifact_cmd_builder.artifact_cmd_builder import \
    ArtifactCmdBuilder
from unittest import TestCase


class TestArtifactCmdBuilder(TestCase):
    def setUp(self) -> None:
        self.__artifact_cmd = ArtifactCmdBuilder()

    def tearDown(self) -> None:
        pass

    def test_build_part(self):
        val_in = dict()
        with self.assertRaises(NotImplementedError):
            self.__artifact_cmd._build_part(**val_in)

    def test_build(self):
        val_in = dict()
        with self.assertRaises(NotImplementedError):
            self.__artifact_cmd.build(**val_in)
