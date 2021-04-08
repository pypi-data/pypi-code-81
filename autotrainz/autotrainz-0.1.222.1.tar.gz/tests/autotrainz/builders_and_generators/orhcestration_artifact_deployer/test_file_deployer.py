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
import unittest
from unittest import TestCase
from autotrainz.builders_and_generators.orhcestration_artifact_deployer.file_deployer import FileDeployer
import os
import subprocess


class TestFileDeployer(TestCase):

    def setUp(self) -> None:
        config = {
            'registry': {
                'type': 'FileRegistry',
                'conf': {
                    'path': ''
                }
            }
        }
        self.__file_dep = FileDeployer(**config)

    def tearDown(self) -> None:
        pass

    @unittest.skip('This test is broken - buggy')
    def test_run(self):
        path = os.path.abspath('./tests/autotrainz/')
        result = subprocess.run(["chmod", "+x", path+'/test_manifest.sh'], check=True, stderr=subprocess.STDOUT)
        self.assertTrue(self.__file_dep._run(path+'/test_manifest.sh'))
