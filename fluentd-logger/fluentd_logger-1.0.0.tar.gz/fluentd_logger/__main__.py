#!/usr/bin/env python3

import click

__author__ = "Catalin Dinuta"

from fluent import sender

from .cli_constants import CLIConstants
from .env_constants import EnvConstants
from .environment import EnvironmentSingleton
from .logger import Logger
from .io_utils import IOUtils


@click.command()
@click.option('--tag', prompt='tag',
              help='Fluentd tag used to log the message. E.g. agent')
@click.option('--label', prompt='name',
              help='The label we use to log the information. E.g. api')
@click.option('--file', prompt='file',
              help='The json file which contains the message(s). E.g. results.json')
@click.option('--fluentd', default=None, help='The fluentd instance location in "ip:port" format. E.g. localhost:24224')
def cli(tag, label, file, fluentd):
    env = EnvironmentSingleton.get_instance()
    fluentd = fluentd if fluentd is not None else env.get_env_and_virtual_env().get(EnvConstants.FLUENTD_IP_PORT)
    app_label = label if label is not None else env.get_env_and_virtual_env().get(EnvConstants.LABEL)
    tag = tag if tag is not None else env.get_env_and_virtual_env().get(EnvConstants.TAG)

    if app_label is None:
        raise Exception(
            "Fluentd label was not set."
            "Please set option '--label' using this CLI or set the 'LABEL' environment variable \n")

    if tag is None:
        raise Exception(
            "Fluentd tag was not set."
            "Please set option '--tag' using this CLI or set the 'TAG' environment variable \n")

    if fluentd is None:
        raise Exception(
            "Fluentd ip:port location was not detected in command and neither environment variable "
            "" + EnvConstants.FLUENTD_IP_PORT + "\n" +
            "Please set option '--fluentd' using this CLI or set the 'FLUENTD_IP_PORT' environment variable \n")

    logger = sender.FluentSender(tag=tag, host=fluentd.split(":")[0], port=int(fluentd.split(":")[1]))
    service = Logger(logger)

    try:
        messages = IOUtils.read_dict_from_file(file=file)
        if isinstance(messages, list):
            for message in messages:
                click.echo(service.emit(app_label=app_label, msg=message))
        elif isinstance(messages, dict):
            click.echo(service.emit(app_label=app_label, msg=messages))
        else:
            raise Exception("Could not deserialize to a List of Dicts / Dict")
    except Exception as e:
        click.echo(f"Exception {e.__str__()}")
        exit(CLIConstants.FAILURE)

    exit(CLIConstants.SUCCESS)


if __name__ == "__main__":
    cli()
