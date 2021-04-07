#!/usr/bin/env python3
import requests
from typing import Optional, Dict, Any
from codoc.domain.model import Graph
import logging

logger = logging.getLogger(__name__)
BASE_URL = "https://api.codoc.org/"
PUBLISH_URL = f"{BASE_URL}graphs/"
# TODO use better path


def publish(
    graph_id: str,
    label: str,
    description: str,
    api_key: str,
    graph: Graph,
    commit_hash: str = "",
) -> str:
    """
    Used to upload a given graph to the web application

    Returns the url that the created graph is accessed at.
    """
    if not api_key:
        raise ApiKeyNotSupplied()

    payload = _get_payload(
        graph=graph,
        graph_id=graph_id,
        label=label,
        description=description,
        commit_hash=commit_hash,
    )
    headers = _get_headers(api_key)

    resp = requests.post(
        url=PUBLISH_URL,
        json=payload,
        headers=headers,
    )

    if not resp.ok:
        raise PublishFailed(graph_id, resp.text)

    # TODO should return a URL.
    ressource = resp.json()["pk"]
    return ressource


def _get_payload(
    graph_id: str,
    label: str,
    description: str,
    graph: Graph,
    commit_hash: Optional[str] = None,
) -> Dict[str, Any]:
    return {
        "label": label,
        "graph_id": graph_id,
        "description": description,
        "commit_hash": commit_hash,
        "nodes": [
            {
                "name": node.name,
                "identifier": node.identifier,
                "description": node.description,
                "of_type": node.of_type.name,
                "parent_node": node.parent_identifier,
                # TODO add parent, path, args etc
            }
            for node in graph.nodes
        ],
        "edges": [
            {"from_node": edge.from_node, "to_node": edge.to_node}
            for edge in graph.edges
        ],
    }


def _get_headers(api_key: str) -> Dict[str, str]:
    return {
        "Authorization": _get_auth_header(api_key),
        "Content-Type": "application/json",
    }


def _get_auth_header(api_key: str) -> str:
    return f"OrgToken {api_key}"


class ExportError(Exception):
    ...


class ApiKeyNotSupplied(ExportError):
    ...


class PublishFailed(ExportError):
    def __init__(self, graph_id: str, resp: str):
        super().__init__(f"Publishing of {graph_id} failed.\nReason={resp}")

    ...
