#!/usr/bin/env python
import boto3
import os
from datacoco_cloud import UNIT_TEST_KEY
import logging


class S3toS3Interaction(object):
    """
    Class to simplify S3 to S3 Interactions using boto3
    """

    def __init__(
        self,
        source_aws_key: str,
        source_aws_secret: str,
        target_aws_key: str,
        target_aws_secret: str,
        source_aws_region: str = "us-east-1",
        target_aws_region: str = "us-east-1",
    ):
        ##########
        ### Setup configuration
        ##########

        self.is_test = os.environ.get(UNIT_TEST_KEY, False)

        self.source_aws_key = source_aws_key
        self.source_aws_secret = source_aws_secret
        self.source_aws_region = source_aws_region

        self.target_aws_key = target_aws_key
        self.target_aws_secret = target_aws_secret
        self.target_aws_region = target_aws_region

        ### Setting up the S3 Clients
        if not self.is_test:
            self.s3_client_source = boto3.client(
                "s3",
                region_name=self.source_aws_region,
                aws_access_key_id=self.source_aws_key,
                aws_secret_access_key=self.source_aws_secret,
            )

            self.s3_client_target = boto3.client(
                "s3",
                region_name=self.target_aws_region,
                aws_access_key_id=self.target_aws_key,
                aws_secret_access_key=self.target_aws_secret,
            )

    def duplicate_objects(
        self,
        source_bucket: str,
        target_bucket: str,
        source_bucket_prefix: str,
        target_path: str,
        source_bucket_suffix: str = "",
    ):

        self.__do_transfer(
            source_bucket=source_bucket,
            target_bucket=target_bucket,
            source_bucket_prefix=source_bucket_prefix,
            target_path=target_path,
            source_bucket_suffix=source_bucket_suffix,
            isMove=False,
        )

    def move_objects(
        self,
        source_bucket: str,
        target_bucket: str,
        source_bucket_prefix: str,
        target_path: str,
        source_bucket_suffix: str = "",
    ):

        self.__do_transfer(
            source_bucket=source_bucket,
            target_bucket=target_bucket,
            source_bucket_prefix=source_bucket_prefix,
            target_path=target_path,
            source_bucket_suffix=source_bucket_suffix,
            isMove=True,
        )

    def __do_transfer(
        self,
        source_bucket: str,
        target_bucket: str,
        source_bucket_prefix: str,
        target_path: str,
        source_bucket_suffix: str,
        isMove: bool = False,
    ):

        # String for Printing Operations
        operation = "copy"
        if isMove:
            operation = "move"

        try:
            payload = self.s3_client_source.list_objects_v2(
                Bucket=source_bucket, Prefix=source_bucket_prefix
            )
            if payload["KeyCount"] == 0:
                logging.info(f"No files to {operation}.")
            else:
                keyCount = 0
                for item in payload["Contents"]:

                    filepath = item["Key"]

                    # Checks first if file matches suffix
                    if filepath.endswith(source_bucket_suffix):

                        # Increase Key Count per matched suffix
                        keyCount += 1

                        if len(filepath.split("/")) > 1:
                            deductLength = len(filepath.split("/")[0]) + 1
                        else:
                            deductLength = 0
                        filename = filepath[deductLength:]
                        logging.info(f"filename: {filename}")
                        if filename is not "":
                            logging.info(
                                f"Sending file {source_bucket}/{filepath} to {target_bucket}/{target_path}/{filename}"
                            )
                            logging.info(
                                f"filename to {operation}: {filename}"
                            )
                            copy_source = {
                                "Bucket": source_bucket,
                                "Key": filepath,
                            }
                            if not self.is_test:
                                copy_response = self.s3_client_target.copy_object(
                                    CopySource=copy_source,
                                    Bucket=target_bucket,
                                    Key=f"{target_path}/{filename}",
                                )
                                logging.info(copy_response)
                                if (
                                    copy_response["ResponseMetadata"][
                                        "HTTPStatusCode"
                                    ]
                                    != 200
                                ):
                                    logging.error(
                                        f"Failed to {operation}: {fileName}"
                                    )

                                if isMove:
                                    delete_response = self.s3_client_source.delete_object(
                                        Bucket=source_bucket, Key=filepath
                                    )
                                    logging.info(delete_response)
                                    if (
                                        delete_response["ResponseMetadata"][
                                            "HTTPStatusCode"
                                        ]
                                        != 200
                                    ):
                                        logging.error(
                                            f"Failed to delete: {fileName}"
                                        )

                    if keyCount == 0:
                        logging.info(f"No files to {operation}.")
        except Exception as e:
            logging.error(e)
            raise e
