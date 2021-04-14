#!/usr/bin/env python3

# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

"""
The Lawwenda command line interface.

This tool is used by the end user for creating and managing shares and more. It can be called with some command line
arguments for a particular action, or without parameters (which will open an interactive Python prompt for further
actions).

Do not use this module in code. See :py:class:`lawwenda.Configuration` instead.
"""

import argparse
import code
import datetime
import getpass
import readline
import rlcompleter
import subprocess
import typing as t

import lawwenda
import lawwenda.datafiles


def console(*, cfg: lawwenda.Configuration) -> None:
    """
    Open an interactive Python console.

    The user will get a small help text and is then able to configure Lawwenda by typing Python code.

    :param cfg: The initial value for the `cfg` variable inside the console.
    """
    def _readme():
        freadme = lawwenda.datafiles.find_data_file("README.pdf")
        if not freadme:
            raise EnvironmentError("Your installation does not include documentation.")
        try:
            subprocess.check_output(["xdg-open", freadme])
        except (subprocess.CalledProcessError, IOError):
            print(f"Please open '{freadme}'.")
    consolevars = {**lawwenda.__dict__, "cfg": cfg,
                   "quickstart": lambda: print(_quickstart(cfg.path)),
                   "readme": _readme}
    print(f"Welcome to Lawwenda Console!\n{_quickstart(cfg.path)}")
    readline.set_completer(rlcompleter.Completer(consolevars).complete)
    readline.parse_and_bind("tab: complete")
    code.InteractiveConsole(consolevars).interact(banner="", exitmsg="Bye.")


def run_dev_server(*, cfg: lawwenda.Configuration) -> None:
    """
    Start a tiny local server for this configuration.

    Such a server can be used for trying, development, testing, and so on, but is not recommended for real usage.

    It will automatically find a free port, will print its url, and blocks.

    Only used internally by the cli. See :py:class:`lawwenda.Configuration`.
    """
    cfg.run_dev_server().wait_stopped()


def list_shares(*, cfg: lawwenda.Configuration) -> str:
    """
    Return a list of share names as string, one line for each share.

    Only used internally by the cli. See :py:class:`lawwenda.Configuration`.
    """
    return "\n".join([share.name for share in cfg.get_shares()])


def describe_share(*, cfg: lawwenda.Configuration, name: str) -> str:
    """
    Return a textual share description (i.e. how it is configured) for a share.

    Only used internally by the cli. See :py:class:`lawwenda.Configuration`.
    """
    return str(cfg.get_share_by_name(name) or "")


def add_share(*, cfg: lawwenda.Configuration, name: str, path: str, title: str, active_until: str,
              hide_by_pattern: t.List[str], hide_by_tag: t.List[str], include_by_pattern: t.List[str],
              include_by_tag: t.List[str], exclude_by_pattern: t.List[str], exclude_by_tag: t.List[str],
              exclude_hidden: bool, readonly: bool) -> None:
    """
    Add a share.

    Only used internally by the cli. See :py:meth:`lawwenda.Configuration.add_share`.
    """
    password = getpass.getpass("Please choose a share password: ")
    # TODO getpass twice
    cfg.add_share(path, name=name, password=password, title=title, readonly=readonly, hide_by_patterns=hide_by_pattern,
                  hide_by_tags=hide_by_tag, include_by_patterns=include_by_pattern, include_by_tags=include_by_tag,
                  exclude_by_patterns=exclude_by_pattern, exclude_by_tags=exclude_by_tag, exclude_hidden=exclude_hidden,
                  active_until=datetime.datetime.fromisoformat(active_until) if active_until else None)


def remove_share(*, cfg: lawwenda.Configuration, name: str) -> None:
    """
    Remove a share.

    Only used internally by the cli. See :py:meth:`lawwenda.Configuration.remove_share`.
    """
    cfg.remove_share(name)


def generate_wsgi(*, cfg: lawwenda.Configuration) -> str:
    """
    Generates a wsgi script for hosting Lawwenda in a web server.

    Only used internally by the cli. See :py:meth:`lawwenda.Configuration.generate_wsgi`.
    """
    return cfg.generate_wsgi()


