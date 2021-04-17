
from generalpackager.api.shared import _SharedAPI
from generalfile import Path
from generallibrary import Ver, deco_cache, Recycle

from setuptools import find_namespace_packages
import re
from git import Repo
import subprocess
import sys


def load_metadata_before(func):
    def _wrapper(self, *args, **kwargs):
        """ :param LocalRepo self: """
        if not self.has_loaded_metadata:
            self.load_metadata()
        return func(self, *args, **kwargs)
    return _wrapper


class LocalRepo(Recycle, _SharedAPI):
    """ Tools to help Path interface a Local Python Repository.
        Todo: Search for imports to list dependencies. """
    enabled = True
    name = ...
    version = "0.0.1"  # type: Ver
    description = "Missing description."
    install_requires = []
    extras_require = {}
    topics = []
    manifest = []

    metadata_keys = [key for key, value in locals().items() if not key.startswith("_")]
    _recycle_keys = {"name": lambda name: str(LocalRepo.get_path_from_name(name=name))}

    def __init__(self, name=None):
        self.path = self.get_path_from_name(name=name)
        self.has_loaded_metadata = False

    def __repr__(self):
        return str(self.path)

    def has_metadata(self):
        return self.get_metadata_path().exists()

    def load_metadata(self):
        self.has_loaded_metadata = True

        if self.get_metadata_path().exists():
            for key, value in self.get_metadata_path().read().items():
                setattr(self, f"_{key}", value)

            if self.extras_require:
                self.extras_require["full"] = list(set().union(*self.extras_require.values()))
                self.extras_require["full"].sort()

            self.version = Ver(self.version)

        if self.name is Ellipsis:
            self.name = self.path.name()

    def get_metadata_dict(self):
        return {key: str(getattr(self, key)) if key == "version" else getattr(self, key) for key in self.metadata_keys}

    def write_metadata(self):
        self.get_metadata_path().write(self.get_metadata_dict(), overwrite=True)

    def exists(self):
        """ Return whether this API's target exists. """
        return self.path_exists(path=self.path)

    @classmethod
    def path_exists(cls, path):
        if path.is_file() or not path.exists():
            return False
        return bool(path.get_child(filt=lambda x: x.name() in ("README.md", ), traverse_excluded=True))
        # return bool(path.get_child(filt=lambda x: x.name() in ("setup.py", ), traverse_excluded=True))

    @classmethod
    def get_repo_path_parent(cls, path=None):
        """ Iterate self and parents to return first path where LocalRepo can be created or None.

            :param Path or any path:
            :rtype: Path """
        return Path(path=path).absolute().get_parent(depth=-1, include_self=True, filt=LocalRepo.path_exists, traverse_excluded=True)

    @classmethod
    def get_repo_path_child(cls, folder_path):
        """ Return whether there's atleast one repo in folder. """
        return Path(folder_path).get_child(filt=LocalRepo.path_exists, traverse_excluded=True)

    @classmethod
    def get_repos_path(cls, path=None):
        """ Try to return absolute path pointing to folder containing repos or None.

            :rtype: Path """
        filt = lambda path: LocalRepo.get_repo_path_child(path) and not path.match("/test")
        return Path(path).absolute().get_parent(depth=-1, include_self=True, filt=filt, traverse_excluded=True)

    @classmethod
    def get_path_from_name(cls, name=None):
        """ Get path from name.

            :param Path or any name:
            :rtype: Path """
        # Check if inside correct repo already
        path = cls.get_repo_path_parent()
        if path and (name is None or name == path.name()):
            return path

        if name is None:
            name = "generalpackager"

        # Check if there's a parent that has a repo child that exists
        repos_path = cls.get_repos_path()
        if repos_path:
            return repos_path / name

        return Path(name).absolute()

    @load_metadata_before
    def _metadata_getter(self, key):
        return getattr(self, f"_{key}")

    @load_metadata_before
    def _metadata_setter(self, key, value):
        """ Set a metadata's key both in instance and json file. """
        if self.has_metadata() and value != getattr(self, f"_{key}", ...):
            metadata = self.get_metadata_path().read()
            metadata[key] = str(value)
            self.get_metadata_path().write(metadata, overwrite=True, indent=4)
        setattr(self, f"_{key}", value)

    def get_readme_path(self):      return self.path / "README.md"
    def get_metadata_path(self):    return self.path / "metadata.json"
    def get_git_exclude_path(self): return self.path / ".git/info/exclude"
    def get_setup_path(self):       return self.path / "setup.py"
    def get_manifest_path(self):    return self.path / "MANIFEST.in"
    def get_license_path(self):     return self.path / "LICENSE"
    def get_workflow_path(self):    return self.path / ".github/workflows/workflow.yml"
    def get_test_path(self):        return self.path / f"{self.name}/test"
    def get_init_path(self):        return self.path / self.name / "__init__.py"

    @deco_cache()
    def get_test_paths(self):
        """ Yield paths to each test python file. """
        return self.get_test_path().get_children(depth=-1, filt=lambda path: path.endswith(".py") and not path.match("/tests/"), traverse_excluded=True)

    @deco_cache()
    def text_in_tests(self, text):
        """ Return whether text exists in one of the test files. """
        for path in self.get_test_paths():
            if path.contains(text=text):
                return True
        return False

    def get_package_paths_gen(self):
        """ Yield Paths pointing to each folder containing a Python file in this local repo, aka `namespace package`.
            Doesn't include self.path """
        for package in find_namespace_packages(where=str(self.path)):
            path = self.path / package.replace(".", "/")
            if not path.match("/dist", "/build"):
                yield path

    def git_changed_files(self):
        """ Get a list of changed files using local .git folder. """
        repo = Repo(str(self.path))
        return [Path(file) for file in re.findall("diff --git a/(.*) " + "b/", repo.git.diff())]

    def bump_version(self):
        """ Bump micro version in metadata.json. """
        self.version = self.version.bump()

    def pip_install(self):
        """ Install this repository with pip, WITHOUT -e flag.
            Subprocess messed up -e flag compared to doing it in terminal, so use the normal one."""
        subprocess.check_call([sys.executable, "-m", "pip", "install", str(self.path)])

    def pip_uninstall(self):
        """ Uninstall this repository with pip."""
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", self.name])

    def unittest(self):
        """ Run unittests for this repository. """
        subprocess.check_call([sys.executable, "-m", "unittest", "discover", str(self.get_test_path())])

    def create_sdist(self):
        """ Create source distribution. """
        with self.path.as_working_dir():
            subprocess.check_call([sys.executable, "setup.py", "sdist", "bdist_wheel"])

    def upload(self):
        """ Upload local repo to PyPI. """
        self.create_sdist()
        with self.path.as_working_dir():
            subprocess.check_call([sys.executable, "-m", "twine", "upload", "dist/*"])

for key in LocalRepo.metadata_keys:
    value = getattr(LocalRepo, key)
    setattr(LocalRepo, f"_{key}", value)
    setattr(LocalRepo, key, property(
        fget=lambda self, key=key: LocalRepo._metadata_getter(self, key),
        fset=lambda self, value, key=key: LocalRepo._metadata_setter(self, key, value),
    ))


































