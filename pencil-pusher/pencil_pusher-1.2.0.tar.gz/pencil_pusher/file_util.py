import os
from typing import List


class FileUtil:
    @staticmethod
    def query_directory(
        directory: str, include_extensions: List[str]
    ) -> List[str]:
        """
        Returns a list of file paths in the given directory and any
        of its containing sub directories

        Args:
            directory (str): the directory to query
            include_extensions (List[str]): a list of file extensions
                that should be included in the result set. any files
                with extensions not defined here will be ignored.
                Note: this should only inlcude the extension name
                and not a prefixed '.'
        """
        result: List[str] = []

        path = os.path.abspath(directory)

        for item in os.listdir(path):
            for ext in include_extensions:
                if item.endswith(ext):
                    result.append(path + "/" + item)
                    break
            if os.path.isdir(path + "/" + item):
                result.extend(
                    FileUtil.query_directory(
                        path + "/" + item + "/", include_extensions
                    )
                )

        return result
