import os


def init():
    global BASE_URL
    global LOCAL_PATH
    global LOCAL_DIR
    global DOCKERFILES_LOC
    global LAMBDA_FUNCTION_DIR
    global S3_CLDZ_PRESIGNED_ENDPOINT

    BASE_URL="https://betaconsole.clouderizer.com"

    LOCAL_PATH=os.getenv("HOME") + "/.clouderizer/creds"
    if "beta" in BASE_URL:
	    LOCAL_PATH = os.getenv("HOME") + "/.clouderizer/beta/creds"
    LOCAL_DIR=os.getenv("HOME") + "/.clouderizer"
    DOCKERFILES_LOC = LOCAL_DIR+"/dockerfiles/"
    LAMBDA_FUNCTION_DIR = LOCAL_DIR+ "/lambda-dir/function/"

    S3_CLDZ_PRESIGNED_ENDPOINT = BASE_URL + '/api/awsconfig/generatepresignedurl'
