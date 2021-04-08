import json
import os
import traceback
from copy import deepcopy
from dataclasses import dataclass, replace
from functools import lru_cache
from typing import cast, Dict, List, Optional, Sequence

import yaml
from docker import DockerClient
from zuper_commons.fs import (
    AbsDirPath,
    AbsFilePath,
    DirPath,
    read_ustring_from_utf8_file,
    write_ustring_to_utf8_file,
)
from zuper_ipce import IESO, ipce_from_object

import duckietown_challenges
from duckietown_build_utils import (
    BuildFailed,
    BuildResult,
    CannotGetVersions,
    docker_caching,
    docker_pull_retry,
    docker_push_optimized,
    docker_push_retry,
    DockerCompleteImageName,
    DockerCredentials,
    DockerOrganizationName,
    DockerRegistryName,
    DockerRepositoryName,
    DockerTag,
    get_complete_tag,
    get_complete_tag_notag,
    get_duckietown_labels,
    get_important_env_build_args_dict,
    get_last_version_fresh,
    get_python_packages_versions,
    log_in_for_build,
    parse_complete_tag,
    pull_for_build,
    run_build,
    VersionInfo,
)
from duckietown_challenges import (
    ChallengeDescription,
    ChallengeName,
    ChallengesConstants,
    ChallengeStep,
    dtserver_challenge_define,
    from_steps_transitions,
    get_registry_info,
    STATE_ERROR,
    STATE_FAILED,
    STATE_START,
    STATE_SUCCESS,
    StepName,
    UserID,
    ZException,
    ZValueError,
)
from duckietown_challenges.challenge import AndCondition, Condition
from duckietown_docker_utils import replace_important_env_vars
from . import logger

__all__ = ["dts_define", "get_package_to_version"]


def check_watchtower_not_running():
    client = DockerClient.from_env()
    containers = client.containers.list()
    for container in containers:
        if "watchtower" in container.name:
            logger.warn("you cannot do build work while using the watchtower container")


@lru_cache(maxsize=None)
def get_last_version_cached(pname: str) -> str:
    return get_last_version_fresh(pname)


@dataclass
class Replication:
    step_name: StepName
    ntimes: int


