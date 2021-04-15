#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Snap Installer
==============
Modified: 2021-02

Handles new snap installations from s3 download location
"""
import os
import shutil
import logging.config

class Installer:

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.tmp = os.environ['SNAP_FP']
        self.name = os.environ['SNAP_NAME']
        self.secrets = os.environ['SNAP_SECRETS']
        self.common = os.environ['SNAP_COMMON']
        self.logger.info("%s instantiated successfully.", __name__)

    def install(self):
        """
        Uninstall existing snap, artificially inject machine secrets from
        secrets to $SNAP_COMMON and install new snap file in devmode.
        """
        self.logger.info("Removing current snap")
        os.system(f"snap stop {self.name}")
        os.system(f"snap remove {self.name}")
        self.logger.info("Installing newest snap")
        try:
            shutil.copytree(self.secrets, self.common)
        except FileNotFoundError as exc:
            self.logger.exception("%s\nIRIS machine secrets not found.\
                Ensure that IMS are present in: ~/.secrets.", exc)
            return
        except FileExistsError:
            self.logger.info(
                "Machine secrets already exist in the correct location.")
        os.system(f"snap install {self.tmp} --devmode")
