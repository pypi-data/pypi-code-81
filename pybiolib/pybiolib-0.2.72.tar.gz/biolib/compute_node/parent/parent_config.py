# pylint: skip-file TODO: Remove this line
import os

# The default recv buffer size 
DEFAULT_BUFFER_SIZE = 32768

# The recv buffer size for OK messages
OK_BUFFER_SIZE = 8

# The recv buffer size for receiving attestation document
ATTESTATION_DOC_BUFFER_SIZE = 65536

# Time in minutes before a Cmpute Node always shuts down
COMPUTE_NODE_SHUTDOWN_TIME_MINUTES = 1440 # 24 hours

# Time in minutes before a Compute Node running a job shuts down 
COMPUTE_NODE_RUNNING_JOB_SHUTDOWN_TIME_MINUTES = 30

# Port to connect to Enclave on
ENCLAVE_PORT = 5005

# Our ECR ID (AWS Account ID)
BIOLIB_AWS_ECR_ID = os.getenv('BIOLIB_AWS_ECR_REGISTRY_ID')

# The full URL to our ECR
BIOLIB_AWS_ECR_URL = f'{BIOLIB_AWS_ECR_ID}.dkr.ecr.eu-west-1.amazonaws.com'
