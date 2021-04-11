from flask_scenario_testing.backend.modifiers.Modifier import Modifier
from time import sleep


class Sleep(Modifier):
    def identifier(self):
        return 'SLEEP'

    def modify(self, fun, endpoint_name, modifier_args: dict):
        def wrapper(*args, **kwargs):
            sleep_for = int(modifier_args.get('time')) / 1000
            sleep(sleep_for)

            return fun(*args, **kwargs)

        return wrapper