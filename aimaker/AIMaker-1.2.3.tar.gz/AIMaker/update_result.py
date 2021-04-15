import os
import requests
import json
import logging

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

KEY_RESULT_VALUE = "result"
KEY_SCORE_VALUE = "scores"
KEY_POD_NAME = "podName"


def sendUpdateRequest(result):

    if isinstance(result, (int, float)) is False:
        logging.error(
            "[TypeError] Data type ({}) of result is not allowed".format(str(type(result))))
        return "Update result failed, please check data type of result."

    try:
        if "ASUS_CLOUDINFRA_JOB_ID" in os.environ:
            jobId = os.getenv('ASUS_CLOUDINFRA_JOB_ID')
        if "ASUS_CLOUDINFRA_RUN_ID" in os.environ:
            trialId = os.getenv('ASUS_CLOUDINFRA_RUN_ID')
        if "ASUS_CLOUDINFRA_TOKEN" in os.environ:
            token = os.getenv('ASUS_CLOUDINFRA_TOKEN')
        if "ASUS_CLOUDINFRA_API_HOST" in os.environ:
            url = os.getenv('ASUS_CLOUDINFRA_API_HOST')

        # This environment value was deprecated
        if "ASUS_JOB_ID" in os.environ:
            jobId = os.getenv('ASUS_JOB_ID')
        if "ASUS_JOB_RUN_ID" in os.environ:
            trialId = os.getenv('ASUS_JOB_RUN_ID')
        if "AI_MAKER_TOKEN" in os.environ:
            token = os.getenv('AI_MAKER_TOKEN')
        if "AI_MAKER_HOST" in os.environ:
            url = os.getenv('AI_MAKER_HOST')

        # For hybrid cloud
        if "ASUS_CLOUDINFRA_TRIAL_ID" in os.environ:
            trialId = os.getenv('ASUS_CLOUDINFRA_TRIAL_ID')
        if "ASUS_CLOUDINFRA_SERVICE_TYPE" in os.environ:
            serviceType = os.getenv('ASUS_CLOUDINFRA_SERVICE_TYPE')

    except KeyError as e:
        logging.error("[KeyError] Please assign {} value".format(str(e)))
        return "Update result failed, please contact your system administrator"

    HEADERS = {"content-type": "application/json",
               "Authorization": "bearer "+token}
    body = json.dumps({KEY_RESULT_VALUE: float(result)})

    if serviceType == "NORMAL" or serviceType == "AI_MAKER":
        url = url+"/api/v1/ai-maker/callback/results/jobs/"+jobId+"/trials/"+trialId
    if serviceType == "SMTR":
        url = url+"/api/v1/ai-maker/callback/results/remote-jobs/"+jobId+"/trials/"+trialId

    logging.debug("Headers: {}".format(HEADERS))
    logging.debug("Body: {}".format(body))
    logging.debug("Url: {}".format(url))

    try:
        r = requests.post(url, data=body, headers=HEADERS)
        logging.debug("Reponse: {}".format(r.text))
        r.raise_for_status()
        return "Update result OK"
    except requests.exceptions.HTTPError as errh:
        logging.error("Http Error: {}".format(errh))
    except requests.exceptions.ConnectionError as errc:
        logging.error("Error Connecting: {}".format(errc))
    except requests.exceptions.Timeout as errt:
        logging.error("Timeout Error: {}".format(errt))
    except requests.exceptions.RequestException as err:
        logging.error("OOps: Something Else {}".format(err))

    return "Update result failed, please contact your system administrator"


