"""
IBM Confidential
OCO Source Materials
5737-H76, 5725-W78, 5900-A1R
(c) Copyright IBM Corp. 2020 All Rights Reserved.
The source code for this program is not published or otherwise divested of its trade secrets,
irrespective of what has been deposited with the U.S. Copyright Office.
"""
#!/usr/bin/env python3

import re
import sys
import os
import time
import logging
import argparse
from zipfile import ZipFile

fl_path = os.path.abspath('.')
if fl_path not in sys.path:
    sys.path.append(fl_path)

import ibmfl.envs as fl_envs
from ibmfl._version import __version__
from ibmfl.connection.router_handler import Router
from ibmfl.message.message import Message
from ibmfl.message.message_type import MessageType
from ibmfl.exceptions import FLException
from ibmfl.connection.route_declarations import get_party_router
import ibmfl.util.config as fl_config
from ibmfl.util.config import read_yaml_config, get_class_by_name, \
	configure_logging_from_file, get_party_config, convert_bytes_to_zip

logger = logging.getLogger(__name__)


class Party:
    """
    Party participates in Federated Learning training.  
    """

    def __init__(self, **kwargs):
        """
        Initializes a party based on the configuration provided in 
        either a yaml file or a dictionary.
        :param config_file: path to yml file with the configuration of the party
        :type config_file: `str`
        :param config_dict: dictionary containing the configuration of the party
        :type config_dict: `dict`
        :return None
        """
        configure_logging_from_file()

        config_file = kwargs.get('config_file')
        config_dict = kwargs.get('config_dict')
        if config_file != None: 
            config_dict = fl_config.read_yaml_config(config_file=config_file)

        config_dict['connection']['name'] = 'WSConnection'
        config_dict['connection']['path'] = 'ibmfl.connection.websockets_connection'
        
        cls_config = fl_config.get_cls_by_config(config_dict)

        self.party_config = cls_config

        self.data_handler = None
        self.fl_model = None
        self.is_running = False

        data_config = cls_config.get('data')
        connection_config = cls_config.get('connection')
        ph_config = cls_config.get('protocol_handler')

        try:
            # Load data (optional field)
            # - in some cases the aggregator doesn't have data for testing purposes
            data_cls_ref = data_config.get('cls_ref')
            data_info = data_config.get('info')
            self.data_handler = data_cls_ref(data_config=data_info)

            # Read and create model (optional field)
            # In some cases aggregator doesn't need to load the model:
            
            self.fl_model = None

            # Load hyperparams
            self.hyperparams = cls_config.get('hyperparams')
            self.agg_info = cls_config.get('aggregator')

            connection_cls_ref = connection_config.get('cls_ref')
            self.connection_info = connection_config.get('info')
            self.connection_info["VERSION"] = __version__
            connection_synch = connection_config.get('sync')
            # Use opt-in privacy for WML, to get metrics by default
            connection_private = self.connection_info.get('private',False)
            self.connection = connection_cls_ref(self.connection_info)
            self.connection.initialize_sender()


            self.local_training_handler = None
        
            ph_cls_ref = ph_config.get('cls_ref')

            self.proto_handler = ph_cls_ref(self.fl_model,
                                            self.connection.sender,
                                            self.data_handler,
                                            self.local_training_handler,
                                            agg_info=self.agg_info,
                                            synch=connection_synch,
                                            is_private=connection_private)

            self.router = Router()
            get_party_router(self.router, self.proto_handler)

            self.connection.initialize_receiver(router=self.router)

            # check for token
            token = kwargs.get('token', None)
            self_signed_cert_flag = kwargs.get('self_signed_cert', None)
            self.connection.initialize(self.router, self.agg_info, self_signed_cert_flag, token)

        except Exception as ex:
            logger.info('Error occurred '
                        'while loading aggregator configuration')
            logger.exception(ex)
        else:
            logger.info("Party initialization successful")

        self.agg_info = cls_config.get('aggregator')


    def initialize_model_config(self):
        logger.info('Initializing model configuration')
        cls_config = self.party_config
        model_config = cls_config.get('model')
        lt_config = cls_config.get('local_training')
        try:
            
            # Read and create model (optional field)
            # In some cases aggregator doesn't need to load the model:
            model_cls_ref = model_config.get('cls_ref')
            spec = model_config.get('spec')
            self.fl_model = model_cls_ref('', spec)

            # Load hyperparams
            self.hyperparams = cls_config.get('hyperparams')

            lt_cls_ref = lt_config.get('cls_ref')
            self.local_training_handler = lt_cls_ref(
                self.fl_model, self.data_handler)

            self.proto_handler.set_model(self.fl_model)
            self.proto_handler.set_training_handler(self.local_training_handler)
            

        except Exception as ex:
            logger.info('Error occurred '
                        'while loading model and lth configuration')
            logger.exception(ex)
        else:
            logger.info("Party model initialization successful")

    def register_party(self):
        """
        Registers party with the aggregator.

        :param: None
        :return: None
        """
        logger.info('Registering party...')
        returnValue = False
        register_message = Message(
            MessageType.REGISTER.value, data=self.connection_info)
        try:
            response = self.connection.sender.send_message(
                self.agg_info, register_message)
            if response is not None and response.get_data()['status'] == 'success':

                data = response.get_data()
                if self.extract_model_from_stream(data):
                    logger.info('Registration Successful')
                    returnValue = True
                else:
                    logger.info('Registration Failed: Model processing error')
                    returnValue = False
            else:
                logger.error('Registration Failed: Failure status from aggregator')
        except Exception as ex:
            logger.error("Error occurred during registration" + str(ex))

        return returnValue

    def stop_connection(self):
        """
        Stop the connection to the aggregator

        :param: None
        :return: None
        """
        try:
            self.connection.stop()

        except Exception as ex:
            logger.error("Error occurred during stop")
            logger.error(ex)
        else:
            logger.info("Party stop successful")

    def evaluate_model(self):
        """
        Calls function that evaluates current model with local testing data
        and prints the results.

        :param: None
        :return: None
        """
        try:
            self.proto_handler.print_evaluate_local_model()

        except Exception as ex:
            logger.error("Error occurred during evaluation.")
            logger.error(ex)

    def start(self):
        """
        Initializes connection and registers with the aggregator,
        then accept commands from the aggregator to effect training.  

        :param: None
        :return: None
        """

        if not self.is_running:
            logger.info('Party not registered yet.')
            if self.register_party():
                logger.info('Listening for commands from Aggregator')
                self.is_running = True
                self.initialize_model_config()
        else:
            logger.info('Party already running.')

    def extract_model_from_stream(self, data):
        """Read model from response stream and extract the content.
        :param data: response data recieved from aggregator.
        :type data: `json` 
        :return: None
        """
        returnValue = False
        working_dir = fl_envs.working_directory

        if 'model_package' in data:
            logger.info(
                'Model Package found, placing in working_dir ' + working_dir)
            model_file_name = 'model_package.zip'
            model_file_op = os.path.join(working_dir, model_file_name)
            model_pk_bytes = data.get('model_package')

            try:
                convert_bytes_to_zip(model_pk_bytes, model_file_op)

                with ZipFile(model_file_op, 'r') as o:
                    o.extractall(working_dir)

            except Exception as ex:
                logger.exception(
                    "Error occurred while unpacking model package from aggregator.")
                raise FLException(
                    "Error occurred while downloading model package. ")
        else:
            logger.info("No model package received from aggregator.")

        logger.info('Checking for model config in payload.')

        model_config_agg = data.get('model_config', None)
        if model_config_agg == None:
            logger.info("No model config received from aggregator.")
            return returnValue
        
        if 'is_model_working_dir' in model_config_agg.get('spec'):
            model_config_agg['spec']['model_definition'] = working_dir
            
        elif 'model_definition' in  model_config_agg.get('spec'):
            model_def = os.path.join(working_dir, model_config_agg['spec']['model_definition'])
            model_config_agg['spec']['model_definition'] = model_def

        logger.info(model_config_agg)
        self.party_config['model'] = model_config_agg

        logger.info('model extract finished!')
        returnValue = True
        return returnValue


