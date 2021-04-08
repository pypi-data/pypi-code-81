# Copyright 2021 EMBL - European Bioinformatics Institute
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from ebi_eva_common_pyutils.logger import AppLogger


class NextFlowProcess:

    def __init__(self, process_name, command_to_run, additional_params=None,dependencies=None):
        self.process_name = process_name
        self.success_flag = f"{self.process_name}_success"
        self.command_to_run = command_to_run
        self.additional_params = additional_params if additional_params else {}
        self.dependencies = dependencies if dependencies else []

    def add_process_params(self, additional_params):
        self.additional_params.update(additional_params)

    def depends_on(self, *other):
        self.dependencies.extend(list(other))

    def __str__(self):
        additional_params_str = "\n".join([f"{key}='{value}'" for key, value in self.additional_params.items()])
        input_dependencies = "val flag from true"
        if self.dependencies:
            input_dependencies = "\n".join([f"val {dependency.success_flag} from {dependency.success_flag}"
                                            for dependency in self.dependencies])
        return "\n".join(map(str.strip, f"""
            process {self.process_name} {{
            {additional_params_str}
            input:
            {input_dependencies}
            output:
            val true into {self.success_flag}
            script:
            \"\"\"
            {self.command_to_run}
            \"\"\"
            }}""".split("\n")))


class NextFlowPipeline(AppLogger):
    def __init__(self, workflow_file_path, nextflow_binary_path='nextflow',
                 nextflow_config_path=None, working_dir=".", process_list=None):
        self.workflow_file_path = workflow_file_path
        self.nextflow_binary_path = nextflow_binary_path
        self.nextflow_config_path = nextflow_config_path
        self.working_dir = working_dir
        # Remove pipeline file if it already exists
        if os.path.exists(workflow_file_path):
            os.remove(self.workflow_file_path)
        self.process_list = process_list if process_list else []

    def add_process(self, process: NextFlowProcess):
        self.process_list.append(process)

    def run_pipeline(self, resume=False, other_args=None):
        self._write_to_pipeline_file(self.__str__())
        workflow_command = f"cd {self.working_dir} && {self.nextflow_binary_path} run {self.workflow_file_path}"
        workflow_command += f" -c {self.nextflow_config_path}" if self.nextflow_config_path else ""
        workflow_command += f" -with-report {self.workflow_file_path}.report.html"
        workflow_command += f" -with-dag {self.workflow_file_path}.dag.png"
        workflow_command += " -resume" if resume else ""
        workflow_command += " ".join([f" -{arg} {val}" for arg, val in other_args.items()]) if other_args else ""
        os.system(workflow_command)

    def _write_to_pipeline_file(self, content):
        with open(self.workflow_file_path, "a") as pipeline_file_handle:
            pipeline_file_handle.write(content + "\n")

    def __str__(self):
        return "\n\n".join(map(str, self.process_list))
