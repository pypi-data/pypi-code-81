from os import path as _p
from unittest import TestCase

import sh

from yautil import git_expand
from tempfile import TemporaryDirectory


class TestGit(TestCase):
    tmpdir: TemporaryDirectory

    def setUp(self):
        self.tmpdir = TemporaryDirectory()

    def tearDown(self) -> None:
        self.tmpdir.cleanup()

    def test_expand(self):
        test_repo = _p.join(_p.dirname(__file__), 'hello-git-repo')
        test_repo_bkup = _p.join(self.tmpdir.name, 'hello-git-repo.bkup')

        sh.cp(test_repo, test_repo_bkup, r=True)

        git_expand(test_repo, self.tmpdir.name, 'branch-A', 'branch-B', 'branch-C')

        with open(_p.join(self.tmpdir.name, 'branch-A', 'A'), 'r') as f:
            assert f.read() == 'A'

        with open(_p.join(self.tmpdir.name, 'branch-B', 'B'), 'r') as f:
            assert f.read() == 'B'

        with open(_p.join(self.tmpdir.name, 'branch-C', 'C'), 'r') as f:
            assert f.read() == 'C'

        assert not str(sh.diff(test_repo, test_repo_bkup, r=True))
