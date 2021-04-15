from unittest.mock import patch

import pytest
from sym.cli.errors import CliError
from sym.cli.helpers.contexts import push_env

from sym.flow.cli.commands.connectors.slack.slack_new import get_magic_url, slack_new
from sym.flow.cli.errors import NotAuthorizedError, SymAPIUnknownError
from sym.flow.cli.symflow import symflow as click_command
from sym.flow.cli.tests.conftest import get_mock_response


class TestSlackConnectorNew:
    """Suite for testing Slack installation."""

    @patch("sym.flow.cli.commands.connectors.slack.slack_new.webbrowser.open")
    @patch(
        "sym.flow.cli.commands.connectors.slack.slack_new.click.confirm",
        return_value=True,
    )
    @patch(
        "sym.flow.cli.commands.connectors.slack.slack_new.get_magic_url",
        return_value="http://fake-test.symops.com",
    )
    def test_click_command_browser(
        self, mock_get_magic_url, mock_click_confirm, mock_webbrowser_open, click_setup
    ):
        with click_setup() as runner:
            result = runner.invoke(click_command, ["connectors", "slack", "new"])
            assert result.exit_code == 0
            assert "http://fake-test.symops.com" in str(result.stdout_bytes, "utf-8")

            mock_get_magic_url.assert_called_once_with(
                api_url="https://api.symops.com/api/v1"
            )
            mock_click_confirm.assert_called_once()
            mock_webbrowser_open.assert_called_once_with("http://fake-test.symops.com")

    @patch("sym.flow.cli.commands.connectors.slack.slack_new.webbrowser.open")
    @patch(
        "sym.flow.cli.commands.connectors.slack.slack_new.click.confirm",
        return_value=False,
    )
    @patch(
        "sym.flow.cli.commands.connectors.slack.slack_new.get_magic_url",
        return_value="http://fake-test.symops.com",
    )
    def test_click_command_no_browser(
        self, mock_get_magic_url, mock_click_confirm, mock_webbrowser_open, click_setup
    ):
        with click_setup() as runner:
            result = runner.invoke(click_command, ["connectors", "slack", "new"])
            assert result.exit_code == 0
            assert "http://fake-test.symops.com" in str(result.stdout_bytes, "utf-8")

            mock_get_magic_url.assert_called_once_with(
                api_url="https://api.symops.com/api/v1"
            )
            mock_click_confirm.assert_called_once()
            mock_webbrowser_open.assert_not_called()

    @patch(
        "sym.flow.cli.commands.connectors.slack.slack_new.get_magic_url",
        side_effect=ValueError("random error"),
    )
    def test_click_call_catches_unknown_error(self, mock_get_magic_url, click_setup):
        with click_setup() as runner:
            result = runner.invoke(click_command, ["connectors", "slack", "new"])
            assert result.exit_code == 1
            assert isinstance(result.exception, ValueError)
            assert str(result.exception) == "random error"

        mock_get_magic_url.assert_called_once_with(
            api_url="https://api.symops.com/api/v1"
        )

    def test_initialize_slack_install_not_authorized_fails(self, sandbox):
        with pytest.raises(NotAuthorizedError, match="symflow login"):
            with sandbox.push_xdg_config_home():
                get_magic_url("http://afakeurl.symops.io/")

    @patch(
        "sym.flow.cli.helpers.sym_api_client.SymAPIClient.get",
        return_value=(
            get_mock_response(200, data={"url": "http://test.symops.io"}),
            "test-request-id",
        ),
    )
    def test_get_magic_url(self, mock_api_get, sandbox):
        with sandbox.push_xdg_config_home():
            assert get_magic_url("http://afakeurl.symops.io/") == "http://test.symops.io"

        mock_api_get.assert_called_once()
