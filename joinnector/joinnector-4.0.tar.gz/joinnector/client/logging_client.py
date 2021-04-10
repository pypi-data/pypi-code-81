import logging

from joinnector.helper.constant_helper import ConstantHelper


class LoggingClient(object):
    def __init__(self):
        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=10)

    def process_ie_log(self, **kwargs):
        kwargs.update(
            {"service": ConstantHelper.get_setting_constant().SERVICE_NAME})
        getattr(logging, kwargs.get("level", "debug"))(
            **kwargs, stack_info=True)
