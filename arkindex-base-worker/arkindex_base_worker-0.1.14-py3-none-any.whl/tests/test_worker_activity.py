# -*- coding: utf-8 -*-
import json

import pytest
from apistar.exceptions import ErrorResponse

from arkindex_worker.worker import ActivityState, Element

# Common API calls for all workers
BASE_API_CALLS = [
    "http://testserver/api/v1/user/",
    "http://testserver/api/v1/workers/versions/12341234-1234-1234-1234-123412341234/",
]


def test_defaults(responses, mock_elements_worker):
    """Test the default values from mocked calls"""
    assert not mock_elements_worker.is_read_only
    assert mock_elements_worker.features == {
        "workers_activity": False,
        "signup": False,
    }

    assert len(responses.calls) == 2
    assert [call.request.url for call in responses.calls] == BASE_API_CALLS


def test_feature_disabled(responses, mock_elements_worker):
    """Test disabled calls do not trigger any API calls"""
    assert not mock_elements_worker.is_read_only

    out = mock_elements_worker.update_activity(
        Element({"id": "1234-deadbeef"}), ActivityState.Processed
    )

    assert out is None
    assert len(responses.calls) == 2
    assert [call.request.url for call in responses.calls] == BASE_API_CALLS


def test_readonly(responses, mock_elements_worker):
    """Test readonly worker does not trigger any API calls"""

    # Setup the worker as read-only, but with workers_activity enabled
    mock_elements_worker.worker_version_id = None
    assert mock_elements_worker.is_read_only is True
    mock_elements_worker.features["workers_activity"] = True

    out = mock_elements_worker.update_activity(
        Element({"id": "1234-deadbeef"}), ActivityState.Processed
    )

    assert out is None
    assert len(responses.calls) == 2
    assert [call.request.url for call in responses.calls] == BASE_API_CALLS


def test_update_call(responses, mock_elements_worker):
    """Test an update call with feature enabled triggers an API call"""
    responses.add(
        responses.PUT,
        "http://testserver/api/v1/workers/versions/12341234-1234-1234-1234-123412341234/activity/",
        status=200,
        json={
            "element_id": "1234-deadbeef",
            "state": "processed",
        },
    )

    # Enable worker activity
    mock_elements_worker.features["workers_activity"] = True

    out = mock_elements_worker.update_activity(
        Element({"id": "1234-deadbeef"}), ActivityState.Processed
    )

    # Check the response received by worker
    assert out == {
        "element_id": "1234-deadbeef",
        "state": "processed",
    }

    assert len(responses.calls) == 3
    assert [call.request.url for call in responses.calls] == BASE_API_CALLS + [
        "http://testserver/api/v1/workers/versions/12341234-1234-1234-1234-123412341234/activity/",
    ]

    # Check the request sent by worker
    assert json.loads(responses.calls[2].request.body) == {
        "element_id": "1234-deadbeef",
        "state": "processed",
    }


@pytest.mark.parametrize(
    "process_exception, final_state",
    [
        # Successful process_element
        (None, "processed"),
        # Failures in process_element
        (
            ErrorResponse(title="bad gateway", status_code=502, content="Bad gateway"),
            "error",
        ),
        (ValueError("Something bad"), "error"),
        (Exception("Any error"), "error"),
    ],
)
def test_run(
    monkeypatch, mock_elements_worker, responses, process_exception, final_state
):
    """Check the normal runtime sends 2 API calls to update activity"""
    # Disable second configure call from run()
    monkeypatch.setattr(mock_elements_worker, "configure", lambda: None)

    # Mock elements
    monkeypatch.setattr(
        mock_elements_worker,
        "list_elements",
        lambda: [
            "1234-deadbeef",
        ],
    )
    responses.add(
        responses.GET,
        "http://testserver/api/v1/element/1234-deadbeef/",
        status=200,
        json={
            "id": "1234-deadbeef",
            "type": "page",
            "name": "Test Page n°1",
        },
    )

    # Mock Update activity
    responses.add(
        responses.PUT,
        "http://testserver/api/v1/workers/versions/12341234-1234-1234-1234-123412341234/activity/",
        status=200,
        json={
            "element_id": "1234-deadbeef",
            "state": "started",
        },
    )
    responses.add(
        responses.PUT,
        "http://testserver/api/v1/workers/versions/12341234-1234-1234-1234-123412341234/activity/",
        status=200,
        json={
            "element_id": "1234-deadbeef",
            "state": final_state,
        },
    )

    # Enable worker activity
    assert mock_elements_worker.is_read_only is False
    mock_elements_worker.features["workers_activity"] = True

    # Mock exception in process_element
    if process_exception:

        def _err():
            raise process_exception

        monkeypatch.setattr(mock_elements_worker, "process_element", _err)

        # The worker stops because all elements failed !
        with pytest.raises(SystemExit):
            mock_elements_worker.run()
    else:
        # Simply run the process
        mock_elements_worker.run()

    assert len(responses.calls) == 5
    assert [call.request.url for call in responses.calls] == BASE_API_CALLS + [
        "http://testserver/api/v1/element/1234-deadbeef/",
        "http://testserver/api/v1/workers/versions/12341234-1234-1234-1234-123412341234/activity/",
        "http://testserver/api/v1/workers/versions/12341234-1234-1234-1234-123412341234/activity/",
    ]

    # Check the requests sent by worker
    assert json.loads(responses.calls[3].request.body) == {
        "element_id": "1234-deadbeef",
        "state": "started",
    }
    assert json.loads(responses.calls[4].request.body) == {
        "element_id": "1234-deadbeef",
        "state": final_state,
    }
