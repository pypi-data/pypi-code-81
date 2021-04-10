import os
import re

from release_mgr.git import git


class VersionFile:
    """
    Represents a file which would contain the version.
    """

    filename = ""
    pattern = re.compile("")
    replace_pattern = "{new_version}"

    @classmethod
    def from_file(cls):
        if os.path.exists(cls.filename):
            return cls()

        return None

    def update(self, version: str):
        if not self.pattern:
            raise Exception("Tried to update a file without a pattern!")

        with open(self.filename, encoding="utf-8") as existing:
            content = existing.read()

        if self.pattern.search(content) is None:
            return False

        content = self.pattern.sub(
            self.replace_pattern.format(new_version=version),
            content,
        )

        with open(self.filename, "w", encoding="utf-8") as new:
            new.write(content)

        git("add", self.filename)
        return True
