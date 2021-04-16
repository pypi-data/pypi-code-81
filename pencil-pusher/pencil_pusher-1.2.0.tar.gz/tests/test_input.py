from unittest import mock
from pencil_pusher.input import InputManager
import os


@mock.patch(
    "pencil_pusher.input.environ",
    {
        "GITHUB_REPOSITORY": "o_n/r_n",
        "INPUT_GITHUB_TOKEN": "gh_t",
        "INPUT_CONFIG_FILE": "c_f",
    },
)
def test_input_manager():
    """
    Validates that this method is working correctly
    """
    im = InputManager()
    im.define(os.environ["GH_PAT"])

    assert im.validate()

    # these are provided by the github action
    assert im.get("owner_name") == "o_n"
    assert im.get("repository_name") == "r_n"

    assert im.get("github_token") == "gh_t"
    assert im.get("config_file") == "c_f"
