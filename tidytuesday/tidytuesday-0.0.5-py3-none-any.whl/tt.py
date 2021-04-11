from datetime import datetime
import pandas as pd
from base64 import b64decode
from io import BytesIO
from github import Github
import os

REPO = "rfordatascience/tidytuesday"


def get_pat():
    if os.environ["GITHUB_PAT"]:
        return os.environ["GITHUB_PAT"]
    if os.environ["GITHUB_TOKEN"]:
        return os.environ["GITHUB_TOKEN"]

    return ""


class TidyTuesday:
    def __init__(self, date, auth=get_pat()):
        self.date = datetime.strptime(date, "%Y-%m-%d").date()

        if self.date.weekday() != 1:
            raise ValueError(f'{self.date.strftime("%Y-%m-%d")} is not a Tuesday')

        self.date = self.date.strftime("%Y-%m-%d")
        self.gh = Github(auth).get_repo(REPO)
        self.load_context()
        self.download_files()

    def load_context(self):
        # master = {}
        # tree = self.gh.get_git_tree("master:static")
        # master["sha"] = tree.sha

        # master["path"] = {}
        # for path in tree.tree:
        #     master["path"][path.path] = path.sha

        prefix = f"data/{self.date[:4]}/{self.date}/"

        data = self.gh.get_contents("static/tt_data_type.csv").content
        ttdt = pd.read_csv(BytesIO(b64decode(data)))
        self._file_names = ttdt.loc[ttdt["Date"] == self.date, "data_files"]

        if self._file_names.isna().all():
            raise ValueError("No TidyTuesday for this Tuesday")

        # get shas of files
        tree = self.gh.get_git_tree("master:" + prefix).tree
        self.sha = {x.path: x.sha for x in tree}

        readme = self.gh.get_git_blob(self.sha["readme.md"]).content
        self.readme = b64decode(readme).decode("utf-8")

    def download_files(self):
        total = len(self._file_names)
        print(f"\033[1m--- There are {total} files available ---\033[0m")
        print("\033[1m--- Starting download ---\033[0m\n")
        for i, file in enumerate(self._file_names):
            print(f"\tDownloading file {i+1} of {total}: {file}")
            content = self.gh.get_git_blob(self.sha[file]).content
            setattr(self, file.split(".")[0], pd.read_csv(BytesIO(b64decode(content))))
        print("\n\033[1m--- Download complete ---\033[0m")
