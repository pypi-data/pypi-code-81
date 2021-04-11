from typing import List

from grid.core import Experiment
from grid.core.base import GridObject
from grid.core.task import Task


class Run(GridObject):
    """
    Run object in Grid. Runs are collections of Experiment objects.

    Parameters
    ----------
    identifier: str
        Run name (not Run ID)
    """
    def __init__(self, identifier: str):
        self.identifier = identifier
        super().__init__()

    def refresh(self) -> None:
        """
        Updates object metadata. This makes a query to Grid to fetch the
        object's latest data.
        """
        query = """
        query GetRunDetails ($runName: ID!) {
            getRuns(runName: $runName) {
                runId
                name
                description
                entrypoint
                createdAt
                startedRunningAt
                finishedAt
                clusterId
                nExperiments
                nRunning
                nFailed
                nCompleted
                nCancelled
                nQueued
                nPending
                invocationCommand
                projectId
                config {
                    compute
                }
            }
        }
        """
        result = self.client.execute_gql(query, runName=self.identifier)
        self._data = result["getRuns"][0]
        self._update_meta()

    @property
    def experiments(self) -> List[Experiment]:
        """
        List of experiments for the Run.

        Returns
        -------
        experiments: List[Experiment]
            List of Experiment instances.
        """
        query = """
        query (
                $runName: ID
            ) {
                getExperiments (runName: $runName) {
                    experimentId
                    name
                    commitSha
                    entrypoint
                    invocationCommands
                    createdAt
                    finishedAt
                    startedRunningAt
                    desiredState
                }
            }
        """
        result = self.client.execute_gql(query, runName=self.identifier)

        # Skips the need for the Experiment object to reload
        # data from the backend API.
        experiments = []
        for experiment_data in result.get("getExperiments"):
            E = Experiment(experiment_data.pop("experimentId"))
            E._data = experiment_data
            E._update_meta()
            experiments.append(E)

        return experiments

    @property
    def tasks(self) -> List[Task]:
        query = """
        query (
            $runName: ID!
        ) {
            getRunTaskStatus (
                runName: $runName
            ) {
                dependencies {
                    taskId
                    status
                    taskType
                    message
                    error
                }
            }
        }
        """
        result = self.client.execute_gql(query, runName=self.identifier)
        tasks = result["getRunTaskStatus"]["dependencies"]

        task_objects = []
        for task in tasks:
            dict_task = {self._camel_case_to_snake_case(k): v for k, v in task.items()}
            task_objects.append(Task(**dict_task))

        return task_objects
