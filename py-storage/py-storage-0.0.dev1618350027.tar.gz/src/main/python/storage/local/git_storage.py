from __future__ import annotations

import abc
import logging
import tempfile
from logging import Logger
from typing import Tuple
from git import Repo, Actor

from storage import MutableStorageSession, E, MutableRepository, Repository, Entity
from storage.api import SessionSupportStorage
from storage.local.file_repository import FileRepositoryListener, FileRepositoryFactory, FileRepository

__logger__: Logger = logging.getLogger(__name__)


class SessionFactory(abc.ABC):

    @abc.abstractmethod
    def __call__(self, origin: GitStorage, message: str) -> MutableStorageSession:
        raise NotImplementedError()


class SessionStrategy:
    class BaseSessionStrategy(MutableStorageSession, FileRepositoryListener):

        def __init__(self, storage: GitStorage, message: str):
            self.storage = storage
            self.message = message

        def repository_for(self, item_type: Entity[E]) -> Repository[E]:
            return self.storage.repository_for(item_type)

        def mutable_repository_for(self, item_type: Entity[E]) -> MutableRepository[E]:
            repository = self.storage.mutable_repository_for(item_type)
            repository.add_listener(self)
            return repository

        def __enter__(self):
            self.on_begin()
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type:
                self.on_error()
                raise exc_val
            self.on_success()

        def on_error(self):
            pass

        def on_success(self):
            pass

        def on_begin(self):
            pass

        def on_rewrite(self, file_name):
            pass

        @classmethod
        def create(cls, **defaults):
            return lambda storage, message: cls(storage, message, **defaults)

    class AddAndCommit(BaseSessionStrategy):

        def __init__(self, storage: GitStorage, message: str,
                     author: Tuple[str, str] = None,
                     committer: Tuple[str, str] = None):
            super().__init__(storage, message)
            self.author = None if author is None else Actor(*author)
            self.committer = None if committer is None else Actor(*committer)

        def on_rewrite(self, file_name):
            self.storage.repo.index.add(file_name)

        def on_error(self):
            self.storage.repo.index.reset()
            self.storage.repo.git.clean('.', force=True)

        def on_success(self):
            self.storage.repo.index.commit(
                self.message,
                author=self.author,
                committer=self.committer,
            )

    class PullAddAndCommit(AddAndCommit):

        def __init__(self, storage: GitStorage, message: str,
                     author: Tuple[str, str] = None, committer: Tuple[str, str] = None,
                     remote='origin', branch='master'):
            super().__init__(storage, message, author=author, committer=committer)
            self.pull_remote = remote
            self.pull_branch = branch

        def on_begin(self):
            remote = self.storage.repo.remote(self.pull_remote)
            remote.pull(self.pull_branch, rebase=True)

    class AddCommitAndPush(AddAndCommit):

        def __init__(self, storage: GitStorage, message: str,
                     author: Tuple[str, str] = None, committer: Tuple[str, str] = None,
                     remote='origin', branch='master'):
            super().__init__(storage, message, author=author, committer=committer)
            self.push_remote = remote
            self.push_branch = branch

        def on_success(self):
            super().on_success()
            remote = self.storage.repo.remote(self.push_remote)
            remote.push(self.push_branch)

    class PullAddCommitAndPush(PullAddAndCommit, AddCommitAndPush):
        pass


class GitStorage(SessionSupportStorage):
    logger = __logger__

    def __init__(self, base_path: str, session_strategy=SessionStrategy.AddAndCommit):
        self.base_path = base_path
        self.repo = Repo(self.base_path)
        self.repository_factory = FileRepositoryFactory(self.base_path)
        self.session_strategy = session_strategy

    def open_session(self, message: str = None) -> MutableStorageSession:
        return self.session_strategy(self, message)

    def mutable_repository_for(self, item_type: Entity[E]) -> FileRepository[E]:
        repository = self.repository_factory.create(item_type)
        return repository

    def repository_for(self, item_type: Entity[E]) -> Repository[E]:
        return self.mutable_repository_for(item_type)

    @classmethod
    def from_repo(cls, repo: Repo, **kwargs):
        return cls(repo.working_dir, **kwargs)

    @classmethod
    def create_from_url(cls, git_url: str, target: str = None, **kwargs):
        target = target or tempfile.TemporaryDirectory().name
        Repo.clone_from(git_url, target)
        return cls(target, **kwargs)

    @classmethod
    def empty(cls, target: str = None, **kwargs):
        target = target or tempfile.TemporaryDirectory().name
        Repo.init(target)
        return cls(target, **kwargs)
