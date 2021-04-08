import argparse
import dataclasses
import json
import os
from typing import cast, Dict, List, Optional

import termcolor
from zuper_commons.types import ZValueError

from duckietown_build_utils import DockerRegistryName
from duckietown_challenges import (
    dtserver_get_compatible_challenges,
    dtserver_submit2,
    get_duckietown_server_url,
    get_registry_info,
    InvalidConfiguration,
    Submit2ResponseDict,
    SubmitDataDict,
)
from duckietown_challenges.submission_read import read_submission_info
from . import logger
from .cli_common import ChallengeEnvironment, sprint, wrap_server_operations
from .cmd_submit_build import submission_build

__all__ = ["dt_challenges_cli_submit"]


def dt_challenges_cli_submit(args: List[str], environment: ChallengeEnvironment):
    """ Make a submission """
    prog = "dts challenges submit"
    usage = """


    Submission:

        %(prog)s --challenge NAME



    ## Building options

    Rebuilds ignoring Docker cache

        %(prog)s --no-cache



    ## Attaching user data

    Submission with an identifying label:

        %(prog)s --user-label  "My submission"

    Submission with an arbitrary JSON payload:

        %(prog)s --user-meta  '{"param1": 123}'




    """
    parser = argparse.ArgumentParser(prog=prog, usage=usage)

    group = parser.add_argument_group("Submission identification")
    parser.add_argument("--challenge", help="Specify challenge name.", default=None)
    group.add_argument(
        "--user-label", dest="message", default=None, type=str, help="Submission message",
    )
    group.add_argument(
        "--user-meta",
        dest="metadata",
        default=None,
        type=str,
        help="Custom JSON structure to attach to the submission",
    )

    group = parser.add_argument_group("Building settings.")

    group.add_argument("--no-cache", dest="no_cache", action="store_true", default=False)
    group.add_argument("--no-pull", dest="no_pull", action="store_true", default=False)
    group.add_argument("--impersonate", type=int, default=None)

    group.add_argument(
        "--retire-same-label",
        action="store_true",
        default=False,
        help="Retire my submissions with the same label.",
    )

    group.add_argument(
        "--priority", type=int, default=50, help="Adjust priority",
    )

    group.add_argument("-C", dest="cwd", default=None, help="Base directory")

    parsed = parser.parse_args(args)

    pull = not parsed.no_pull
    impersonate = parsed.impersonate
    if parsed.cwd is not None:
        logger.info("Changing to directory %s" % parsed.cwd)

        if not os.path.exists(parsed.cwd):
            msg = "Directory to change to does not exist."
            raise ZValueError(msg, cwd=parsed.cwd)
        os.chdir(parsed.cwd)

    if not os.path.exists("submission.yaml"):
        msg = "Expected a submission.yaml file in %s." % (os.path.realpath(os.getcwd()))
        raise InvalidConfiguration(msg)

    priority: int = int(parsed.priority)

    sub_info = read_submission_info(".")

    token = environment.token
    # logger.info(f"token: {token}")

    with wrap_server_operations():
        ri = get_registry_info(token=token, impersonate=impersonate)

        registry = cast(DockerRegistryName, ri.registry)

        compat = dtserver_get_compatible_challenges(
            token=token, impersonate=impersonate, submission_protocols=sub_info.protocols,
        )
        if not compat.compatible:
            msg = (
                f"There are no compatible challenges with protocols {sub_info.protocols},\n"
                " or you might not have the necessary permissions."
            )
            raise InvalidConfiguration(msg)

        if parsed.message:
            sub_info.user_label = parsed.message
        if parsed.metadata:
            sub_info.user_metadata = json.loads(parsed.metadata)
        if parsed.challenge:
            sub_info.challenge_names = parsed.challenge.split(",")
        if sub_info.challenge_names is None:
            msg = "You did not specify a challenge. I will use the first compatible one."
            sprint(msg)
            sub_info.challenge_names = [list(compat.compatible)[0]]

        if sub_info.challenge_names == ["all"]:
            sub_info.challenge_names = compat.compatible

        sprint(f"I will submit to the challenges {sub_info.challenge_names}")

        for c in sub_info.challenge_names:
            if not c in compat.available_submit:
                msg = f"The challenge {c!r} does not exist among available."
                raise InvalidConfiguration(msg, compat=list(compat.available_submit))
            if not c in compat.compatible:
                msg = 'The challenge "%s" is not compatible with protocols %s .' % (c, sub_info.protocols,)
                raise InvalidConfiguration(msg)

        sprint("")
        sprint("")
        br = submission_build(
            credentials=environment.docker_credentials, registry=registry, no_cache=parsed.no_cache, pull=pull
        )

        retire_same_label: bool = parsed.retire_same_label and (sub_info.user_label is not None)
        # data_send: SubmitDataDict
        image: object = dataclasses.asdict(br)
        user_label: Optional[str] = sub_info.user_label
        user_payload: Dict[str, object] = sub_info.user_metadata
        protocols: List[str] = sub_info.protocols
        # XXX: not sure why it complains...
        # noinspection PyTypeChecker
        data_send: SubmitDataDict = {
            "image": image,
            "user_label": user_label,
            "user_payload": user_payload,
            "protocols": protocols,
            "retire_same_label": retire_same_label,
            "user_priority": priority,
        }

        #   image: object
        #     user_label: Optional[str]
        #     user_payload: Dict[str, object]
        #     protocols: List[str]
        #     retire_same_label: bool
        #     user_priority: int

        submit_to_challenges = sub_info.challenge_names

        data: Submit2ResponseDict
        data = dtserver_submit2(
            token=token, challenges=submit_to_challenges, data=data_send, impersonate=impersonate,
        )

        # sprint('obtained:\n%s' % json.dumps(data, indent=2))
        component_id = data["component_id"]
        _ = component_id
        submissions = data["submissions"]
        # url_component = href(get_duckietown_server_url() + '/humans/components/%s' % component_id)

        # msg = f"""
        #
        # Successfully created component.
        #
        # This component has been entered in {len(submissions)} challenge(s).
        #
        #         """
        #
        msg = ""

        for challenge_name, sub_info2 in submissions.items():
            submission_id = sub_info2["submission_id"]
            existing = sub_info2.get("existing", False)
            challenge_title = sub_info2["challenge"]["title"]
            challenge_name = sub_info2["challenge"]["queue_name"]
            url_submission = href(get_duckietown_server_url() + f"/humans/submissions/{submission_id}")

            if existing:
                msg += f"""
        You already have an identical submission {submission_id} for challenge {challenge_name}.
        Inspect it at: {url_submission}
                """
                continue

            submission_id_color = termcolor.colored(submission_id, "cyan")
            P = dark("$")
            head = bright(f"## Challenge {challenge_name} - {challenge_title}")
            msg += (
                "\n\n"
                + f"""

        {head}

        Track this submission at:

            {url_submission}

        You can follow its fate using:

            {P} dts challenges follow --submission {submission_id_color}

        You can speed up the evaluation using your own evaluator:

            {P} dts challenges evaluator --submission {submission_id_color}

        """.strip()
            )
            manual = href("https://docs.duckietown.org/daffy/AIDO/out/")
            msg += f"""

        For more information, see the manual at {manual}
        """

        sprint(msg)

    extra = set(submissions) - set(submit_to_challenges)

    if extra:
        msg = f"""
    Note that the additional {len(extra)} challenges ({cute_list(extra)}) are required checks
    before running the code on the challenges you chose ({cute_list(submit_to_challenges)}).
    """
        sprint(msg)


def cute_list(x):
    return ", ".join(x)


def bright(x):
    return termcolor.colored(x, "blue")


def dark(x):
    return termcolor.colored(x, attrs=["dark"])


def href(x):
    return termcolor.colored(x, "blue", attrs=["underline"])
