# Copyright 2021 Francesco Apruzzese <cescoap@gmail.com>
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl-3.0.html).

import importlib
from os import listdir, getcwd, chdir
from os.path import join
import click
import yaml
from github import Github
from base64 import b64decode
from datetime import datetime


CLI_DOC_KEY = "description"


class Repo:
    def __init__(self, script_name, repo_data, token):
        gh = Github(token)
        # TODO: Separate import based on marche.yaml version
        self._script_name = script_name
        self.name = repo_data["name"]
        self.repo = gh.get_repo(self.name)
        self.source_branch = str(repo_data["source_branch"])
        self.target_branch = str(repo_data["target_branch"])
        self._collect_pr = False
        self._collected_pr = []

    @property
    def collect_pr(self):
        return self._collect_pr

    @collect_pr.setter
    def collect_pr(self, value: bool):
        self._collect_pr = value

    def collected_pr(self):
        return self._collected_pr

    def branch_exists(self, branch):
        for b in list(self.repo.get_branches()):
            if b.name == branch:
                return b
        return False

    def _create_or_get_branch(self, branch):
        # If target branch doesn't exist on remote, create it
        existing_branch = self.branch_exists(branch)
        if not existing_branch:
            source_branch = self.repo.get_branch(self.source_branch)
            existing_branch = self.repo.create_git_ref(
                ref=f"refs/heads/{self.target_branch}",
                sha=source_branch.commit.sha,
            )
        existing_branch = self.branch_exists(branch)
        return existing_branch

    def create_file(self, file_name, file_content, commit_message):
        target_branch = self._create_or_get_branch(self.target_branch)
        # Create remote file
        commit = self.repo.create_file(
            file_name, commit_message, file_content, branch=target_branch.name
        )
        return commit

    def read_file(self, file_name):
        content = self.repo.get_contents(file_name)
        raw_content = b64decode(content.content)
        return raw_content

    def read_local_file(self, file_name):
        file_to_read = open(
            join(".", "scripts", self._script_name, "resources", file_name)
        )
        file_content = file_to_read.read()
        file_to_read.close()
        return file_content

    def update_file(self, file_name, file_content, commit_message):
        target_branch = self._create_or_get_branch(self.target_branch)
        # Update remote file
        contents = self.repo.get_contents(file_name, ref=target_branch.name)
        commit = self.repo.update_file(
            contents.path,
            commit_message,
            file_content,
            contents.sha,
            branch=target_branch.name,
        )
        return commit

    def delete_file(self, file_name, commit_message):
        target_branch = self._create_or_get_branch(self.target_branch)
        # Create remote file
        contents = self.repo.get_contents(file_name, ref=target_branch.name)
        self.repo.delete_file(
            contents.path,
            commit_message,
            contents.sha,
            branch=target_branch.name,
        )

    def create_pr(self, title, body, reviewers=False):
        target_branch = self._create_or_get_branch(self.target_branch)
        pr = self.repo.create_pull(
            title=title,
            body=body,
            head=target_branch.name,
            base=self.source_branch,
        )
        if reviewers:
            pr.create_review_request(reviewers)
        if self.collect_pr:
            self._collected_pr.append(pr)
        return pr

    def _rich_log_message(self, message):
        now = datetime.now().strftime("%Y-%M-%d %H:%M:%S.%s")
        return f"[{now}] [{self.name}] {message}"

    def log_info(self, message):
        click.echo(self._rich_log_message(message))

    def log_warning(self, message):
        click.secho(self._rich_log_message(message), fg="red")

    def log_debug(self, message):
        click.secho(self._rich_log_message(message), fg="yellow")

    def log_ok(self, message):
        click.secho(self._rich_log_message(message), fg="green")


def get_config(path):
    # TODO: Check if file exists or raise an error
    with open(join(path, "marche.yaml")) as config_yaml:
        data = yaml.load(config_yaml, Loader=yaml.FullLoader)
        return data


def module_from_file(module_name, file_path):
    marche_py_path = join(file_path, "marche.py")
    spec = importlib.util.spec_from_file_location(module_name, marche_py_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@click.group()
def cli():
    pass


@cli.command()
def available_scripts():
    scripts_path = listdir(".")
    for script_path in scripts_path:
        response = script_path
        config_data = get_config(join(".", script_path))
        if config_data.get(CLI_DOC_KEY, False):
            response = f"{response} - {config_data[CLI_DOC_KEY]}"
        click.echo(response)


@cli.command()
@click.option("-t", "--token")
@click.option("--collect-pr/--no-collect-pr", default=True)
@click.option("--bar/--no-bar", default=True)
@click.argument("name")
@click.argument("script_args", nargs=-1)
def script(name, token, collect_pr, bar, script_args):
    # Dinamically import sub-script
    # TODO: Check if script exists or raise an error
    script_path = join(getcwd(), name)
    script_module = module_from_file("marche", script_path)
    marche_fnct = script_module.marche
    # Get configurations
    config_data = get_config(script_path)
    if collect_pr:
        prs = {}
    # Execute main function
    repos = config_data.get("repo", [])
    with click.progressbar(length=len(repos), width=0) as progressbar:
        for repo_data in repos:
            repo = Repo(name, repo_data, token)
            # Set always collect_pr property of repo
            repo.collect_pr = collect_pr
            marche_fnct(repo, script_args)
            # Collect repo prs
            if collect_pr:
                prs[repo.name] = repo.collected_pr()
            if bar:
                progressbar.update(1)
    # Show all the collected pr
    if collect_pr:
        for repo_name in prs:
            click.echo(f"{repo_name} PRs list:")
            for pr in prs[repo_name]:
                click.echo(f"\tPR #{pr.number} -> {pr.html_url}")


def entrypoint():
    cli()
