import logging
from typing import List, Optional

import annotell.input_api.model.input as InputModel
from annotell.input_api.util import filter_none
from annotell.input_api.resources.abstract import InputAPIResource

log = logging.getLogger(__name__)


class InputResource(InputAPIResource):
    """
    Class exposing Annotell Inputs
    """

    def invalidate_inputs(
        self,
        input_uuids: List[str],
        invalidated_reason: InputModel.InvalidatedReasonInput
    ) -> None:
        """
        Invalidates inputs, and removes them from all input lists

        :param input_uuids: The input uuids to invalidate
        :param invalidated_reason: An Enum describing why inputs were invalidated
        """
        invalidated_json = dict(inputIds=input_uuids, invalidatedReason=invalidated_reason)
        self._client.post("v1/inputs/actions/invalidate", json=invalidated_json)

    def get_inputs(
        self,
        project: str,
        batch: Optional[str] = None,
        include_invalidated: bool = False,
        external_ids: Optional[List[str]] = None
    ) -> List[InputModel.Input]:
        """
        Gets inputs for project, with option to filter for invalidated inputs

        :param project: Project (identifier) to filter
        :param batch: Batch (identifier) to filter
        :param invalidated: Returns invalidated inputs if True, otherwise valid inputs
        :param external_id: External ID to filter input on
        :return List: List of Inputs
        """

        external_id_query_param = ",".join(external_ids) if external_ids else None
        json_resp = self._client.get("v1/inputs", params=filter_none({
            "project": project,
            "batch": batch,
            "invalidated": include_invalidated,
            "externalIds": external_id_query_param
        }))
        return [InputModel.Input.from_json(js) for js in json_resp]
