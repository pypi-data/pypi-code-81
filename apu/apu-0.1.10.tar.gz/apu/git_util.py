""" my git utils
https://gist.github.com/zosimos/228ac374c4d52f61374c186199799a74
"""

import os
from git import Repo

# pylint: disable=C0301

class GitUtil:
    """  git utils helps working with git in python

    Examples:
    ..  example_code::
        >>> from apu.git_util import GitUtil

        >>> git = GitUtils(
        ...        repo="local_repo",
        ...        path="/home/path/to/local/repo/"
        ...        )
        >>> git.short_hash()
        'e648'
        >>> git.hash
        'e6481c4d3d06b872cc677faaf38e766a4f8a6652'
        >>> git.short_hash(num=16)
        'e6481c4d3d06b872'
    """

    def __init__(self,
                repo: str,
                user: dict=None,
                path: str='',
                refresh:bool=False):
        """  git utils helps working with git in python

        Arguments:
            repo: string
                name of the repository or ssh path
            user : dict, optional
                Git user information. You must provide `ssh` script path, Git user `name` and `email` with dictionary format, e.g:
                {
                    'ssh': '/home/path/to/ssh',
                    'name': 'anonymous',
                    'email': 'anonymous@example.com',
                }

        path : str, optional
            The path where you would like tho checkout your repository or the local repo.
            If you didn't specify this value, it will based on your current working directory.

            **Make sure that's an empty folder for `git clone`**

        refresh : bool, optional
            If true the local repo will get an pull request for origin in the master branch

        Examples:
        ..  example_code::
            >>> from apu.git_util import GitUtil

            >>> git = GitUtils(
            ...        repo="local_repo",
            ...        user={
                            'ssh': '/home/path/to/ssh',
                            'name': 'anonymous',
                            'email': 'anonymous@example.com',
                        }
            ...        )
            >>> git.short_hash()
        """

        repo = repo.strip()
        path = path.strip()

        if os.path.isdir(path):
            self.repo = Repo(path)
            if refresh:
                self.repo.git.pull('origin', 'master')
        else:
            if user is None:
                raise Exception('no user set to get the repo')

            _ = {'ssh': '', 'name': 'anonymous', 'email': 'anonymous@example.com'}
            _.update(user)
            user = _

            if not repo.startswith('git@'):
                raise Exception(
                    f'Invalid git checkout url: {repo}\n\n'
                    'Please make sure you are using the valid \
                    SSH url with the correct `git@github.com:account/repository.git` format\n\n'
                )

            if not os.path.isfile(user['ssh']):
                raise Exception(
                    f'Missing custom SSH script {user["ssh"]}!\n\n'
                    'You must provide a custom SSH script which can be \
                    able to execute git commands with the correct SSH key.\n'
                    'The bash script should contain this line:\n\n'
                    'ssh -i <SSH_private_key> -oIdentitiesOnly=yes \
                        -oStrictHostKeyChecking=no -oUserKnownHostsFile=/dev/null "$@"\n\n'
                )
            os.environ['GIT_SSH'] = user['ssh']
            os.makedirs(path)
            self.repo = Repo.clone_from(repo, path, env={'GIT_SSH': user['ssh']})
            self.repo.config_writer().set_value('user', 'name', user['name']).release()
            self.repo.config_writer().set_value('user', 'email', user['email']).release()

        self.commit = self.repo.head.commit

    @property
    def hash(self):
        """ return the hash oof the commit"""
        return str(self.commit.hexsha)

    def short_hash(self, num:int=4):
        """ sometimes a short hash is needed """
        return str(self.repo.git.rev_parse(self.commit.hexsha, short=num))

    @property
    def is_dirty(self):
        """ loos objects? """
        return self.repo.is_dirty()

    @property
    def is_bare(self):
        """ is it a bare repo?
        TODO: check all methods for bare.
        """
        return self.repo.bare

    def set_commit(self, commit:str="master"):
        """ set the commit to a different point """
        self.commit = self.repo.commit(commit)

    def print_commit(self):
        """ pretty printing commit infos """
        print('----')
        print(str(self.hash))
        print(f'"{self.commit.summary}" by {self.commit.author.name} ({self.commit.author.email})')
        print(str(self.commit.authored_datetime))
        print(str(f"count: {self.commit.count()} and size: {self.commit.size}"))

    def print_repo(self):
        """ pretty printing repo infos """
        print(f'Repo description: {self.repo.description}')
        print(f'Repo active branch is {self.repo.active_branch}')
        for remote in self.repo.remotes:
            print(f'Remote named "{remote}" with URL "{remote.url}"')
        print(f'Last commit for repo is {str(self.repo.head.commit.hexsha)}.')

    def auto_commit(self, branch: str = 'master', message: str = 'Auto commit'):
        """Basic commit method.
        This commit method will detect all file changes and doing `git add`,\
         `git commit -m <message>`, and `git push <branch>` all at once.
        """
        has_changed = False

        # Check if there's any untracked files
        for file in self.repo.untracked_files:
            print(f'Added untracked file: {file}')
            self.repo.git.add(file)
            if not has_changed:
                has_changed = True

        if self.is_dirty:
            for file in self.repo.git.diff(None, name_only=True).split('\n'):
                print(f'Added file: {file}')
                self.repo.git.add(file)
                if not has_changed:
                    has_changed = True

        if has_changed:
            self.repo.git.commit('-m', message)
            self.repo.git.push('origin', branch)
