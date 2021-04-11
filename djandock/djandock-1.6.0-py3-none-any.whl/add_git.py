import os
from git import Repo

def initialize_repo(name, remote_url):
    """
    Clones the repository
    """
    repo = Repo.clone_from(remote_url, os.path.join(os.getcwd(), name))