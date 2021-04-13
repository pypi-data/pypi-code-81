import logging

logger = logging.getLogger(__name__)


class Server:

    def __init__(self, service_name, queue_manager, encoder, router):
        self.queue_manager = queue_manager
        self.encoder = encoder
        self.router = router

        services = self.router.services
        queue_names = list()
        for service in services.keys():
            queue_names.append("{}_{}".format(service_name, service))

        self.queue_manager.connect()
        self.queue_manager.set_listening_queues(queue_names)
        self.queue_manager.init_service_consumption()

    def listen(self):
        message = None
        while message is None:
            self.queue_manager.wait_with_timeout()
            message = self.queue_manager.get_next()

        logger.debug("New message arrived. Length of the message is {} byte".format(len(message)))

        command = self.encoder.decode(message)
        result = self.router.invoke(command)
        command.result = result

        return
