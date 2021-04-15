def checkIfMessageIsForAction(logger, config, message, action_name):
    logger.debug("Received message: {}".format(message))
    action = message['message']['action']
    for configActionKey, configAction in config["action"].items():
        logger.debug("Check if action {} requested".format(configActionKey))
        if configActionKey.upper() == action.upper():
            logger.debug("Action {}, does match the requested key".format(configActionKey))
            if configAction["type"].upper() == action_name.upper():
                logger.info("Executing action {}".format(configAction["name"]))
                return True
    return False

