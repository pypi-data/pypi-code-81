from typing import Dict, List, Optional

from grid.core.artifact import Artifact
from grid.core.base import GridObject


class Experiment(GridObject):
    """
    Grid experiment object. This object contains all the properties that a
    given artifact should have. This also encapsulates special methods
    for interactive with experiment properties.

    Parameters
    ----------
    name: str
        Experiment name
    """
    def __init__(self, name: str):
        self._data: Optional[Dict[str, str]] = {}
        self.name = name
        self.identifier = None
        super().__init__()

    def refresh(self) -> None:
        """
        Updates object metadata. This makes a query to Grid to fetch the
        object's latest data.
        """
        self.identifier = self.client.get_experiment_id(self.name)

        query = """
        query GetExperimentDetails ($experimentId: ID!) {
            getExperimentDetails(experimentId: $experimentId) {
                name
                githubId
                desiredState
                commitSha
                entrypoint
                invocationCommands
                createdAt
                startedRunningAt
                finishedAt
                parameters {
                    name
                    value
                }
            }
        }
        """
        result = self.client.execute_gql(query, experimentId=self.identifier)
        self._data = result["getExperimentDetails"]
        self._update_meta()

    @property
    def status(self):
        query = """
        query GetExperimentDetails ($experimentId: ID!) {
            getExperimentDetails(experimentId: $experimentId) {
                status
            }
        }
        """
        result = self.client.execute_gql(query, experimentId=self.identifier)
        return result["getExperimentDetails"]["status"]

    @property
    def artifacts(self) -> List[Dict[str, str]]:
        """Fetches artifacts from a given experiments. Artifacts are"""
        query = """
        query (
            $experimentId: ID!
        ) {
            getArtifacts(experimentId: $experimentId) {
                signedUrl
                downloadToPath
                downloadToFilename
            }
        }
        """
        result = self.client.execute_gql(query, experimentId=self.identifier)
        return [Artifact(*a.values()) for a in result.get("getArtifacts")]
