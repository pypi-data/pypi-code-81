import os
import sys
import logging
import click

from mldock.platform_helpers.docker.auth import login_and_authenticate
from mldock.api.local import \
    docker_build
from mldock.api.cloud import \
    push_image_to_repository, pull_image_from_repository
from mldock.config.config_manager import \
    MLDockConfigManager

click.disable_unicode_literals_warning = True
logger=logging.getLogger('mldock')

def reset_terminal():
    # os.system("clear")
    click.clear()

@click.group()
def cloud():
    """
    Commands for cloud operations
    """
    pass

@click.command()
@click.option(
    '--dir',
    help='Set the working directory for your mldock container.',
    required=True,
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        writable=True,
        readable=True,
        resolve_path=False,
        allow_dash=False,
        path_type=None
    )
)
@click.option('--no-cache', help='builds container from scratch', is_flag=True)
@click.option(
    '--build',
    help='Set the working directory for your mldock container.',
    is_flag=True
)
@click.option(
    '--provider',
    help='Set the cloud provider',
    required=True,
    type=click.Choice(['ecr', 'gcr', 'dockerhub'],
    case_sensitive=False
    )
)
@click.option(
    '--region',
    help='Set the registry region',
    default=None,
    type=str
)
@click.option('--tag', help='docker tag', type=str, default='latest')
@click.option('--stage', help='environment to stage.')
@click.pass_obj
def push(obj, dir, region, build, provider, no_cache, stage, tag):
    """
    Command to push docker container image to Cloud Container Registry
    """
    reset_terminal()
    helper_library_path = obj['helper_library_path']
    mldock_manager = MLDockConfigManager(
        filepath=os.path.join(dir, ".mldock.json")
    )
    # get mldock_module_dir name
    mldock_config = mldock_manager.get_config()
    image_name = mldock_config.get("image_name", None)
    container_dir = mldock_config.get("container_dir", None)
    module_path = os.path.join(
        dir,
        mldock_config.get("mldock_module_dir", "src"),
    )
    dockerfile_path = os.path.join(
        dir,
        mldock_config.get("mldock_module_dir", "src"),
        container_dir
    )
    requirements_file_path = os.path.join(
        dir,
        mldock_config.get("requirements.txt", "requirements.txt")
    )

    try:
        stages = mldock_config.get("stages", None)

        if stage is not None:
            tag = stages[stage]['tag']

        if tag is None:
            raise Exception("tag is not valid. Either choose a stage or set a tag manually")
    except KeyError as exception:
        logger.error("Stage not found. Either update stages in mldock config or manually set docker tag.")
        sys.exit(-1)
    except Exception as exception:
        logger.error(exception)
        sys.exit(-1)
    try:
        # login and authenticate
        client, metadata = login_and_authenticate(provider=provider, region=region)
        image_repository = "{}/{}".format(metadata['repository'], image_name)
        logger.info("\nLogin Complete! ヽ(´▽`)/\n")

        if build:
            logger.info("\nStarting build...\n")
            # build image for cloud repository
            docker_build(
                image_name=image_repository,
                dockerfile_path=dockerfile_path,
                module_path=module_path,
                target_dir_name=mldock_config.get("mldock_module_dir", "src"),
                requirements_file_path=requirements_file_path,
                no_cache=no_cache,
                docker_tag=tag
            )
            logger.info("\nBuild Complete! ヽ(´▽`)/\n")

        # Push image to cloud repository
        states = push_image_to_repository(
            image_repository=image_repository,
            auth_config = {'username': metadata['username'], 'password': metadata['password']},
            tag=tag
        )
        reset_terminal()
        logger.info(obj["logo"])

        for layer_id, metadata in states.items():
            single_line = [
                click.style(layer_id, bg='blue'),
                click.style(metadata["message"], fg='white')
            ]
            single_line = " ".join(single_line)
            click.echo(single_line, nl=True)

        logger.info("\nPush Complete! ヽ(´▽`)/\n")

    except Exception as e:
        logger.error("{}".format(e))
        sys.exit(-1)

@click.command()
@click.option(
    '--dir',
    help='Set the working directory for your mldock container.',
    required=True,
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        writable=True,
        readable=True,
        resolve_path=False,
        allow_dash=False,
        path_type=None
    )
)
@click.option('--no-cache', help='builds container from scratch', is_flag=True)
@click.option(
    '--provider',
    help='Set the cloud provider',
    required=True,
    type=click.Choice(['ecr', 'gcr', 'dockerhub'],
    case_sensitive=False
    )
)
@click.option(
    '--region',
    help='Set the registry region',
    default=None,
    type=str
)
@click.option('--tag', help='docker tag', type=str, default='latest')
@click.option('--stage', help='environment to stage.')
@click.pass_obj
def pull(obj, dir, region, provider, no_cache, stage, tag):
    """
    Command to push docker container image to Cloud Container Registry
    """
    helper_library_path = obj['helper_library_path']
    mldock_manager = MLDockConfigManager(
        filepath=os.path.join(dir, ".mldock.json")
    )
    # get mldock_module_dir name
    mldock_config = mldock_manager.get_config()
    image_name = mldock_config.get("image_name", None)
    container_dir = mldock_config.get("container_dir", None)
    module_path = os.path.join(
        dir,
        mldock_config.get("mldock_module_dir", "src"),
    )
    dockerfile_path = os.path.join(
        dir,
        mldock_config.get("mldock_module_dir", "src"),
        container_dir
    )
    requirements_file_path = os.path.join(
        dir,
        mldock_config.get("requirements.txt", "requirements.txt")
    )

    try:
        stages = mldock_config.get("stages", None)

        if stage is not None:
            tag = stages[stage]['tag']

        if tag is None:
            raise Exception("tag is not valid. Either choose a stage or set a tag manually")
    except KeyError as exception:
        logger.error("Stage not found. Either update stages in mldock config or manually set docker tag.")
        sys.exit(-1)
    except Exception as exception:
        logger.error(exception)
        sys.exit(-1)
    try:
        # login and authenticate
        client, metadata = login_and_authenticate(provider=provider, region=region)
        image_repository = "{}/{}".format(metadata['repository'], image_name)
        logger.info("\nLogin Complete! ヽ(´▽`)/\n")

        # Push image to cloud repository
        states = pull_image_from_repository(
            image_repository=image_repository,
            auth_config = {'username': metadata['username'], 'password': metadata['password']},
            tag=tag
        )

        reset_terminal()
        logger.info(obj["logo"])

        for layer_id, metadata in states.items():
            single_line = [
                click.style(layer_id, bg='blue'),
                click.style(metadata["message"], fg='white')
            ]
            single_line = " ".join(single_line)
            click.echo(single_line, nl=True)
        logger.info("\nPull Complete! ヽ(´▽`)/\n")

    except Exception as e:
        logger.error("{}".format(e))
        sys.exit(-1)

cloud.add_command(push)
cloud.add_command(pull)
