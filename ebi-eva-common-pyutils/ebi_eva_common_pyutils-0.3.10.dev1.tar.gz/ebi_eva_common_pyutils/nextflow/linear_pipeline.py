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
from ebi_eva_common_pyutils.nextflow import NextFlowProcess, NextFlowPipeline


class LinearNextFlowPipeline(NextFlowPipeline):
    """
    Simple linear pipeline that supports resumption
    """
    def __init__(self, workflow_file_path, process_list=None, nextflow_binary_path='nextflow', nextflow_config_path=None, working_dir="."):
        super().__init__(workflow_file_path, process_list, nextflow_binary_path, nextflow_config_path, working_dir)
        self.previous_process = None

    def add_process(self, process_name, command_to_run, memory_in_gb=4):
        current_process = NextFlowProcess(process_name=process_name, command_to_run=command_to_run)
        if self.previous_process:
            current_process.depends_on(self.previous_process)
        super().add_process(current_process)
        self.previous_process = current_process
