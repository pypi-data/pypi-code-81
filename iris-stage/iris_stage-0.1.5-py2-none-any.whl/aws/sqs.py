#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
AWS SQS Staging Client
======================
Modified: 2021-03

This module listens for an SQS message on a multi-part upload event completion.
Once an SQS notification is received it digests the message and unblocks the
proceeding stages in the pipeline.
"""

import boto3
import botocore.exceptions
import logging.config

class SQSClient:

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        # Create SQS client
        try:
            self.sqs = boto3.client('sqs')
        except botocore.exceptions.NoCredentialsError as exc:
            self.logger.exception("%s\nAWS credentials not found.\
                Ensure that ~/.aws/config and ~/.aws/credentials exist.", exc)
            raise FileNotFoundError from exc
        # Latch on available SQS queue
        response = self.sqs.list_queues()
        self.logger.info("SQS Queue list: %s", response['QueueUrls'])
        self.sqs_queue_url=response['QueueUrls'][-1]
        self.logger.info("%s instantiated successfully.", __name__)

    def poll_sqs(self) -> bool:
        """
        Polls SQS server for snap push completion messages.

        :returns: True if SQS poll returns a notification and False otherwise
        """
        # Receive message from SQS queue
        try:
            response = self.sqs.receive_message(
                QueueUrl=self.sqs_queue_url,
                AttributeNames=[
                    'SentTimestamp'
                ],
                MaxNumberOfMessages=1,
                MessageAttributeNames=[
                    'All'
                ],
                VisibilityTimeout=0,
                WaitTimeSeconds=20
            )
        except BaseException as exc:
            self.logger.exception(
                "An exception occured when making sqs request: %s", exc)
            return False
        
        self.logger.info("Received Response: %s", response)
        
        try:
            message = response['Messages'][0]
        except KeyError:
            pass
        else:
            self.logger.info("Receiving and digesting message")
            # digest recieved message and launch a service
            receipt_handle = message['ReceiptHandle']
            # Delete received message from queue
            self.sqs.delete_message(
                QueueUrl=self.sqs_queue_url,
                ReceiptHandle=receipt_handle
            )
            return True
        return False
