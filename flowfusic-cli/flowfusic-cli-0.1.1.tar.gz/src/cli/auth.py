import sys

import click

import src
from src.client.auth import AuthClient
from src.log import logger
from src.manager.auth_config import AuthConfigManager
from src.manager.login import has_browser, wait_for_apikey


@click.command()
@click.option("--apikey", "-k", help="Api Key")
def login(apikey):
    """
    Login to Flowfusic.
    """
    # if manual_login_success(token, username, password):
    #     return

    if not apikey:
        if has_browser():
            apikey = wait_for_apikey()
        else:
            logger.error(
                "No browser found, please login manually by creating "
                "login key at %s/settings/apikey.",
                src.FLOWFUSIC_WEB_HOST,
            )
            sys.exit(1)

    if apikey:
        user = AuthClient().get_user(apikey, is_apikey=True)
        AuthConfigManager.set_apikey(username=user.username, apikey=apikey)
        logger.info("Login Successful as %s", user.username)
    else:
        logger.error("Login failed, please see --help for other login options.")


@click.command()
def logout():
    """
    Logout of Flowfusic.
    """
    AuthConfigManager.purge_access_token()
