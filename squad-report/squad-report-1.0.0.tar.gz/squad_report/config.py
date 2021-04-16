import yaml
import pprint
import os
from os.path import expanduser
from squad_report.logging import getLogger

logger = getLogger(__name__)


class Config:
    squad_group = None
    squad_project = None
    email_from = "LKFT <lkft@linaro.org>"
    email_to = None
    email_cc = None
    email_subject = None
    reported_tested_by = "Linux Kernel Functional Testing <lkft@linaro.org>"
    signature_name = "Linaro LKFT"
    signature_url = "https://lkft.linaro.org"
    filter_suites = None
    filter_suite_prefixes = None
    filter_environments = None
    filter_environment_prefixes = None
    template = None
    output = None


def setup_config(args):
    yaml_dict = None
    config = Config()

    config.squad_group = args.group
    config.squad_project = args.project
    config.email_from = args.email_from
    config.email_to = args.email_to
    config.email_cc = args.email_cc
    config.email_subject = args.email_subject
    config.filter_suites = args.suites
    config.filter_suite_prefixes = args.suite_prefixes
    config.filter_environments = args.environments
    config.filter_environment_prefixes = args.environment_prefixes
    config.template = args.template
    config.output = args.output

    config_file = "~/.config/squad_report/config.yaml"
    if (
        not os.path.exists((expanduser(config_file)))
        and args.config_report_type is None
    ):
        logger.info("No config file")
    else:
        parser = yaml.safe_load
        with open(expanduser(config_file), "r") as fh:
            try:
                yaml_dict = parser(fh)
            except yaml.YAMLError as e:
                raise SystemExit(e)

        for report in yaml_dict.get("report"):
            if report.get("name") == args.config_report_type:
                logger.debug(pprint.pformat(args.config_report_type))
                config.squad_group = config.squad_group or report.get("squad_group")
                config.squad_project = config.squad_project or report.get(
                    "squad_project"
                )
                config.email_from = config.email_from or report.get("email_from")
                config.email_to = config.email_to or report.get("email_to")
                config.email_cc = config.email_cc or report.get("email_cc", "")
                config.email_subject = config.email_subject or report.get(
                    "email_subject"
                )
                config.reported_tested_by = report.get("reported_tested_by")
                config.signature_name = report.get("sig_name")
                config.signature_url = report.get("sig_url")
                config.filter_suites = config.filter_suites or report.get(
                    "filter_suites"
                )
                config.filter_suite_prefixes = (
                    config.filter_suite_prefixes or report.get("filter_suite_prefixes")
                )
                config.filter_environments = config.filter_environments or report.get(
                    "filter_environments"
                )
                config.filter_environment_prefixes = (
                    config.filter_environment_prefixes
                    or report.get("filter_environment_prefixes")
                )
                config.template = report.get("template")
                config.output = report.get("output")

                logger.debug(pprint.pformat(config))
    return config
