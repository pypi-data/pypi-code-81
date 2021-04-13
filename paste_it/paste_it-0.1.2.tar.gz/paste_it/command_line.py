#!/usr/bin/env python3
import argparse
import os
import json
from time import sleep
from rich import print
from sys import exit
from paste_it import make_user_api_key, paste  # type: ignore


def main():
    parser = argparse.ArgumentParser(prog="paste_it")
    parser.add_argument(
        "--format",
        type=str,
        help="format of the file contents. you can find the avalible formats at https://pastebin.com/doc_api",
        default="",
    )
    parser.add_argument(
        "--private",
        type=int,
        help="if your file should be privte, 0 public, 1 unlisted, 2 Private (only allowed in combination with api_user_key, as you have to be logged into your account to access the paste)",
        default=0,
    )
    parser.add_argument(
        "--title",
        nargs="?",
        dest="title",
        type=str,
        help="the title of your paste",
    )
    parser.add_argument(
        "path",
        type=str,
        help="file who's contents you want to paste on pastebin",
    )
    args = parser.parse_args()
    if os.path.exists(args.path):
        with open("config.json", "r") as f:
            config = json.loads(f.read())
        f.close()
        with open(args.path, "r") as f:
            content: str = f.read()
        f.close()
        if args.private < 0 or args.private > 2:
            print("[red] the paste  of a file must lie between 0 to 2 [/red]")
            exit(1)
        else:
            if args.private == 2:
                if config["api_user_key"] == "":
                    print(
                        "[blue]I couldn't find a api_user_key I am assuming you want me to create one if not press ^c in the next 5 second[/blue]"
                    )
                    sleep(5)
                    config.update({"api_user_key": make_user_api_key(config)})
                    with open("config.json", "w") as f:
                        f.write(json.dumps(config))
                paste_status = paste(
                    content, args.title, args.format, args.private, config
                )
            else:
                paste_status = paste(
                    content, args.title, args.format, args.private, config
                )
            if paste_status[0]:
                print(f"created paste at {paste_status[1]}")
            else:
                print(f"could not create paste, {paste_status[1]}")
    else:
        print("[red]file path is not valid[/red]")