if __name__ == '__main__':
    """
    Main function to run a party-side application in a Federated Learning training job.
    The application can either be run in an interactive ( -i ), or a non-interactive
    mode.  

    In interactive mode, enter commands:

    START     - Start the connection for communication with the aggregator
    STOP      - Stop the connection 
    REGISTER  - Register with the aggregator and start accepting commands
    EVAL      - Evaluate the model with local test data

    In non-interactive mode, the party will be started, and registered with
    the aggregator.  After training is complete and a STOP message is received
    from the aggregator, the application will exit.

    """

    parser = argparse.ArgumentParser(
        description='WML Federated Learning Party')
    parser.add_argument('config_file', help='yaml configuration file')
    parser.add_argument('token', help='authentication token')
    parser.add_argument('-s', '--self_signed_cert', help='flag for self-signed certificate', action='store_true')
    parser.add_argument('-i', '--interactive',
                        help='run interactively', action='store_true')

    args = parser.parse_args()

    
    if (args.self_signed_cert):
        self_signed_cert_arg = True
    else:
        self_signed_cert_arg = None

    p = Party(config_file=args.config_file, token=args.token, self_signed_cert=self_signed_cert_arg)
    if (args.interactive):
        # Indefinite loop to accept user commands to execute
        while 1:
        	
            try:
                msg = sys.stdin.readline()
                if re.match('START', msg):
                    p.start()

                if re.match('STOP', msg):
                    p.stop_connection()
                    break

                if re.match('REGISTER', msg):
                    p.register_party()

                if re.match('EVAL', msg):
                    p.evaluate_model()

            except Exception as ex:
                logger.error("Error occurred during " + msg)
                logger.error(ex)
    else:
        try:
            p.start()
        except Exception as ex:
            logger.error("Error occurred during start")
            logger.error(ex)
            p.stop_connection()

        while not p.connection.stopped:
            logger.debug("Party is still running")
            time.sleep(10)
        logger.info("Party is complete")
