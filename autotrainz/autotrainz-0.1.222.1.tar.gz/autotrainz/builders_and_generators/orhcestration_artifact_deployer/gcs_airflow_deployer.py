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
import subprocess
import traceback
from autotrainz.builders_and_generators.orhcestration_artifact_deployer.airflow_deployer import AirflowDeployer


class GCSAirflowDeployer(AirflowDeployer):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _deploy(self, artifact):

        try:
            self._log_start()
            result = subprocess.run(['gsutil', 'cp', artifact, self._path], check=True, stderr=subprocess.STDOUT)

            if result.stderr:
                error_message = f'Standard Error: {result.stderr}'
                self._handle_error(error_message, RuntimeError)
            self._log_stop()
        except:
            self._handle_error(traceback.format_exc(), RuntimeError)
