#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
S3 Client
=========
Modified: 2020-02

Pulls bucket objects from target s3 bucket
"""

import os
import boto3
import logging
import botocore.exceptions

class S3Client:

    def __init__(self) -> None:
        # here we need to get the bucket credentials from .aws/config so the 
        # aws credentials can be easily referenced and persist through service
        # restarts
        self.bucket = os.environ['S3_BUCKET']
        self.obj = os.environ['S3_OBJECT']
        self.tmp = os.environ['SNAP_FP']
        self.logger = logging.getLogger(__name__)
        try:
            self.s3 = boto3.client("s3")
        except botocore.exceptions.NoCredentialsError as exc:
            self.logger.exception("%s\nAWS credentials not found.\
                Ensure that ~/.aws/config and ~/.aws/credentials exist.", exc)
            raise FileNotFoundError from exc
        self.logger.info("%s instantiated successfully.", __name__)
    
    def pull(self) -> None:
        """
        Pulls file from target s3 bucket to /tmp
        """
        self.logger.info("Pulling %s from S3 %s bucket", self.obj, self.bucket)
        self.s3.download_file(self.bucket, self.obj, self.tmp)
        self.logger.info("S3 download complete.")
