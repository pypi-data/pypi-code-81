from os import path

import boto3

from notificationhub_sdk.base import ImproperlyConfigured

TOKEN_PATH = "/var/run/secrets/eks.amazonaws.com/serviceaccount/token"
SQS_SERVICE_NAME = "sqs"

class Session:
    """
    Used to create AWS Session
    """
    
    def __init__(self,
                 region: str,
                 access_key: str,
                 secret_key: str, 
                 eks_role_arn: str):
        """
        Parameters:
            access_key: access key of aws account
            secret_key: secret key of aws account
            eks_role_arn: eks role which has access to SQS 
        """
        self._region = region
        self._acces_key = access_key
        self._secret_key = secret_key
        self._eks_role_arn = eks_role_arn
        
    def get(self):
        """
        creates aws session based on different criteria
        - Access key and secret key given in the settings
        - EC2: based on the assumption that the role is given to the EC2 instance
        - EKS-role based access: eks_role_arn is taken into consideration
        - Local settings: read from the local ~/.aws/credentials path
        """
        # Access key and secret key given in the settings
        if self._acces_key and self._secret_key:
            session = self.__handle_access_key_authentication()
        else:
            session = self.__handle_role_based_authentication()
        
        # local development
        if session is None:
            session = self.__handle_local_dev_authentication()

        # check whether session is created after all possible options
        if session is None:
            raise ImproperlyConfigured('AWS session is not created due to improper setting provided in region `{}`'.format(self._region))

        return session
    
    def __handle_access_key_authentication(self):
        """
        creates an AWS session based on the Access Key and Secret Key
        """
        client_kwargs = {
            'service_name': SQS_SERVICE_NAME,
            'aws_access_key_id': self._acces_key,
            'aws_secret_access_key': self._secret_key,
            'region_name': self._region
        }
        return boto3.resource(**client_kwargs)
    
    def __handle_role_based_authentication(self):
        """
        creates an AWS session based on IAM role given to EC2 or Pod
        """
        # EC2 instance
        client_kwargs = {
            'service_name': SQS_SERVICE_NAME,
            'region_name': self._region
        }
        session = boto3.resource(**client_kwargs)

        # eks role-based access
        if self._eks_role_arn and self._eks_role_arn != "":
            # check whether the given information has the account number or not
            aws_client = boto3.client('sts')
            if aws_client == None or aws_client == "":
                raise ImproperlyConfigured('Issue while connecting to SQS region `{}`'.format(self._region))

            try:
                if not path.exists(TOKEN_PATH):
                    raise ImproperlyConfigured('Token not present in pod. Check token at `{}`'.format(TOKEN_PATH))
                with open(TOKEN_PATH, 'r') as file:
                    access_details = file.read()
                response = aws_client.assume_role_with_web_identity(
                    RoleArn=self._eks_role_arn,
                    RoleSessionName='string',
                    WebIdentityToken=access_details,
                )
                if not response:
                    raise ImproperlyConfigured('Issue with token in pod. Check token at `{0}` with {1} '.format(TOKEN_PATH, self._eks_role_arn))
                session_created = True
            except ImportError:
                raise ImproperlyConfigured('Token not present in pod. Check token at `{0}` with {1} '.format(TOKEN_PATH, self._eks_role_arn))

    def __handle_local_dev_authentication(self):
        """
        creates an AWS session from ~/.aws/credentials file
        """
        return boto3.resource(SQS_SERVICE_NAME)
