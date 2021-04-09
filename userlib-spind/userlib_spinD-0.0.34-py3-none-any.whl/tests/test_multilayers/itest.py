# -*- coding: utf-8 -*-
r"""
abstract base class for tests in multilayer test branch
"""
from python3.shell_commands import writelog
from abc import ABC, abstractmethod
from pathlib import Path
import shutil


class ITest(ABC):
    r"""
    abstract base class for tests.
    """

    def __init__(self, logfile: Path, cleanup: bool = True, **kwargs) -> None:
        r"""
        Initializes test. Each inheriting test class has to call super().__init__ as this initializes the test
        directories

        Args:
            cleanup(bool): boolean flag if the temp-directory after the test shall be deleting. The default value is
            True.
        """
        self.logfile = logfile
        self.tempdir = self._load_tempdir()
        self.cleanup = cleanup

    def _load_tempdir(self) -> Path:
        r"""
        Loads the temporary directory for the test.
        """
        if (Path.cwd() / f'{self.testsignature}_temp_').is_dir():
            # print('WARNING: temp folder for this test already exists. Removing...')
            shutil.rmtree(Path.cwd() / f'{self.testsignature}_temp_')
        l_p = (Path.cwd() / f'{self.testsignature}_temp_')
        l_p.mkdir()
        return l_p

    @property
    @abstractmethod
    def testsignature(self) -> int:
        r"""
        The test signature helps to identify different test and also ensures unique _temp_-folders for different test-
        routines.

        Returns:
            the test signature
        """

    @abstractmethod
    def __call__(self, *args, **kwargs) -> bool:
        r"""
        perform a single test

        Returns:
            the result of the test.
        """

    @abstractmethod
    def __repr__(self) -> str:
        r"""
        Returns:
            the representation of the testing class.
        """

    def cleanup_test(self) -> None:
        r"""
        Any test subclass inheriting from this class has this cleanup method.
        """
        if not self.tempdir.is_dir():
            raise FileNotFoundError('_temp_-folder for this test does not exist.')
        writelog(self.logfile, message='#' * 100)
        writelog(self.logfile, message='clean up test: remove temporary files...')
        shutil.rmtree(self.tempdir)
