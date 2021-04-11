from typing import Dict
from datetime import datetime
import pandas as pd
from base64 import b64decode
from io import BytesIO
from github import Github
import functools
import os
from parse_zip import parse_zip


REPO = "rfordatascience/tidytuesday"
PARSERS = {
    "csv": pd.read_csv,
    "xlsx": pd.read_excel,
    "tsv": functools.partial(pd.read_csv, delimiter="\t"),
}
PARSERS["zip"] = functools.partial(parse_zip, parsers=PARSERS)


def get_pat():
    if "GITHUB_TOKEN" in os.environ and os.environ["GITHUB_TOKEN"]:
        return os.environ["GITHUB_TOKEN"]
    if "GITHUB_PAT" in os.environ and os.environ["GITHUB_PAT"]:
        return os.environ["GITHUB_PAT"]

    return None


class TidyTuesday:
    data: Dict[str, pd.DataFrame] = {}
    readme: str = ""

    def __init__(self, date, auth=get_pat()):
        # convert improperly formatted dates like 2018-5-21 into 2018-05-21
        self.date = datetime.strptime(date, "%Y-%m-%d").date().strftime("%Y-%m-%d")

        self.gh = Github(auth)
        self.repo = self.gh.get_repo(REPO)

        success = self.load_context()
        if success:
            self.download_files()

    def get_blob(self, sha):
        return b64decode(self.repo.get_git_blob(sha).content)

    def get_rate_limit(self, n=10):
        limit = self.gh.get_rate_limit().core
        if limit.remaining - 1 < n:
            print("Github API rate limit is hit.")
            print(f"You can try again at {limit.reset.strftime('%Y-%m-%d %r %Z')}.")
            return True

        return False

    def load_context(self):
        if self.get_rate_limit(2):
            return False

        tree = self.repo.get_git_tree("master:static").tree

        # get shas of files in static folder
        static_sha = {x.path: x.sha for x in tree}

        ttdt = pd.read_csv(BytesIO(self.get_blob(static_sha["tt_data_type.csv"])))
        file_info = ttdt.loc[
            ttdt["Date"] == self.date, ["data_files", "data_type", "delim"]
        ]

        if file_info["data_files"].isna().all():
            raise ValueError("No TidyTuesday for " + self.date)

        # compile info for data files
        self._file_info = {}
        for _, row in file_info.iterrows():
            self._file_info[row["data_files"]] = (row["data_type"], row["delim"])

        return True

    def download_files(self):
        # get shas of files
        total = len(self._file_info)
        if self.get_rate_limit(2 + total):
            return

        tree = self.repo.get_git_tree(f"master:data/{self.date[:4]}/{self.date}/").tree
        sha = {x.path: x.sha for x in tree}

        if "readme.md" in sha:
            self.readme = self.get_blob(sha["readme.md"]).decode("utf-8")
        else:
            print("\033[1m--- No readme detected ---\033[0m")

        if total > 1:
            print(f"\033[1m--- There are {total} files available ---\033[0m")
        else:
            print("\033[1m--- There is 1 file available ---\033[0m")

        print("\033[1m--- Starting download ---\033[0m\n")

        for i, (file, (dtype, delim)) in enumerate(self._file_info.items()):
            print(f"\tDownloading file {i+1} of {total}: {file}")

            content = self.get_blob(sha[file])
            parser = PARSERS[dtype]
            if str(delim) != "nan":
                parser = functools.partial(parser, delimiter=delim)

            if dtype == "zip":
                self.data.update(parser(BytesIO(content)))
            else:
                self.data[file.split(".")[0]] = parser(BytesIO(content))

        print("\n\033[1m--- Download complete ---\033[0m")
