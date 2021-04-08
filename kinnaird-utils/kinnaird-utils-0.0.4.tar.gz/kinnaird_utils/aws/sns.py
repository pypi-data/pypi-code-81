from typing import Dict, List, Optional, Literal
from datetime import datetime
from pydantic import BaseModel
from pydantic.networks import HttpUrl
from aws_lambda_powertools.utilities.data_classes import SNSEvent


class SnsMsgAttributeModel(BaseModel):
    Type: str
    Value: str


class SnsNotificationModel(BaseModel):
    Subject: Optional[str]
    TopicArn: str
    UnsubscribeUrl: HttpUrl
    Type: Literal["Notification"]
    MessageAttributes: Optional[Dict[str, SnsMsgAttributeModel]]
    Message: str
    MessageId: str
    SigningCertUrl: HttpUrl
    Signature: str
    Timestamp: datetime
    SignatureVersion: str


class SnsRecordModel(BaseModel):
    EventSource: Literal["aws:sns"]
    EventVersion: str
    EventSubscriptionArn: str
    Sns: SnsNotificationModel


class SnsModel(BaseModel):
    Records: List[SnsRecordModel]



def get_sns_event_subject(event: SNSEvent):
    """Return the subject for the first sns event record"""
    return event.record.sns.subject


def get_example_event_json(subject: str, message: str):
    """Helper method to generate example events given a message and a subject"""
    if not message:
        message = "example message"
    if not subject:
        subject = "example subject"
    event = {
        "Records": [
            {
                "EventSource": "aws:sns",
                "EventVersion": "1.0",
                "EventSubscriptionArn": "arn:aws:sns:us-east-1::privateapi",
                "Sns": {
                    "Type": "Notification",
                    "MessageId": "95df01b4-ee98-5cb9-9903-4c221d41eb5e",
                    "TopicArn": "arn:aws:sns:us-east-1:12345678912:privateapi",
                    "Subject": subject,
                    "Message": message,
                    "Timestamp": "1970-01-01T00:00:00.000Z",
                    "SignatureVersion": "1",
                    "Signature": "Tb9Y/BZnBDbDwqj3yEOnjHuuIulXDHKZgHo3VT8bClqHwglWMBABnWOfUFFsJWaQLWRE8MIDPWSr0IR0gVHpTicmA9XWpMGhLy0KBnWuRF/FEQU886SdZz3TJW94lX1vGDZFJX6LA8ZpwQFJ69bVf2WemSCcPnzPFaVnSp+2W4fTMRIreRwGvAQW1HSHObowmRqtSz7ZBmDFRjyF9wuPte0KyWwJh9m9Z/zhIFkJfNUBMM+hSafxVqVUrHKcSO1vnAi7eFeIzJzpQHiXaZEKCmPMD4NVAeuqF3CHjfbd6n4Jwe1dcVP+o69fuXyADqrV1kGtHpLBAlGk9MRyIeWWoQ==",
                    "SigningCertUrl": "https://sns.eu-west-1.amazonaws.com/SimpleNotificationService-010a507c1833636cd94bdb98bd93083a.pem",
                    "UnsubscribeUrl": "https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:12345678912:powertools265:5e4c8d5d-383c-4aa1-90aa-d849f068e7dc",
                    "MessageAttributes": {
                        "Test": {
                            "Type": "String",
                            "Value": "TestString"
                        },
                        "TestBinary": {
                            "Type": "Binary",
                            "Value": "TestBinary"
                        }
                    }
                }
            }
        ]
    }
    return event
