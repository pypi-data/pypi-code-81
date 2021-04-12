from configparser import ConfigParser
from gnani_voicebiometric_api.log_config.logger import get_logger
from gnani_voicebiometric_api.utils import voicebiometric_service

import os

current_dir = os.getcwd()

logger = get_logger(__name__)

# Reading from config file
parser = ConfigParser()
parser.read('user.config')

authenticate_api_url = "https://asr.gnani.ai/authenticate"

def start():
    """ Set all below parameters in the config file. """
    certificate = input("Enter the name of the certificate with extention: ")
    cert = current_dir + "/" + certificate

    audio_name = input("Enter the full name of the audiofile with extention: ")
    audio_file = current_dir + "/" + audio_name

    speaker = input("Enter Speaker's name: ")
    try:
        logger.info("Authenticate Method ! - Start")

        # construct request headers
        headers = {
            "org": "biometric"
        }

        # construct request payload
        payload = {'speaker': speaker}

        files = {'audio_file': open(audio_file, 'rb')}
        """
            Request Gnani VoiceBiometric Service to enroll your voice
        """
        response = voicebiometric_service(authenticate_api_url, cert, headers, payload, files)
        logger.info("Response from VoiceBiometric server : {}".format(response))
        logger.info("Authenticate Method ! - End")
    except BaseException as e:
        logger.exception(e)
        logger.info("Exception in main method !")


if __name__ == '__main__':
    start()
