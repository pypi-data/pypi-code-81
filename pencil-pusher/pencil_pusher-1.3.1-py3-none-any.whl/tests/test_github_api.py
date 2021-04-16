from pencil_pusher.github_api import GithubAPI
import os
import shutil

REPO = "ghapd"
OWNER = "stephend017"
ROOT_DIR = os.path.dirname(os.path.abspath("./setup.py"))


def test_get_public_file():
    """
    Tests that a public file can be successfully queried from
    a public repository
    """
    file_path = "action.yml"

    contents = GithubAPI.get_public_file(
        OWNER, REPO, file_path, os.environ["GH_PAT"]
    )

    assert 'name: "pencil_pusher"' in contents


def test_clone_repo():
    """
    Tests that a repo can be cloned successfully to a
    local location
    """
    ghapi = GithubAPI(os.environ["GH_PAT"])
    ghapi.clone_repo(OWNER, REPO, "example-repo")
    path = os.path.join(ROOT_DIR, "example-repo")

    assert os.path.exists(path)
    shutil.rmtree(path)


def test_clone_repo_external():
    """
    Tests that a repo can be cloned successfully to a
    local location that is outside of the executing directory

    This is needed so the wiki repo and the source repo can be
    used in tandem without having to deal with git potentially
    interacting with both of them
    """
    ghapi = GithubAPI(os.environ["GH_PAT"])
    ghapi.clone_repo(OWNER, REPO, "../example-repo")
    path = os.path.join(ROOT_DIR, "../example-repo")

    assert os.path.exists(path)
    shutil.rmtree(path)


def test_full_send():
    """
    Tests that a repo can be automatically staged, committed and
    pushed
    """
    ghapi = GithubAPI(os.environ["GH_PAT"])
    ghapi.clone_repo(OWNER, "pencil-pusher.wiki", "../example-repo")
    path = os.path.join(ROOT_DIR, "../example-repo")

    # do a change
    with open(os.path.join(path, "_testing.md"), "a+") as fp:
        fp.write("* testing string \n\n")

    ghapi.full_update(OWNER, "ghapd.wiki", path)

    shutil.rmtree(path)


def test_full_send_relative_path():
    """
    Tests that a repo can be automatically staged, committed and
    pushed from a relative path
    """
    ghapi = GithubAPI(os.environ["GH_PAT"])
    ghapi.clone_repo(OWNER, "pencil-pusher.wiki", "../example-repo")

    # do a change
    with open(os.path.join("../example-repo", "_testing.md"), "a+") as fp:
        fp.write("* testing string from relative \n\n")

    ghapi.full_update(OWNER, "pencil-pusher.wiki", "../example-repo")

    shutil.rmtree("../example-repo")
