import argparse
import os
from typing import cast, Dict, List, Optional
from urllib.request import urlretrieve

import yaml
from zuper_commons.fs import DirPath, write_ustring_to_utf8_file
from zuper_commons.text import wildcard_to_regexp

from duckietown_challenges import (
    ArtefactDict,
    d8n_make_sure_dir_exists,
    dtserver_get_info,
    dtserver_get_job,
    dtserver_get_submissions,
    JobID,
    RPath,
    SubmissionID,
    ZException,
)
from duckietown_challenges.utils import friendly_size
from duckietown_challenges_runner.runner_cache import copy_to_cache, get_file_from_cache
from . import logger
from .cli_common import ChallengeEnvironment, wrap_server_operations

__all__ = ["dt_challenges_cli_download"]


def dt_challenges_cli_download(args: List[str], environment: ChallengeEnvironment):
    """ Lists submissions on the server. """

    parser = argparse.ArgumentParser(prog="", usage="")
    parser.add_argument("--job", required=False, type=int)
    parser.add_argument("--submission", required=False, type=int)
    parser.add_argument("--challenge", required=False, type=str)
    parser.add_argument("--patterns", required=False, type=str, default="*.*")
    parser.add_argument("--flatten", default=False, action="store_true")
    parser.add_argument("--out", default=None, required=True)
    parsed = parser.parse_args(args)

    token = environment.token

    outd = parsed.out
    n = 0
    n += 1 if parsed.job else 0
    n += 1 if parsed.submission else 0
    n += 1 if parsed.challenge else 0
    if n != 1:
        msg = "Please specify exactly one of --job, --submission, --challenge"
        raise ZException(msg, argargs=args)
    if parsed.job:
        job_id = cast(JobID, parsed.job)
        with wrap_server_operations():
            res = dtserver_get_job(token, job_id=job_id)
        out = os.path.join(outd, "jobs", str(job_id))
        artefacts = res["artefacts"]
        download_artefacts_url(artefacts, out, patterns=parsed.patterns, flatten=parsed.flatten, prefix="")
        return
    if parsed.submission:
        submission_id = cast(SubmissionID, parsed.submission)
        subinfo = dtserver_get_info(token, submission_id)
        logger.info(subinfo=subinfo)
        user_id = subinfo["user_id"]
        step2job = subinfo["status-details"]["step2job"]

        for step_name, job_id in step2job.items():
            with wrap_server_operations():
                res = dtserver_get_job(token, job_id=job_id)

            out = os.path.join(outd, "submissions", f"sub-{submission_id}-user-{user_id}")

            artefacts = res["artefacts"]
            if parsed.flatten:
                prefix = step_name + "-"
            else:
                prefix = step_name + "/"
            download_artefacts_url(
                artefacts, out, patterns=parsed.patterns, prefix=prefix, flatten=parsed.flatten
            )
    from multiprocessing import Pool

    if parsed.challenge:
        challenge_names = parsed.challenge.split(",")
        with Pool(16) as pool:
            for challenge_name in challenge_names:
                res = dtserver_get_submissions(token=token, challenge_name=challenge_name, user_id=None)
                logger.info(submissions=list(res))
                # cd: ChallengeDescription = get_challenge_description(token, challenge_name)
                for submission_id, _ in res.items():
                    # noinspection PyTypeChecker
                    subinfo = dtserver_get_info(token, submission_id)

                    user_id = subinfo["user_id"]
                    out = os.path.join(
                        outd, "challenges", challenge_name, f"sub-{submission_id}-user-{user_id}"
                    )

                    write_ustring_to_utf8_file(yaml.dump(subinfo), out + ".yaml")
                    status_details = subinfo.get("status-details", None)
                    if status_details is None:
                        logger.warning(f"no status for {submission_id}")
                        continue

                    if status_details["complete"]:
                        write_ustring_to_utf8_file("This submission is complete", out + "/COMPLETE.txt")
                    step2job = subinfo["status-details"]["step2job"]

                    for step_name, job_id in step2job.items():
                        with wrap_server_operations():
                            res = dtserver_get_job(token, job_id=job_id)
                        if res["status"] != "success":
                            continue
                        # noinspection PyTypedDict
                        artefacts = res.pop("artefacts")
                        # logger.info(job_info=res, arts=list(artefacts))
                        if parsed.flatten:
                            challenge_name2 = challenge_name
                            challenge_name2 = challenge_name2.replace("aido5-", "")
                            challenge_name2 = challenge_name2.replace("-validation", "")

                            challenge_name2 = challenge_name2.replace("-", "")
                            # [challenge] - [sub] - [user] - [step] - [job] - [robot name] - camera.mp4
                            prefix = f"{challenge_name2}-{submission_id}-{user_id}-{step_name}-{job_id}" + "-"
                        else:
                            prefix = step_name + "/"

                        pool.apply_async(
                            download_artefacts_url,
                            (artefacts, out),
                            dict(patterns=parsed.patterns, prefix=prefix, flatten=parsed.flatten),
                        )
            logger.info("waiting...")
            pool.close()
            pool.join()


