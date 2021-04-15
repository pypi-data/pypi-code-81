import requirements
import os

from spell.api.models import RunRequest
from spell.cli.exceptions import ExitException
from spell.cli.utils.dependencies import merge_dependencies, split_pip_conda


# returns a list of pip packages
def get_requirements_file(requirements_file):
    if requirements_file is None:
        return []
    pip_packages = []
    if not os.path.isfile(requirements_file):
        raise ExitException("--pip-req file not found: " + requirements_file)
    with open(requirements_file, "r") as rf:
        for req in requirements.parse(rf):
            pip_packages.append(req.line)
    return pip_packages


def get_run_request(client, kwargs):
    """Converts an python API request's kwargs to a RunRequest"""
    # grab conda env file contents
    python_deps = merge_dependencies(
        None,
        kwargs.pop("conda_file", None),
        kwargs.pop("requirements_file", None),
        kwargs.pop("pip_packages", []),
    )
    pip, conda = split_pip_conda(python_deps)
    # set workflow id
    if "workflow_id" not in kwargs and client.active_workflow:
        kwargs["workflow_id"] = client.active_workflow.id

    return RunRequest(
        run_type="user",
        pip_packages=pip,
        conda_file=conda,
        **kwargs,
    )


def validate_pip(pip):
    if pip.find("==") != pip.find("="):
        raise ExitException(
            f"Invalid pip dependency {pip}: = is not a valid operator. Did you mean == ?"
        )


def format_pip_apt_versions(pip, apt):
    if pip:
        for x in pip:
            validate_pip(x)
        pip = [convert_name_version_pair(x, "==") for x in pip]
    if apt:
        apt = [convert_name_version_pair(x, "=") for x in apt]
    return (pip, apt)


def convert_name_version_pair(package, separator):
    split = package.split(separator)
    return {"name": split[0], "version": split[1] if len(split) > 1 else None}