def sendScoresRequest(scores):

    # check data type is dict
    if isinstance(scores, dict) is False:
        logging.error(
            "[TypeError] Data type ({}) of scores is not allowed".format(str(type(scores))))
        return "Update scores failed, please check data type of scores."

    try:
        if "ASUS_CLOUDINFRA_JOB_ID" in os.environ:
            jobId = os.getenv('ASUS_CLOUDINFRA_JOB_ID')
        if "ASUS_CLOUDINFRA_RUN_ID" in os.environ:
            trialId = os.getenv('ASUS_CLOUDINFRA_RUN_ID')
        if "ASUS_CLOUDINFRA_TOKEN" in os.environ:
            token = os.getenv('ASUS_CLOUDINFRA_TOKEN')
        if "ASUS_CLOUDINFRA_API_HOST" in os.environ:
            url = os.getenv('ASUS_CLOUDINFRA_API_HOST')

        # This environment value was deprecated
        if "ASUS_JOB_ID" in os.environ:
            jobId = os.getenv('ASUS_JOB_ID')
        if "ASUS_JOB_RUN_ID" in os.environ:
            trialId = os.getenv('ASUS_JOB_RUN_ID')
        if "AI_MAKER_TOKEN" in os.environ:
            token = os.getenv('AI_MAKER_TOKEN')
        if "AI_MAKER_HOST" in os.environ:
            url = os.getenv('AI_MAKER_HOST')

        # For hybrid cloud
        if "ASUS_CLOUDINFRA_TRIAL_ID" in os.environ:
            trialId = os.getenv('ASUS_CLOUDINFRA_TRIAL_ID')
        if "ASUS_CLOUDINFRA_SERVICE_TYPE" in os.environ:
            serviceType = os.getenv('ASUS_CLOUDINFRA_SERVICE_TYPE')

    except KeyError as e:
        logging.error("[KeyError] Please assign {} value".format(str(e)))
        return "Update scores failed, please contact your system administrator"

    HEADERS = {"content-type": "application/json",
               "Authorization": "bearer "+token}
    body = json.dumps({KEY_SCORE_VALUE: scores})

    if serviceType == "NORMAL" or serviceType == "AI_MAKER":
        url = url+"/api/v1/ai-maker/callback/scores/jobs/"+jobId+"/trials/"+trialId
    if serviceType == "SMTR":
        url = url+"/api/v1/ai-maker/callback/results/remote-jobs/"+jobId+"/trials/"+trialId

    logging.debug("Headers: {}".format(HEADERS))
    logging.debug("Body: {}".format(body))
    logging.debug("Url: {}".format(url))

    try:
        r = requests.post(url, data=body, headers=HEADERS)
        logging.debug("Reponse: {}".format(r.text))
        r.raise_for_status()
        return "Update scores OK"
    except requests.exceptions.HTTPError as errh:
        logging.error("Http Error: {}".format(errh))
    except requests.exceptions.ConnectionError as errc:
        logging.error("Error Connecting: {}".format(errc))
    except requests.exceptions.Timeout as errt:
        logging.error("Timeout Error: {}".format(errt))
    except requests.exceptions.RequestException as err:
        logging.error("OOps: Something Else {}".format(err))

    return "Update scores failed, please contact your system administrator"


def saveValidationResult(result):

    if isinstance(result, (int, float)) is False:
        logging.error(
            "[TypeError] Data type ({}) of result is not allowed".format(str(type(result))))
        return "Update result failed, please check data type of result."

    try:
        if "ASUS_CLOUDINFRA_JOB_ID" in os.environ:
            cronjob = os.getenv('ASUS_CLOUDINFRA_JOB_ID')
        if "ASUS_CLOUDINFRA_TOKEN" in os.environ:
            token = os.getenv('ASUS_CLOUDINFRA_TOKEN')
        if "ASUS_CLOUDINFRA_API_HOST" in os.environ:
            url = os.getenv('ASUS_CLOUDINFRA_API_HOST')
        if "HOSTNAME" in os.environ:
            HOSTNAME = os.getenv('HOSTNAME')

        # This environment value was deprecated
        if "AI_MAKER_CRONJOB_ID" in os.environ:
            cronjob = os.getenv('AI_MAKER_CRONJOB_ID')
        if "AI_MAKER_TOKEN" in os.environ:
            token = os.getenv('AI_MAKER_TOKEN')
        if "AI_MAKER_HOST" in os.environ:
            url = os.getenv('AI_MAKER_HOST')

    except KeyError as e:
        logging.error("[KeyError] Please assign {} value".format(str(e)))
        return "Update result failed, please contact your system administrator"

    HEADERS = {"content-type": "application/json",
               "Authorization": "bearer "+token}
    body = json.dumps({KEY_RESULT_VALUE: float(
        result), KEY_POD_NAME: str(HOSTNAME)})
    url = url+"/api/v1/ai-maker/callback/results/validations/"+cronjob

    logging.debug("Headers: {}".format(HEADERS))
    logging.debug("Body: {}".format(body))
    logging.debug("Url: {}".format(url))

    try:
        r = requests.post(url, data=body, headers=HEADERS)
        logging.debug("Reponse: {}".format(r.text))
        r.raise_for_status()
        return "Update result OK"
    except requests.exceptions.HTTPError as errh:
        logging.error("Http Error: {}".format(errh))
    except requests.exceptions.ConnectionError as errc:
        logging.error("Error Connecting: {}".format(errc))
    except requests.exceptions.Timeout as errt:
        logging.error("Timeout Error: {}".format(errt))
    except requests.exceptions.RequestException as err:
        logging.error("OOps: Something Else {}".format(err))

    return "Update result failed, please contact your system administrator"