def download_artefacts_url(
    artefacts: Dict[RPath, ArtefactDict], out: DirPath, patterns: Optional[str], flatten: bool, prefix: str
):
    naccepted = 0
    for rpath, artefact in artefacts.items():
        if not pattern_matches(patterns, rpath):
            # logger.debug(f'Not downloading {rpath}')
            continue
        if "tmp" in rpath:
            continue
        naccepted += 1
        if flatten:
            dest = os.path.join(out, prefix + rpath.replace("/", "_"))

            dest = dest.replace("challenge-evaluation-output_", "")
            dest = dest.replace("-camera_node-image-compressed", "")
            dest = dest.replace("_watchtowers", "")
            dest = dest.replace("_watchtower", "")
            dest = dest.replace("_robot_autobot01", "")
            dest = dest.replace("_robot_autobot02", "")
            dest = dest.replace("_robot_autobot03", "")
            dest = dest.replace("_robot_autobot04", "")
            # dest = dest.replace('-camera', '')
            dest = dest.replace("-robots_", "-")
            dest = dest.replace("-visualize", "")
            dest = dest.replace("-isualization_sync_", "-")
            # for _ in ['01','02','03', '04']
            for i in reversed(range(300)):
                f = f"{i:02d}"
                dest = dest.replace(f + f + ".mp4", f + ".mp4")
            dest = dest.replace("-videos", "")
        else:
            dest = os.path.join(out, prefix + rpath)

        sha256hex = artefact["sha256hex"]
        size = artefact["size"]
        fs = friendly_size(size)
        if os.path.exists(dest):
            logger.debug(f"found    {fs:>7}   {dest}")
            continue
        logger.debug(dest=dest)
        d8n_make_sure_dir_exists(dest)

        try:
            get_file_from_cache(dest, sha256hex)

            logger.debug(f"cache   {fs:>7}   {dest}")
        except KeyError:

            if "s3" in artefact["storage"]:
                url = artefact["storage"]["s3"]["url"]

                tmp = dest + ".tmp"
                logger.info(f"get    {fs:>7}   {dest}")
                urlretrieve(url, tmp)
                logger.info(url=url, retrieving=tmp)
                os.rename(tmp, dest)

                copy_to_cache(dest, sha256hex)
            else:
                logger.debug("cannot get file")
    logger.info(
        "finished", out=out, prefix=prefix, patterns=patterns, nartefacts=len(artefacts), naccepted=naccepted
    )


def pattern_matches(wildcard: str, s: str):
    patterns = wildcard.split(",")
    for wildcard in patterns:
        regexp = wildcard_to_regexp(wildcard)
        if regexp.match(s) is not None:
            return True
    return False
