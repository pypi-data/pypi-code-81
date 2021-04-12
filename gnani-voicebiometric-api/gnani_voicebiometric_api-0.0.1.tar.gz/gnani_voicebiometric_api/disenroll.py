from configparser import ConfigParser
from gnani_voicebiometric_api.log_config.logger import get_logger
from gnani_voicebiometric_api.utils import voicebiometric_service

import os

current_dir = os.getcwd()

logger = get_logger(__name__)

# Reading from config file
parser = ConfigParser()
parser.read('user.config')

disenroll_api_url = "https://asr.gnani.ai/disenroll"


def start():
    """ Set all below parameters in the config file. """
    certificate = input("Enter the name of the certificate with extention: ")
    cert = current_dir + "/" + certificate

    speaker = input("Enter Speaker's name: ")
    try:
        logger.info("DisEnrollment Method ! - Start")

        # construct request headers
        headers = {
            "org": "biometric"
        }

        # construct request payload
        payload = {'speaker': speaker}
        """
            Request Gnani VoiceBiometric Service to enroll your voice
        """
        response = voicebiometric_service(disenroll_api_url, cert, headers, payload)
        logger.info("Response from VoiceBiometric server : {}".format(response))
        logger.info("DisEnrollment Method ! - End")
    except BaseException as e:
        logger.exception(e)
        logger.info("Exception in main method !")


if __name__ == '__main__':
    start()
