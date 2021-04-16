import os
from tests.test_configs.config_helper import load_and_validate, load_config
from pencil_pusher.file_util import FileUtil
from pencil_pusher.documenter import Documenter
from pencil_pusher.github_api import GithubAPI
from pencil_pusher.repo_manager import RepoManager


def test_repo_manager_simple_config():
    """
    Tests running the repo manager with the
    most basic config that can be provided
    """
    load_config(
        sources=["biit_server/"], title_prefix="", title_suffix="", python={}
    )
    load_and_validate()

    Documenter.install()

    owner = "biit-407"
    repo = "biit-server"
    ghapi = GithubAPI(os.environ["GH_PAT"])
    rm = RepoManager(owner, repo, ghapi)

    rm.setup()

    rm.install()

    rm.document(sources=["biit_server/"], extensions=["py"])
    # no publish, just testing

    files_to_check = FileUtil.query_directory(
        "../biit-server/biit_server/", [".py"]
    )
    files_found = FileUtil.query_directory("../biit-server-wiki/", [".md"])

    for fc in files_to_check:
        fc_name = fc[fc.index("biit_server") : -3]
        fc_name = fc_name.replace("/", ".")
        found = False
        for ff in files_found:
            if fc_name in ff:
                found = True
                break
        if fc_name.endswith("__init__") or fc_name.endswith("__main__"):
            continue
        assert found, f"could not find [{fc_name}]"

    rm.cleanup()
