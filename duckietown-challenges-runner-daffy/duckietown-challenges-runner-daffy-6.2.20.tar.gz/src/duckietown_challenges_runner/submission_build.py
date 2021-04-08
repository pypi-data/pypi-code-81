# coding=utf-8
import os
from typing import cast

from docker import DockerClient
from zuper_commons.fs import read_ustring_from_utf8_file
from zuper_commons.timing import now_utc
from zuper_commons.types import ZValueError

from duckietown_build_utils import (
    BuildFailed,
    BuildResult,
    DockerCompleteImageName,
    DockerCredentials,
    DockerOrganizationName,
    DockerRegistryName,
    DockerRepositoryName,
    get_complete_tag,
    get_duckietown_labels,
    get_important_env_build_args_dict,
    log_in_for_build,
    pull_for_build,
    run_build,
    update_versions,
)
from duckietown_challenges.utils import tag_from_date

__all__ = ["submission_build3"]


def submission_build3(
    credentials: DockerCredentials, registry: DockerRegistryName, no_cache: bool, pull: bool
) -> DockerCompleteImageName:
    df = "Dockerfile"
    if registry not in credentials:
        msg = f"Needs credentials for {registry}"
        raise ZValueError(msg, known=list(credentials))
    username = credentials[registry]["username"]
    organization = cast(DockerOrganizationName, username.lower())
    repository = cast(DockerRepositoryName, "aido-submissions-dummy")
    update_versions()

    tag = tag_from_date(now_utc())
    br = BuildResult(
        registry=registry, organization=organization, repository=repository, tag=tag, digest=None
    )
    complete_image = get_complete_tag(br)

    if not os.path.exists(df):
        msg = f'I expected to find the file "{df}".'
        raise Exception(msg)

    # cmd = ["docker", "build", "--pull", "-t", complete_image, "-f", df]
    path = os.getcwd()
    client = DockerClient.from_env()
    labels = get_duckietown_labels(path)

    df_contents = read_ustring_from_utf8_file(df)

    build_vars = get_important_env_build_args_dict(df_contents)
    log_in_for_build(df_contents, credentials)
    if pull:
        pull_for_build(client, df_contents, credentials, quiet=False)
    args = dict(
        path=path, tag=complete_image, pull=False, buildargs=build_vars, labels=labels, nocache=no_cache
    )
    try:
        run_build(client, **args)
    except BuildFailed:
        raise

    return complete_image
