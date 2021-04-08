import argparse
import os
from configparser import ConfigParser
from typing import List, Optional

from docker import DockerClient
from zuper_commons.fs import read_ustring_from_utf8_file
from zuper_commons.types import ZException

from duckietown_build_utils import (
    aido_check_need_upload_main,
    aido_check_not_dirty_main,
    aido_check_tagged_main,
    aido_dir_status_main,
    aido_labels_main,
    BuildFailed,
    DirInfo,
    docker_push_optimized,
    docker_push_retry,
    DockerCompleteImageName,
    get_complete_tag_notag,
    get_dir_info_exceptions,
    get_duckietown_labels,
    log_in_for_build,
    parse_complete_tag,
    pull_for_build,
    run_build,
    update_versions,
)
from duckietown_docker_utils import (
    ENV_IGNORE_DIRTY,
    ENV_IGNORE_UNTAGGED,
    ENV_REGISTRY,
    IMPORTANT_ENVS,
)
from . import logger
from .cli_common import ChallengeEnvironment
from .dt_push import dt_push_main

__all__ = [
    "dt_push",
    "dt_dir_status",
    "dt_push_main",
    "dt_update_reqs",
    "dt_check_tagged",
    "dt_labels",
    "dt_build_container",
    "dt_check_not_dirty",
    "dt_push_container",
    "dt_check_need_upload",
]


def dt_push(args: List[str], environment: ChallengeEnvironment):
    """ Equivalent to `docker push` with some optimization to avoid pushing when not required. """
    return dt_push_main(args, environment.docker_credentials)


def dt_update_reqs(args: List[str], environment: ChallengeEnvironment):
    """ Updates versions in the requirements file to the last available from PIP_INDEX_URL repo. """
    parser = argparse.ArgumentParser(prog=environment.prog)
    parser.add_argument("-r", "--requirements", default="requirements.txt", help="Source requirements file")
    parser.add_argument(
        "-o", "--output", default="requirements.resolved", help="Destination requirements file"
    )
    parsed = parser.parse_args(args)

    update_versions(fn=parsed.requirements, out=parsed.output)


def dt_dir_status(args: List[str], environment: ChallengeEnvironment):
    """ Returns the status of the repo, noting updated, deleted, etc. Used for debugging. """
    _ = environment
    return aido_dir_status_main(args=args)


def dt_check_tagged(args: List[str], environment: ChallengeEnvironment):
    """ Checks that the repo is at a tagged commit. """
    _ = environment
    return aido_check_tagged_main(args=args)


def dt_check_not_dirty(args: List[str], environment: ChallengeEnvironment):
    """ Checks that the repo is not dirty. """
    _ = environment
    return aido_check_not_dirty_main(args=args)


def dt_labels(args: List[str], environment: ChallengeEnvironment):
    """ Gets the image labels that describe the repo. """
    _ = environment
    return aido_labels_main(args=args)


def dt_check_need_upload(args: List[str], environment: ChallengeEnvironment):
    """ Checks if we need to upload the given library. """
    _ = environment
    return aido_check_need_upload_main(args=args)


def dt_push_container(args: List[str], environment: ChallengeEnvironment):
    """ Pushes the container created using aido-build-container."""
    parser = argparse.ArgumentParser(prog=environment.prog)
    parser.add_argument("-C", dest="directory", default=".")
    parser.add_argument("--use-name", default=None, help="forces container name")
    parser.add_argument("--use-branch", default=None, help="forces branch name")
    parser.add_argument("--use-org", default=None, help="forces org name")
    parser.add_argument("--force", default=False, action="store_true")
    args = parser.parse_args(args)

    di = get_dir_info_exceptions(os.getcwd())
    registry = os.environ.get(ENV_REGISTRY, IMPORTANT_ENVS[ENV_REGISTRY])
    tag = get_tag_from_dirinfo(
        registry, di, use_name=args.use_name, use_branch=args.use_branch, use_org=args.use_org
    )
    if args.force:
        client = DockerClient.from_env()
        docker_push_retry(client, tag, credentials=environment.docker_credentials)
    else:
        docker_push_optimized(tag, credentials=environment.docker_credentials)


def get_tag_from_dirinfo(
    registry: str, di: DirInfo, use_name: Optional[str], use_branch: Optional[str], use_org: Optional[str]
) -> DockerCompleteImageName:
    if use_name is None:
        use_name = di.repo_name.lower()
    if use_branch is None:
        use_branch = di.branch.lower()
    if use_org is None:
        use_org = di.org_name.lower()
    arch = "amd64"
    tag = f"{registry}/{use_org}/{use_name}:{use_branch}-{arch}"

    return DockerCompleteImageName(tag)


