import logging
import traceback
from functools import wraps
from subprocess import check_output
from typing import Any, List, Optional

import zmtools

LOGGER = logging.getLogger(__name__)


class GICD():
    
    def __init__(self, repo_owner: str, repo_name: str) -> None:
        """Class that provides a function to create an issue on GitHub's issues section for a specific repo

        Args:
            repo_owner (str): The owner of the repo
            repo_name (str): The name of the repo
        """
        self.repo_owner = repo_owner
        self.repo_name = repo_name


    def _create_issue(self, issue_title: str, issue_body: str, issue_label: str = "bug") -> str:
        """Create an issue on GitHub's issues section for a specific repo

        Args:
            issue_title (str): The title of the issue to create
            issue_body (str): The body of the issue to create
            issue_label (str, optional): The label to attach to the issue. Defaults to "bug".

        Returns:
            str: The URL of the created issue
        """
        return check_output(["gh", "issue", "create", "--title", issue_title, "--body", issue_body, "--label", issue_label, "-R", f"{self.repo_owner}/{self.repo_name}"])


    def auto_create_issue(self, exceptions: Optional[List[Exception]] = None) -> Any:
        """Decorator to create a GitHub issue on exception throw

        Args:
            exceptions (list[Exception], optional): The exception types to create an issue for. If None, create the issue for any exception. Defaults to None.
        """
        def actual_decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if not exceptions or any(isinstance(e, etype) for etype in exceptions):
                        tb = traceback.format_exc().strip()
                        issue_title = zmtools.truncate(
                            tb.split("\n")[-1], length=25)
                        issue = self._create_issue(issue_title, f"```python\n{tb}\n```")
                        LOGGER.info(f"An issue was created at {issue}")
                    raise e
            return wrapper
        return actual_decorator
