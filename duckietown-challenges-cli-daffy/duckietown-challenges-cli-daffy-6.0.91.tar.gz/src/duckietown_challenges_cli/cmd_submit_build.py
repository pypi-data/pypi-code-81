import os
from typing import cast

from docker import DockerClient
from zuper_commons.fs import read_ustring_from_utf8_file
from zuper_commons.timing import now_utc
from zuper_commons.types import ZException

from duckietown_build_utils import (
    BuildFailed,
    BuildResult,
    docker_push_optimized,
    DockerCompleteImageName,
    DockerCredentials,
    DockerRegistryName,
    get_duckietown_labels,
    get_important_env_build_args_dict,
    log_in_for_build,
    parse_complete_tag,
    pull_for_build,
    run_build,
    update_versions,
)
from duckietown_challenges.utils import tag_from_date
from . import logger

__all__ = ["submission_build"]


def submission_build(
    credentials: DockerCredentials, registry: DockerRegistryName, no_cache: bool, pull: bool
) -> BuildResult:
    tag = tag_from_date(now_utc())
    df = "Dockerfile"

    if registry is None:
        logger.error("had to have explicit registry here")
        registry = cast(DockerRegistryName, "docker.io")
    if registry not in credentials:
        msg = f"Credentials for registry {registry} not available"
        raise ZException(msg, available=list(credentials))
    username = credentials[registry]["username"]
    organization = username.lower()
    repository = "aido-submissions"
    update_versions()

    complete_image = DockerCompleteImageName(f"{registry}/{organization}/{repository}:{tag}")

    if not os.path.exists(df):
        msg = f'I expected to find the file "{df}".'
        raise Exception(msg)

    # cmd = ["docker", "build", "--pull", "-t", complete_image, "-f", df]
    path = os.getcwd()
    client = DockerClient.from_env()
    labels = get_duckietown_labels(path)

    df_contents = read_ustring_from_utf8_file(df)
    log_in_for_build(df_contents, credentials)
    if pull:
        pull_for_build(client, df_contents, credentials, quiet=False)
    build_vars = get_important_env_build_args_dict(df_contents)
    args = dict(
        path=path, tag=complete_image, buildargs=build_vars, labels=labels, nocache=no_cache, pull=False
    )
    try:
        run_build(client, **args)
    except BuildFailed:
        raise

    digest = docker_push_optimized(complete_image, credentials=credentials)
    br = parse_complete_tag(digest)
    br.tag = tag
    return br
