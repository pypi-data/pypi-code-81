"""
This module contains functions for managing a repository

This includes
- cloning a repo
- cloning a repo's wiki
- installing a repo's python project

"""
import shutil
from typing import List
from pencil_pusher.process_util import ProcessUtil
from pencil_pusher.file_util import FileUtil
from pencil_pusher.documenter import Documenter
from pencil_pusher.github_api import GithubAPI
from pencil_pusher.configs import config_manager


class RepoManager:
    def __init__(self, owner: str, repo: str, github_api: GithubAPI):
        """
        Creates a RepoManager object, designed to manage a repo and
        its corresponding wiki.

        Args:
            owner (str): the owner of the repo
            repo (str): the name of the repo
            github_api (GithubAPI): the `GithubAPI` object being
                used to iterface this repo with github
        """
        self._owner = owner
        self._repo = repo
        self._gh = github_api

    def setup(self):
        """
        clones both this repo and its wiki into their
        own directories
        """
        self._gh.clone_repo(self._owner, self._repo, self._repo_path)
        self._gh.clone_repo(self._owner, f"{self._repo}.wiki", self._wiki_path)

    def install(self):
        """
        installs the python project in the source repo
        using the command pip install . (from source repo)
        """
        ProcessUtil.execute(
            ["python3", "-m", "pip", "install", "."], cwd=self._repo_path
        )

    def document(
        self,
        sources: List[str] = [],
        module: str = "",
        title_prefix: str = "",
        title_suffix: str = "",
        titles: dict = {},
        extensions: List[str] = [],
    ):
        """
        documents all given modules in the source
        repo (using config definition) then outputs
        them to the wiki repo and commits them

        Args:
            sources (List[str]): the sources defined by the config file to document
            module (str): the name of the base python module in the repo (defaults
                to the same name as the repo)
            title_prefix (str): text to append before the title of a generated file
            title_suffix (str): text to append after the title of a generated file
            extensions (List[str]): any extension (excluding leading '.') to check for
                in the sources (only applies to directory sources)
        """
        if module == "":
            # use default module name (same as repo name)
            module = self._repo

        file_list = self._get_file_list(sources, extensions)

        for f in file_list:
            module_python_path = f.replace("/", ".")
            title = f

            # use user defined titles if they exist
            if title in titles:
                title = titles[title]
            else:
                title = module_python_path

            Documenter.generate(
                module_python_path,
                title_prefix + title + title_suffix,
                self._wiki_path,
            )

    def publish(self):
        """
        Publishes the generated documentation to the
        wiki repo
        """
        self._gh.full_update(
            self._owner, f"{self._repo}.wiki", self._wiki_path
        )

    def cleanup(self):
        """
        removes all files created by this object
        """
        shutil.rmtree(self._repo_path)
        shutil.rmtree(self._wiki_path)

    @property
    def _repo_path(self) -> str:
        """
        Returns the relative path of the source repo
        """
        return f"../{self._repo}"

    @property
    def _wiki_path(self) -> str:
        """
        Returns the relative path of the wiki repo
        """
        return f"../{self._repo}-wiki"

    def _get_file_list(
        self, sources: List[str], extensions: List[str]
    ) -> List[str]:
        """
        Gets a list of all files to process

        Args:
            sources (List[str]): the user defined sources to process
            extensions (List[str]): the file extensions to check for
                (only applies to directory sources)

        Returns:
            List[str]: a list of file paths to process for documentation
        """
        file_list = []

        for source in sources:
            if source.endswith("/"):
                # source is a directory
                directory_files = FileUtil.query_directory(
                    f"../{self._repo}/{source[:-1]}", extensions
                )
                for sf in directory_files:
                    response = config_manager.process_lang_file(sf)
                    if not response[0]:
                        continue
                    relative_source_file = sf[
                        sf.index(self._repo) + len(self._repo) + 1 : -3
                    ]
                    file_list.append(relative_source_file)

            else:
                # source is a file
                response = config_manager.process_lang_file(source)
                if not response[0]:
                    continue
                for ext in extensions:
                    if source.endswith(f".{ext}"):
                        # remove extension
                        source = source[: -(len(ext) + 1)]

                    file_list.append(source)
        return file_list
