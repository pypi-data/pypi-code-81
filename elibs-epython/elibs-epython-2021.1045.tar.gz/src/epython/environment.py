# -*- coding: utf-8 -*-
"""
Description:
    This module contains the environment constructs that are used globally for epython.

    NOTE: This module should remain small!

Author:
    Ray Gomez

Date:
    12/7/20
"""
import os

from epython.logger import setup_logging

#########################################################################################################
# Environmental overrides                                                                               #
#########################################################################################################
EPYTHON_LOG_LEVEL = os.getenv("EPYTHON_LOG_LEVEL")
EPYTHON_LOG_FILE = os.getenv("EPYTHON_LOG_FILE")

#########################################################################################################
# Retry overrides                                                                                       #
#########################################################################################################
EPYTHON_SSH_RETRIES = os.getenv("EPYTHON_SSH_RETRIES") or 3
EPYTHON_SSH_RETRY_INTERVAL = os.getenv("EPYTHON_SSH_RETRY_INTERVAL") or 5

#########################################################################################################
# Request Components                                                                                    #
#########################################################################################################
EPYTHON_REQUEST_ID = os.getenv("EPYTHON_REQUEST_ID", "epython-poke")
EPYTHON_REQUEST_INTERVAL = os.getenv("EPYTHON_REQUEST_INTERVAL") or 5
EPYTHON_REQUEST_RETRIES = os.getenv("EPYTHON_REQUEST_RETRIES") or 5

#########################################################################################################
# SSH Components                                                                                        #
#########################################################################################################
EPYTHON_SSH_KEY = os.getenv("EPYTHON_SSH_KEY")

#########################################################################################################
# Setup logging for the library                                                                         #
#########################################################################################################
_LOG = setup_logging(log_level=EPYTHON_LOG_LEVEL, log_file=EPYTHON_LOG_FILE)
