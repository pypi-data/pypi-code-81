#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
IRIS Staging Client Service
===========================
Modified: 2021-03


"""

import logging.config
import time

from service import Service
from iris_stage.aws.s3 import S3Client
from iris_stage.aws.sqs import SQSClient
from iris_stage.snap.installer import Installer


class StageClient(Service):

    POLL_RATE = 5

    def __init__(self, name:str, pid_dir:str):
        self.logger = logging.getLogger(__name__)
        super().__init__(name, pid_dir)
        self.logger.info("%s instantiated successfully.", __name__)

    def run(self) -> None:
        """
        Service runner entry and polling loop.
        """
        # initialize clients
        try:
            sqs_client = SQSClient()
        except FileNotFoundError:
            self.logger.exception("Failed to initialize sqs client. Exiting.")
            self.stop()
        else:
            self.logger.info("Initialized AWS SQS client")
        try:
            s3_client = S3Client()
        except FileNotFoundError:
            self.logger.exception("Failed to initialize s3 client. Exiting.")
            self.stop()
        else:
            self.logger.info("Initialized AWS S3 client")
        installer = Installer()

        self.logger.info("Starting sqs main event loop")
        while not self.got_sigterm():
            response = sqs_client.poll_sqs()
            # pull snap from s3 and install if sqs poll yeilds notification
            if response:
                s3_client.pull()
                installer.install()
            time.sleep(self.POLL_RATE)