def dts_define(
    *,
    token: str,
    impersonate: Optional[UserID],
    challenge: ChallengeDescription,
    force_invalidate: bool,
    steps: str,
    dopull: bool,
    base: DirPath,
    client: DockerClient,
    no_cache: bool,
    credentials: DockerCredentials,
    replicate: Sequence[Replication] = (),
):
    check_watchtower_not_running()
    ri = get_registry_info(token=token, impersonate=impersonate)
    # logger.info(f"impersonate {impersonate}")
    if steps:
        use_steps = steps.split(",")
    else:
        use_steps = list(challenge.steps)
    registry = os.environ.get("AIDO_REGISTRY", ri.registry)

    if replicate:
        for r in replicate:
            replicated_names = []
            step_name: StepName = r.step_name
            ntimes: int = r.ntimes
            if not step_name in challenge.steps:
                msg2 = "Cannot find step name"
                raise ZValueError(msg2, step_name=step_name, available=list(challenge.steps))
            s = challenge.steps.pop(step_name)
            for i in range(ntimes):
                s2: ChallengeStep = deepcopy(s)
                for k, v in s2.evaluation_parameters.services.items():
                    v.environment["replica"] = json.dumps(dict(index=i, total=ntimes))
                name2 = cast(StepName, f"{step_name}-{i}of{ntimes}")
                challenge.steps[name2] = s2
                replicated_names.append(name2)

            transitions = []
            for a in replicated_names:
                transitions.append([STATE_START, "success", a])
                transitions.append([a, "failed", STATE_FAILED])
                transitions.append([a, "error", STATE_ERROR])

            allof = ",".join(replicated_names)
            transitions.append([allof, "success", STATE_SUCCESS])
            challenge.transitions = transitions

        use_steps = list(challenge.steps)
        logger.info(steps=challenge.steps)

    challenge.ct = from_steps_transitions(use_steps, challenge.transitions)
    logger.info("Transitions", challenge=challenge)

    use_steps = cast(List[StepName], use_steps)
    for step_name in use_steps:
        if step_name not in challenge.steps:
            msg = f'Could not find step "{step_name}" in {list(challenge.steps)}.'
            raise Exception(msg)
        step = challenge.steps[step_name]

        services = step.evaluation_parameters.services
        for service_name, service in services.items():
            complete = get_image_name_for_service(
                challenge_name=challenge.name,
                step_name=step_name,
                service_name=service_name,
                registry=registry,
                credentials=credentials,
            )
            if service.build:
                context = os.path.join(base, service.build.context)

                if not os.path.exists(context):
                    msg = f"Context does not exist."
                    raise ZException(msg, context=context)

                # XXX not sure about this
                context_abs = os.path.abspath(context)

                if service.build.dockerfile is None:
                    use_dockerfile = os.path.join(context_abs, "Dockerfile")
                else:

                    dockerfile = service.build.dockerfile

                    base_abs = os.path.abspath(base)
                    dockerfile_abs = os.path.join(base_abs, dockerfile)
                    if not os.path.exists(dockerfile_abs):
                        msg = f"Cannot find Dockerfile"
                        raise ZException(msg, base=base, dockerfile=dockerfile, dockerfile_abs=dockerfile_abs)

                    logger.debug(
                        context=context,
                        dockerfile=dockerfile,
                        context_abs=context_abs,
                        dockerfile_abs=dockerfile_abs,
                    )
                    use_dockerfile = dockerfile_abs
                args = service.build.args
                # if args:
                #     logger.warning(f"arguments not supported yet: {args}")

                br = build_image(
                    client,
                    path=context_abs,
                    complete=complete,
                    filename=use_dockerfile,
                    no_cache=no_cache,
                    dopull=dopull,
                    args=args,
                    credentials=credentials,
                )
                assert br.digest is not None, br
                service.image = get_complete_tag_notag(br)

                # very important: get rid of it!
                service.build = None
            else:
                if service.image == ChallengesConstants.SUBMISSION_CONTAINER_TAG:
                    pass
                else:
                    if service.image:
                        service.image = replace_important_env_vars(service.image)

                        # logger.info(service=service)
                        service_image_name = DockerCompleteImageName(service.image)
                        # br = parse_complete_tag(service_image_name)
                        # if br.digest is None:
                        #     # msg = f"Finding digest for image {service.image}"
                        #     # logger.warning(msg, br=br)

                        dpr = docker_pull_retry(
                            client,
                            service_image_name,
                            ntimes=10,
                            wait=10,
                            quiet=False,
                            credentials=credentials,
                        )

                        im = client.images.get(dpr.complete_image_name)

                        c = parse_complete_tag(complete)
                        try:
                            when, digest = docker_caching.get_last_image_push(
                                c.registry, c.organization, c.repository, im.id
                            )
                            logger.info("can reuse upload info")
                        except KeyError:
                            im.tag(get_complete_tag_notag(c), tag=c.tag)

                            digest = docker_push_retry(client, complete, credentials)

                        c2 = replace(c, digest=digest, tag=None)
                        service.image = get_complete_tag_notag(c2)

            logger.debug(f" {service_name} ->  {service.image}")

        do_read_versions = False

        for service_name, service in services.items():
            if not do_read_versions:
                continue

            if service.image == ChallengesConstants.SUBMISSION_CONTAINER_TAG:
                continue

            logger.info(service_name=service_name, image=service.image)

            try:
                versions = get_python_packages_versions(service.image, "/tmp/duckietown")
            except CannotGetVersions as e:
                msg = f"Cannot get versions for service {service_name} - skipping."
                logger.warning(msg, e=traceback.format_exc())
                continue
            # myversions = get_package_to_version()

            freshes = {}
            interesting = {}
            for k, his in versions.items():
                if not interesting_to_compare(k):
                    continue

                fresh = get_last_version_cached(k)
                freshes[k] = fresh
                #
                # found[k] = his
                # if k not in myversions:
                #     continue

                # mine = myversions[k]
                if fresh != his["version"]:
                    msg = f'service {service_name} mismatch for "{k}"'
                    logger.error(msg, mine=fresh, his=his)

                interesting[k] = his["version"]
            logger.info(service_name=service_name, interesting=interesting, freshes=freshes)

    logger.info("zipping challenge...", v=duckietown_challenges.__version__, a=AndCondition.__annotations__)
    ieso = IESO(with_schema=False)
    assert challenge.date_close.tzinfo is not None, (challenge.date_close, challenge.date_open)
    assert challenge.date_open.tzinfo is not None, (challenge.date_close, challenge.date_open)
    # logger.info(challenge_to_upload=challenge)
    ipce = ipce_from_object(challenge, ChallengeDescription, ieso=ieso)
    data2 = yaml.dump(ipce)

    logger.info("uploading challenge", ipce=ipce)
    fn = os.path.join("out", "defined", f"{challenge.name}.challenge_description.yaml")
    write_ustring_to_utf8_file(data2, fn)

    res = dtserver_challenge_define(token, data2, force_invalidate=force_invalidate, impersonate=impersonate)
    challenge_id = res["challenge_id"]
    steps_updated = res["steps_updated"]

    if steps_updated:
        logger.info(
            f"The following steps of {challenge_id} were updated and will be invalidated.",
            steps_updated=steps_updated,
        )
        # for step_name, reason in steps_updated.items():
        #     logger.info("\n\n" + indent(reason, " ", step_name + "   "))
    else:
        msg = "No update needed - the container digests did not change."
        logger.info(msg)
    return challenge


