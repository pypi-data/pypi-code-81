from datetime import datetime
from typing import Dict, List, Optional, Tuple

import pytest

from sym.flow.cli.errors import SymAPIRequestError, UnknownOrgError
from sym.flow.cli.helpers.sym_api_client import BaseSymAPIClient
from sym.flow.cli.helpers.sym_api_service import ConnectorType, SymAPIService

MOCK_INTEGRATIONS_DATA = [
    {
        "slug": "integration 1",
        "type": "aws",
        "updated_at": datetime(2021, 1, 19, hour=14, minute=23),
    },
    {
        "slug": "integration 2",
        "type": "aws_sso",
        "updated_at": datetime(2021, 1, 19, hour=15, minute=23),
    },
]

MOCK_INTEGRATIONS_BAD_DATA = [
    {"name": "integration 1", "updated_at": datetime.now()},
    {"type": "aws-sso", "updated_at": datetime.now()},
]

MOCK_SLACK_CONNECTOR_DATA = [
    {
        "type_name": "slack",
        "settings": {"team_name": "connector 1", "team_id": "T1234567"},
    },
    {
        "type_name": "slack",
        "settings": {"team_name": "connector 2", "team_id": "T7654321"},
    },
]


class MockGoodSymAPIClient(BaseSymAPIClient):
    """This instance of a BaseSymAPIClient is intended to be
    used with SymAPIService to mock successful behaviors
    """

    def get_integrations(self) -> Tuple[List[dict], str]:
        return MOCK_INTEGRATIONS_DATA, "test-request-id"

    def get_connectors(self, type_name: Optional[str] = None) -> Tuple[List[dict], str]:
        if type_name == ConnectorType.SLACK.value:
            return MOCK_SLACK_CONNECTOR_DATA, "test-request-id"
        raise ValueError("Unknown connector type")

    def set_access_token(self, access_token: str):
        pass

    def get_organization_from_email(self, email: str):
        return {"slug": "test", "client_id": "12345abc"}, "test-request-id"

    def verify_login(self, email: str):
        return 200, "test-request-id"

    def patch_users(self, csv_data: str) -> Tuple[List[Dict[str, str]], str]:
        return [{"email": "test", "identities": []}], "test-request-id"


class MockBadSymAPIClient(BaseSymAPIClient):
    """This instance of a BaseSymAPIClient is intended to be
    used with SymAPIService to mock failure scenarios.
    """

    def get_integrations(self) -> Tuple[List[dict], str]:
        return MOCK_INTEGRATIONS_BAD_DATA, "test-request-id"

    def get_connectors(self, type_name: Optional[str] = None) -> Tuple[List[dict], str]:
        return [{}], "test-request-id"

    def set_access_token(self, access_token: str):
        pass

    def get_organization_from_email(self, email: str):
        return {}, "test-request-id"

    def verify_login(self, email: str):
        return 400, "test-request-id"

    def patch_users(self, csv_data: str) -> Tuple[List[Dict[str, str]], str]:
        return [{"email": "test"}], "test-request-id"


class TestSymAPIService:
    def test_get_integration_table_data_success(self):
        service = SymAPIService(api_client=MockGoodSymAPIClient())
        data = service.get_integration_table_data()

        assert data == [
            ["integration 1", "aws", "19 Jan 2021 02:23PM"],
            ["integration 2", "aws_sso", "19 Jan 2021 03:23PM"],
        ]

    def test_get_integration_table_data_failure(self):
        service = SymAPIService(api_client=MockBadSymAPIClient())

        with pytest.raises(SymAPIRequestError) as exc_info:
            service.get_integration_table_data()

        assert "Request ID (test-request-id)" in str(exc_info.value)
        assert "https://docs.symops.com/docs/support" in str(exc_info.value)

    def test_get_slack_connector_table_data_success(self):
        service = SymAPIService(api_client=MockGoodSymAPIClient())
        data = service.get_slack_connectors_table_data()

        assert data == [
            ["connector 1", "T1234567"],
            ["connector 2", "T7654321"],
        ]

    def test_get_slack_connector_table_data_failure(self):
        service = SymAPIService(api_client=MockBadSymAPIClient())

        with pytest.raises(SymAPIRequestError) as exc_info:
            service.get_slack_connectors_table_data()

        assert "Request ID (test-request-id)" in str(exc_info.value)
        assert "https://docs.symops.com/docs/support" in str(exc_info.value)

    def test_get_organization_from_email_missing_data_errors(self):
        service = SymAPIService(api_client=MockBadSymAPIClient())

        with pytest.raises(UnknownOrgError):
            service.get_organization_from_email("test@symops.io")

    def test_verify_login_failure(self):
        service = SymAPIService(api_client=MockBadSymAPIClient())
        assert service.verify_login("test@symops.io") is False

    def test_verify_login_success(self):
        service = SymAPIService(api_client=MockGoodSymAPIClient())
        assert service.verify_login("test@symops.io") is True
