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
import traceback

from autotrainz.builders_and_generators.base import Base
from autotrainz.builders_and_generators.builder import Builder
from autotrainz.exceptions.container_build_error import ContainerBuildError
from autotrainz.exceptions.deploy_script_generation_error import DeployScriptGenerationError
from autotrainz.exceptions.flow_build_error import FlowBuildError
from autotrainz.exceptions.flow_validation_error import FlowValidationError
from autotrainz.exceptions.orchestration_artifact_build_error import OrchestrationArtifactBuildError


class Director(Base):

    def __init__(self, **kwargs):
        super().__init__()

        # TODO Validate Builder steps are present

        # TODO This should be hidden in some way - maybe
        self._builder = Builder(**kwargs)

    def build_and_run(self) -> dict:
        """

        Returns:
            run summary as dict

        Raises:
            FlowValidationError

        """
        # ---------------------------- #
        # -------- Initialize -------- #
        # ---------------------------- #
        self._log_start()

        self._builder.build()

        run_summary = dict()

        try:

            self._builder.pipeline.workflow_validator.validate()

            self._builder.pipeline.pipeline_composer.build_part(**self._builder.pipeline.workflow_validator.get_results())

            self._builder.pipeline.packager.build_part(**self._builder.pipeline.pipeline_composer.get_results())

            self._builder.pipeline.deployment_artifact_builder.build_part(**self._builder.pipeline.packager.get_results())

            self._builder.pipeline.deployer.build_part(**self._builder.pipeline.deployment_artifact_builder.get_results())

            print(self._builder.pipeline.deployer.get_results())

        except FlowValidationError:
            raise
        except FlowBuildError:
            raise
        except ContainerBuildError:
            raise
        except OrchestrationArtifactBuildError:
            raise
        except DeployScriptGenerationError:
            raise
        except:
            self._handle_error(traceback.format_exc(), RuntimeError)

        finally:
            self.__log_build_results(log_info=run_summary)
            self._log_stop()
        # TODO: Summary needs to be built
        return run_summary

    def __log_build_results(self, log_info: dict) -> bool:
        pass