def interesting_to_compare(package_name: str) -> bool:
    return (
        "dt" in package_name or "duckietown" in package_name or "aido" in package_name or "zu" in package_name
    )


def get_package_to_version() -> Dict[str, VersionInfo]:
    # noinspection PyBroadException
    try:
        # noinspection PyCompatibility,PyUnresolvedReferences
        from pip import get_installed_distributions
    except:
        # noinspection PyCompatibility,PyProtectedMember,PyProtectedMember
        from pip._internal.utils.misc import get_installed_distributions

    packages = {}
    for i in get_installed_distributions(local_only=False):
        # print(i.__dict__)

        # noinspection PyProtectedMember
        pkg = {
            # 'project_name': i.project_name,
            "version": i._version,
            "location": i.location,
        }
        packages[i.project_name] = pkg

        # assert isinstance(i, (pkg_resources.EggInfoDistribution, pkg_resources.DistInfoDistribution))

    ps = sorted(packages)
    packages = {k: packages[k] for k in ps}
    return packages


def get_image_name_for_service(
    challenge_name: ChallengeName,
    step_name: StepName,
    service_name: str,
    registry: DockerRegistryName,
    credentials: DockerCredentials,
) -> DockerCompleteImageName:
    if registry not in credentials:
        msg = f"Need credentials for {registry}"
        raise ZValueError(msg, known=list(credentials))
    username = credentials[registry]["username"]
    #
    # d = datetime.datetime.now()
    # tag_date = tag_from_date(d)
    tag = DockerTag(f"{challenge_name}-{step_name}-{service_name}".lower())
    repository_ = DockerRepositoryName("duckietown-challenges")
    organization = cast(DockerOrganizationName, username.lower())

    br = BuildResult(
        repository=repository_, organization=organization, registry=registry, tag=tag, digest=None,
    )
    complete = get_complete_tag(br)
    return complete


def build_image(
    client: DockerClient,
    path: AbsDirPath,
    complete: DockerCompleteImageName,
    filename: AbsFilePath,
    no_cache: bool,
    dopull: bool,
    args: Dict[str, str],
    credentials: DockerCredentials,
) -> BuildResult:
    dockerfile = read_ustring_from_utf8_file(filename)

    labels = get_duckietown_labels(path)

    log_in_for_build(dockerfile, credentials)
    if dopull:
        pull_for_build(client, dockerfile, credentials, quiet=False)

    all_build_args = {}
    all_build_args.update(args)
    all_build_args.update(get_important_env_build_args_dict(dockerfile))

    args = dict(
        path=path,
        tag=complete,
        pull=False,
        buildargs=all_build_args,
        labels=labels,
        nocache=no_cache,
        dockerfile=filename,
    )
    try:
        run_build(client, **args)
    except BuildFailed:
        raise

    digest = docker_push_optimized(complete, credentials=credentials)

    br = parse_complete_tag(digest)
    # br.tag = tag_date
    return br
