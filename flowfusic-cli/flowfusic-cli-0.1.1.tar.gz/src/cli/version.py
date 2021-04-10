import click

from src.log import logger


PROJECT_NAME = "flowfusic-cli"


def pip_upgrade():
    import sys
    import subprocess

    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "--upgrade", PROJECT_NAME]
    )
    logger.info("Upgrade completed.")


def conda_upgrade():
    logger.info("Conda is not supported at the moment. We are working on it!")
    # logger.info("To upgrade please run:\nconda install -y -c floydhub -c conda-forge floyd-cli")


@click.command()
def version():
    """
    View the current version of the CLI.
    """
    import pkg_resources

    version = pkg_resources.require(PROJECT_NAME)[0].version
    logger.info(version)


def auto_upgrade():
    try:
        from src.cli.utils import is_conda_env

        if is_conda_env():
            conda_upgrade()
        else:
            pip_upgrade()
    except Exception as e:
        logger.error(e)


@click.command()
def upgrade():
    """
    Upgrade CLI to the latest version.
    """
    auto_upgrade()
