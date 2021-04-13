"""a cli script and tiny library to upload files to pastebin"""
import requests
import logging
import os
from time import sleep
from rich.logging import RichHandler
from typing import Dict, Tuple

__version__ = "0.1.2"

FORMAT: str = "%(message)s"
logging.basicConfig(
    level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
log = logging.getLogger("Rich")
"""
TODO:
    move cli component to other file
"""


def make_user_api_key(config: Dict[str, str]) -> str:
    """
    Genrates a user api key for pastebin

    This genrates a user api key to allow creating of "private" api keys
    Args:
        config (dict):
            api_dev_key (str): Your pastebin api key, vist https://pastebin.com/doc_api to get it(you will need to be logged in.
            api_user_name (str): Your pastebin username
            api_user_password (str): the password of your pastebin accouont
            api_url (str): for pastebin set to https://pastebin.com
            api_user_key (str): this value will be overwritten so you can set it to "" if you do not have one
    Returns:
        api_user_key (str): returns the genrated user key
    """
    payload: Dict[str, str] = {
        "api_dev_key": config["api_dev_key"],
        "api_user_name": config["api_user_name"],
        "api_user_password": config["api_user_password"],
    }
    user_api_key_request = requests.post(
        f"{config['api_url']}/api/api_login.php", data=payload
    )
    if user_api_key_request.status_code != 200:
        log.error("[red]failed to create key[/red]")
        exit(1)
    else:
        logging.info(
            f"[green]created user api key: {user_api_key_request.text},\nadding to config.json[/green]"
        )
        return user_api_key_request.text


def paste(
    text: str, title: str, text_format: str, private: int, config: Dict[str, str]
) -> Tuple[bool, str]:
    """
    Function to upload the text to pastebin
    This functon uploads the contents of the text variable to paste bin with the title as variable title.
    Args:
        text (str): content for the body of the paste
        title (str): title of paste
        text_format (str): format of text specified from list at https://pastebin.com/doc_api, set to "" if you don't want any
        private (int): integer between 0 and 2
        config (Dict):
            api_dev_key (str): Your pastebin api key, vist https://pastebin.com/doc_api to get it(you will need to be logged in.
            api_user_name (str): Your pastebin username
            api_user_password (str): the password of your pastebin accouont
            api_url (str): for pastebin set to https://pastebin.com
            api_user_key (str): this value is required for privateness level 2 but in other cases you can set it to "" as it is not required but will be used if provided.
    Returns:
        status (bool): If the paste was made successfully
    """
    if private == 2:
        payload = {
            "api_dev_key": config["api_dev_key"],
            "api_user_key": config["api_user_key"],
            "api_paste_name": title,
            "api_paste_private": private,
            "api_paste_code": text,
            "api_paste_format": text_format,
            "api_option": "paste",
        }
    else:
        payload = {
            "api_dev_key": config["api_dev_key"],
            "api_paste_name": title,
            "api_paste_code": text,
            "api_paste_format": text_format,
            "api_option": "paste",
        }
        if config["api_user_key"] != "":
            payload["api_user_key"] = config["api_user_key"]
        if private == 1:
            payload["api_paste_private"] = 1
        paste_request = requests.post(
            f"{config['api_url']}/api/api_post.php", data=payload
        )
        if paste_request.status_code != 200:
            log.error(
                f"[red] Couldn't create a the paste, here is the error I got:\n{paste_request.text}[/red]"
            )
            return (False, f"{paste_request.text}")
        else:
            log.debug(f"created post at {paste_request.text}")
            return (True, f"{paste_request.text}")
    return (False, f"")
