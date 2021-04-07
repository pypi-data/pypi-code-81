# Copyright 2021 Outside Open
# This file is part of Digital-Hydrant.

# Digital-Hydrant is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Digital-Hydrant is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Digital-Hydrant.  If not, see https://www.gnu.org/licenses/.

import sqlite3
import shutil
import sys

from digital_hydrant import logging
from digital_hydrant.uploader import Uploader
from digital_hydrant.collector_queue import CollectorQueue
from digital_hydrant.ping import Ping
from digital_hydrant.args import args
from digital_hydrant.process_manager import ProcessManager
from digital_hydrant.config import db_path, update_config, check_default_config
from digital_hydrant.migration import migrate_db


def check_required_ubuntu_packages():
    missing = False
    packages = {
        "arp-scan": "https://github.com/royhills/arp-scan",
        "dhcpcd": "https://wiki.archlinux.org/index.php/Dhcpcd",
        "iw": "https://wireless.wiki.kernel.org/en/users/documentation/iw",
        "lldpd": "https://lldpd.github.io/lldpd/installation.html",
        "ifconfig": "(https://wiki.linuxfoundation.org/networking/net-tools",
        "nmap": "https://nmap.org",
        "hydra": "https://github.com/vanhauser-thc/thc-hydra",
        "tshark": "https://www.wireshark.org/docs/man-pages/tshark.html",
        "wpa_supplicant": "https://wiki.archlinux.org/index.php/wpa_supplicant",
        "yersinia": "https://github.com/tomac/yersinia",
    }

    for package, link in packages.items():
        which = shutil.which(package)

        if which is None:
            print(f"Digital Hydrant requires your system to have {package} installed")
            print(f"    Package details can be found at {link}")
            missing = True

    return missing


def run():
    check_default_config()
    migrate_db()

    missing = False if args.force else check_required_ubuntu_packages()

    if args.init is not None:
        if len(args.init) > 0:
            update_config({"api": {"token": args.init}})

        print("\ninit complete!")
        return

    if missing:
        sys.exit(
            "\nPlease install all required dependencies or use -f/--force to run without dependencies"
        )

    logger = logging.getLogger(__name__)
    manager = ProcessManager("Main")

    if args.clear_queue:
        queue = CollectorQueue()
        queue.remove_all()

    ping = Ping()
    manager.add_process("ping", ping.__exec__)

    collect = args.collect
    upload = args.upload

    if not (collect or upload):
        collect = upload = True

    if collect:
        logger.info("Launching Scheduler")
        scheduler = ProcessManager("Scheduler")
        manager.add_process("scheduler", scheduler.manage)

    if upload:
        logger.info("Launching Uploader")
        uploader = Uploader()
        manager.add_process("uploader", uploader.__upload__)

    manager.manage()
