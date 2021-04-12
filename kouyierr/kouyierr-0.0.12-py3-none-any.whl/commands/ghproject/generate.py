from datetime import datetime
import logging
import click

from ghapi.all import GhApi

from kouyierr.commands import global_options
from kouyierr.utils.helper import Helper


class Generator:
    def __init__(
            self,
            helper: Helper,
            user_token: str,
            repo_owner: str,
            repo_name: str,
            project: str,
            output_dir: str,
    ):
        logging.basicConfig(format="%(message)s")
        logging.getLogger(__package__).setLevel(logging.INFO)
        self._logger = logging.getLogger(__name__)
        self.helper = helper
        self.user_token = user_token
        self.output_dir = output_dir
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.project = project
        self.api = GhApi(token=user_token)

    def execute(self) -> None:
        f_markdown = open(f"project_{self.project.lower()}_tasks.md", "w+")
        projects = self.api.projects.list_for_repo(self.repo_owner, self.repo_name)
        project = [f for f in projects if str(f.name).lower() == self.project.lower()]
        project_id = project[0].id
        f_markdown.write(f"# Projet {self.project}\n\n")
        f_markdown.write(
            f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
        )
        for column in self.api.projects.list_columns(project_id):
            f_markdown.write(f"\n## Issue {column.name}\n\n")
            for card in self.api.projects.list_cards(column.id):
                card_split = card.content_url.split("/")
                owner = card_split[4]
                repo = card_split[5]
                issue_number = card_split[7]
                issue = self.api.issues.get(owner, repo, issue_number)
                labels = "".join(
                    f"[{f.name}]"
                    for f in issue.labels
                    if f.name.lower() != self.project.lower()
                )
                f_markdown.write(
                    f"* {issue.title} [#{issue.number}]({issue.html_url}) **{labels}**\n"
                )
        f_markdown.close()


@click.command(
    help="Generate a changelog-lookalike .md file with all Github project issues grouped by category/column"
)
@global_options
@click.option(
    "--user-token",
    required=True,
    type=str,
    help="Github personal access token used for authentication, use env_var for security reason",
)
@click.option(
    "--repo-owner",
    required=True,
    type=str,
    help="Github repository owner (user or organization)",
)
@click.option("--repo-name", required=True, type=str, help="Github repository name")
@click.option("--project", required=True, type=str, help="Github project name")
def generate(
        user_token: str, repo_owner: str, repo_name: str, project: str, output_dir: str
):
    Generator(
        Helper(), user_token, repo_owner, repo_name, project, output_dir
    ).execute()