def dt_build_container(args: List[str], environment: ChallengeEnvironment):
    """ Checks if we need to upload the given library. """

    parser = argparse.ArgumentParser(prog=environment.prog)

    parser.add_argument(
        "--ignore-dirty",
        default=ENV_IGNORE_DIRTY in os.environ,
        action="store_true",
        help=f"Also set by env {ENV_IGNORE_DIRTY}.",
    )
    parser.add_argument(
        "--ignore-untagged",
        default=ENV_IGNORE_UNTAGGED in os.environ,
        action="store_true",
        help=f"Also set by env {ENV_IGNORE_UNTAGGED}.",
    )
    parser.add_argument("--use-org", default=None, help="forces org name")
    parser.add_argument("--use-name", default=None, help="forces container name")
    parser.add_argument("--use-branch", default=None, help="forces branch name")
    parser.add_argument("--force-login", action="store_true", default=False)
    parser.add_argument("-C", dest="directory", default=".")

    args = parser.parse_args(args)

    ignore_dirty = args.ignore_dirty
    ignore_untagged = args.ignore_untagged
    dirname = args.directory  # os.path.join(os.getcwd(), args.directory)
    dirname_abs = os.path.realpath(dirname)
    # return aido_check_need_upload_main(args=args)
    di = get_dir_info_exceptions(dirname_abs)
    if (not ignore_dirty) and di.dirty:
        msg = "Directory is dirty"
        raise ZException(msg, dirname=dirname_abs, di=di)
    if (not ignore_untagged) and not di.tag:
        msg = "Git commit is not tagged"
        raise ZException(msg, dirname=dirname_abs, di=di)
    # logger.info(di=di)

    update_versions()
    build_vars = {}
    for k in ["PIP_INDEX_URL", ENV_REGISTRY]:
        default = IMPORTANT_ENVS[k]
        if k in os.environ:
            v = os.environ[k]
        else:
            logger.warn(f"No variable {k} set.")
            v = default
        build_vars[k] = v
    labels = get_duckietown_labels(dirname)
    #
    # args = get_build_args_from_labels(labels)
    # for k, v in build_vars.items():
    #     args.append()
    #
    pull = True
    if "DT_DOCKER_BUILD_HOST" in os.environ:
        host = os.environ["DT_DOCKER_BUILD_HOST"]
        env = dict(DOCKER_HOST=host)
        if "ssh" in host:
            ssh_config = os.path.expanduser("~/.ssh")
            if not os.path.exists(ssh_config):
                logger.error(f"Cannot find {ssh_config}")
            else:
                config = os.path.join(ssh_config, "config")

                logger.info(fs2=list(os.listdir(ssh_config)), config=read_ustring_from_utf8_file(config))
        logger.info(f"BUilding on remote host {host}")
    else:
        env = os.environ
    client = DockerClient.from_env(environment=env)
    registry = build_vars[ENV_REGISTRY]
    tag = get_tag_from_dirinfo(
        registry, di, use_name=args.use_name, use_org=args.use_org, use_branch=args.use_branch
    )

    logger.info(tag=tag)
    dockerfile = os.path.join(dirname, "Dockerfile")
    dockerfile_contents = read_ustring_from_utf8_file(dockerfile)
    credentials = environment.docker_credentials
    log_in_for_build(dockerfile_contents, credentials)
    if pull:
        pull_for_build(client, dockerfile_contents, credentials, quiet=False)
    args = dict(
        path=dirname,
        tag=tag,
        pull=False,
        buildargs=build_vars,
        labels=labels,
        # dockerfile=dockerfile
    )
    try:
        run_build(client, **args)
    except BuildFailed:
        raise

    v = get_version_info(dirname_abs)
    if v is not None:
        image = client.images.get(tag)
        br = parse_complete_tag(tag)
        # br.tag = v
        tag_notag = get_complete_tag_notag(br)
        # tag2 = get_complete_tag(br)
        # logger.info("tagging version", tag=tag, new=f"{tag_notag}:{v}")
        image.tag(repository=tag_notag, tag=br.tag + "-" + v)


def get_version_info(dn: str) -> Optional[str]:
    fn = os.path.join(dn, ".bumpversion.cfg")
    if not os.path.exists(fn):
        return None
    config = ConfigParser()
    config.read(fn)
    if "bumpversion" not in config:
        return None

    if "current_version" not in config["bumpversion"]:
        return None

    return config["bumpversion"]["current_version"]


def bump(args: List[str], environment: ChallengeEnvironment):
    from bumpversion.cli import main

    _ = environment
    main(args)