def _fmt_cmd(txt: str) -> str:
    return f"\033[1;36m{txt}\033[0m"


def _quickstart(cfgpath: str) -> str:
    return f"""
Quick start guide
-----------------
Whenever you got lost, calling '{_fmt_cmd("quickstart()")}' shows this text again and 
'{_fmt_cmd("readme()")}' opens the Lawwenda documentation. Any Python code is allowed.

At first you need a Configuration object. If you are fine with
 {cfgpath}
as configuration path, just take 'cfg'. Otherwise, call:
{_fmt_cmd('cfg = Configuration("/path/to/my/lawwenda/config/dir")')}
(replace paths with something that fits your needs!)

Then you can create a new share by calling:
{_fmt_cmd('cfg.add_share("/path/that/i/want/to/share", name="myshare", password="foo")')}

Call '{_fmt_cmd('help(cfg)')}' in order to find out what other methods exist, and 
'{_fmt_cmd('help(cfg.add_share)')}' for more parameters of 'add_share', and for other things
when needed. Calls like '{_fmt_cmd('print(cfg)')}' print details about an object.

If your web server provides your Lawwenda installation at 
'https://example.com/shares/', you can access your new 'myshare' share at
'https://example.com/shares/myshare/'. For playing around (only!) you can call 
'{_fmt_cmd('cfg.run_dev_server()')}' in order to start a little toy server."""


def main():
    """
    Parse command line arguments and call the right function with its arguments.
    """
    parser = argparse.ArgumentParser(description="Lawwenda command line interface.")
    parser.add_argument("--cfgpath", help="the path of your Lawwenda configuration directory", required=False)
    sbaction = parser.add_subparsers(help="the action to execute")
    parser_listshares = sbaction.add_parser("list_shares", help="lists all shares")
    parser_listshares.set_defaults(fct=list_shares)
    parser_describeshare = sbaction.add_parser("describe_share", help="prints details about a share")
    parser_describeshare.add_argument("name", help="the share name")
    parser_describeshare.set_defaults(fct=describe_share)
    parser_addshare = sbaction.add_parser("add_share", help="adds a new share")
    parser_addshare.add_argument("name", help="the share name")
    parser_addshare.add_argument("path", help="the directory to share")
    parser_addshare.add_argument("--title", help="the share title text")
    parser_addshare.add_argument("--active-until", help="the expiration date/time (in iso format)")
    parser_addshare.add_argument("--hide-by-pattern", help="a regex pattern of paths to hide at first", action="append")
    parser_addshare.add_argument("--hide-by-tag", help="a tag to hide at first", action="append")
    parser_addshare.add_argument("--include-by-pattern", help="a regex pattern of paths to include", action="append")
    parser_addshare.add_argument("--include-by-tag", help="a tag to include", action="append")
    parser_addshare.add_argument("--exclude-by-pattern", help="a regex pattern of paths to exclude entirely",
                                 action="append")
    parser_addshare.add_argument("--exclude-by-tag", help="a tag to exclude entirely", action="append")
    parser_addshare.add_argument("--exclude-hidden", help="exclude each item that is hidden", action="store_true")
    parser_addshare.add_argument("--readwrite", help="allow write access", action="store_false", dest="readonly")
    parser_addshare.set_defaults(fct=add_share)
    parser_removeshare = sbaction.add_parser("remove_share", help="removes a share")
    parser_removeshare.add_argument("name", help="the share name")
    parser_removeshare.set_defaults(fct=remove_share)
    parser_console = sbaction.add_parser("console", help="opens the Console (this is the default for no arguments)")
    parser_console.set_defaults(fct=console)
    parser_rundevserver = sbaction.add_parser("run_dev_server", help="runs a tiny web server for development")
    parser_rundevserver.set_defaults(fct=run_dev_server)
    parser_generatewsgi = sbaction.add_parser("generate_wsgi", help="generates wsgi application code")
    parser_generatewsgi.set_defaults(fct=generate_wsgi)
    argsdict = parser.parse_args().__dict__
    argsdict["cfg"] = lawwenda.Configuration(argsdict.pop("cfgpath"))
    fct = argsdict.pop("fct", console)
    print(fct(**argsdict) or "")


if __name__ == "__main__":
    main()
