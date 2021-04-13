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

from collections import OrderedDict
import os
from functools import reduce
from typing import List, Union

from ebi_eva_common_pyutils.logger import AppLogger


class NextFlowProcess:

    def __init__(self, process_name: str, command_to_run: str, process_directives: dict = None,
                 dependencies: List['NextFlowProcess'] = None):
        self.process_name = process_name
        self.success_flag = f"{self.process_name}_success"
        self.command_to_run = command_to_run
        self.process_directives = process_directives if process_directives else {}
        self.dependencies = dependencies if dependencies else []

    def _add_dependency(self, dependencies):
        new_set_of_dependencies = []
        for dependency in dependencies:
            if dependency not in self.dependencies and dependency.process_name != self.process_name:
                new_set_of_dependencies.append(dependency)
        return NextFlowProcess(process_name=self.process_name, command_to_run=self.command_to_run,
                               process_directives=self.process_directives,
                               dependencies=self.dependencies + new_set_of_dependencies)

    def __and__(self, other: Union['NextFlowPipeline', 'NextFlowProcess']):
        if isinstance(other, NextFlowPipeline):
            return NextFlowPipeline(process_list=[self]) & other
        else:
            if self.process_name == other.process_name:
                return self
            else:
                return NextFlowPipeline(process_list=[self, other])

    def __or__(self, other: Union['NextFlowPipeline', 'NextFlowProcess']):
        if isinstance(other, NextFlowPipeline):
            return NextFlowPipeline(process_list=[self]) | other
        else:
            if self.process_name == other.process_name:
                return self
            else:
                return NextFlowPipeline(process_list=[self, other.depends_on(self)])

    def depends_on(self, *other: 'NextFlowProcess'):
        return self._add_dependency(list(other))

    def __str__(self):
        process_directives_str = "\n".join([f"{key}='{value}'" for key, value in self.process_directives.items()])
        input_dependencies = "val flag from true"
        if self.dependencies:
            input_dependencies = "\n".join([f"val {dependency.success_flag} from {dependency.success_flag}"
                                            for dependency in self.dependencies])
        return "\n".join(map(str.strip, f"""
            process {self.process_name} {{
            {process_directives_str}
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
    def __init__(self, process_list: List[NextFlowProcess] = None):
        self.process_list = OrderedDict((proc.process_name, proc)
                                        for proc in process_list) if process_list else OrderedDict()

    def _has_process(self, process: NextFlowProcess):
        return process.process_name in self.process_list

    def __and__(self, other: Union['NextFlowPipeline', NextFlowProcess]):
        other_pipeline = other
        if isinstance(other, NextFlowProcess):
            other_pipeline = NextFlowPipeline(process_list=[other])
        return NextFlowPipeline(process_list=list(self.process_list.values()) +
                                             list(other_pipeline.process_list.values()))

    def __or__(self, other: Union['NextFlowPipeline', NextFlowProcess]):
        other_pipeline = other
        if isinstance(other, NextFlowProcess):
            other_pipeline = NextFlowPipeline(process_list=[other])
        return other_pipeline.depends_on(self)

    def depends_on(self, *other_pipelines: 'NextFlowPipeline'):
        other_pipeline_processes = reduce(list.__add__,
                                          [list(pipeline.process_list.values()) for pipeline in list(other_pipelines)])
        # This is more of a nicety
        # ex: pipeline2 with processes p3,p4 - depends on - pipeline1 with processes p1,p2
        # having p1 and p2 prepended before the object's process list p3 and p4 is nicer
        processes_with_updated_dependencies = []
        for this_pipeline_process in self.process_list.values():
            processes_with_updated_dependencies.append(this_pipeline_process.depends_on(*other_pipeline_processes))
        return NextFlowPipeline(process_list=(other_pipeline_processes +  processes_with_updated_dependencies))

    def run_pipeline(self, workflow_file_path: str, nextflow_binary_path: str = 'nextflow',
                     nextflow_config_path: str = None, working_dir: str = ".", resume: bool = False,
                     other_args: dict = None):
        # Remove pipeline file if it already exists
        if os.path.exists(workflow_file_path):
            os.remove(workflow_file_path)
        self._write_to_pipeline_file(workflow_file_path)
        workflow_command = f"cd {working_dir} && {nextflow_binary_path} run {workflow_file_path}"
        workflow_command += f" -c {nextflow_config_path}" if nextflow_config_path else ""
        workflow_command += f" -with-report {workflow_file_path}.report.html"
        workflow_command += f" -with-dag {workflow_file_path}.dag.png"
        workflow_command += " -resume" if resume else ""
        workflow_command += " ".join([f" -{arg} {val}" for arg, val in other_args.items()]) if other_args else ""
        os.system(workflow_command)

    def _write_to_pipeline_file(self, workflow_file_path: str):
        with open(workflow_file_path, "a") as pipeline_file_handle:
            pipeline_file_handle.write(self.__str__() + "\n")

    def __str__(self):
        return "\n\n".join(map(str, self.process_list.values()))


class LinearNextFlowPipeline(NextFlowPipeline):
    """
    Simple linear pipeline that supports resumption
    """
    def __init__(self, process_list: List[NextFlowProcess] = None):
        super().__init__(process_list)

    def add_process(self, process_name, command_to_run, memory_in_gb=4):
        current_process = NextFlowProcess(process_name=process_name, command_to_run=command_to_run,
                                          process_directives={"memory_in_gb": memory_in_gb})
        return self | current_process
