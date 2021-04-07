# (C) Copyright IBM Corp. 2020.
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

import logging

from ibm_watson_machine_learning.libs.repo.mlrepository import  WmlExperimentArtifact
from ibm_watson_machine_learning.libs.repo.mlrepository import MetaNames, MetaProps

from ibm_watson_machine_learning.libs.repo.util.library_imports import LibraryChecker

lib_checker = LibraryChecker()

logger = logging.getLogger('WmlExperimentCollectionAdapter')


class WmlExperimentCollectionAdapter(object):
    """
    Adapter creating experiment artifact using output from service.
    """

    def __init__(self, experiment_output, client):

        self.experiment_output = experiment_output
        self.client = client
        self.experiment_entity = experiment_output.entity
        self.experiment_metadata = experiment_output.metadata

    def artifact(self):
        experiement_artifact_builder = type(
                "ExperimentArtifact",
                (WmlExperimentArtifact, object),
                {}
            )

        prop_map = {
            MetaNames.CREATION_TIME: self.experiment_metadata.created_at,
            MetaNames.LAST_UPDATED: self.experiment_metadata.modified_at,
            MetaNames.EXPERIMENT_URL : self.experiment_metadata.url
        }

        if self.experiment_entity.settings is not None:
            prop_map[MetaNames.EXPERIMENTS.SETTINGS] = self.experiment_entity.settings


        if self.experiment_entity.tags is not None:
            prop_map[MetaNames.EXPERIMENTS.TAGS] = self.experiment_entity.tags


        if self.experiment_entity.training_data_reference is not None:
            prop_map[MetaNames.EXPERIMENTS.TRAINING_DATA_REFERENCE] = self.experiment_entity.training_data_reference

        if self.experiment_entity.training_references is not None:
            prop_map[MetaNames.EXPERIMENTS.TRAINING_REFERENCES] = self.experiment_entity.training_references

        if self.experiment_entity.training_results_reference is not None:
            prop_map[MetaNames.EXPERIMENTS.TRAINING_RESULTS_REFERENCE] = self.experiment_entity.training_results_reference


        name = None
        experiment_url = self.experiment_metadata.url
        experiment_id = experiment_url.split("/experiments/")[1].split("/")[0]


        experiment_artifact = experiement_artifact_builder(
            experiment_id,
            name,
            MetaProps(prop_map)
        )

        experiment_artifact.client = self.client


        return experiment_artifact
