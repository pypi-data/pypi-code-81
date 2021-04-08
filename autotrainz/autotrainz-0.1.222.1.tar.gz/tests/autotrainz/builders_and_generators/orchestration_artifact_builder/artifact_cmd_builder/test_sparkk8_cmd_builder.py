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
from autotrainz.builders_and_generators.orchestration_artifact_builder.artifact_cmd_builder.sparkk8_cmd_builder \
    import Sparkk8CmdBuilder
from unittest import TestCase


class TestSparkk8CmdBuilder(TestCase):
    def setUp(self) -> None:
        self.__artifact_cmd = Sparkk8CmdBuilder()

    def tearDown(self) -> None:
        pass

    def test_build_part(self):

        val_in = {
            'cmd_config': {
                'cmd': '$SPARK_HOME/bin/spark-submit',
                'base_path': 'local:///opt/spark/work-dir/app/',
                'parameters': {
                    'master': 'yarn'
                },
                'conf': {
                    'spark.kubernetes.namespace': 'airflow'}
            },
            'repo_tagged_docker_image_name': 'image_name',
            'fit': 'script.py'
        }

        val_out = "$SPARK_HOME/bin/spark-submit  --master yarn  --conf spark.kubernetes.namespace=airflow  --conf " \
                  "spark.kubernetes.container.image=image_name local:///opt/spark/work-dir/app/script.py"
        self.assertEqual(self.__artifact_cmd._build_part(**val_in), val_out)
