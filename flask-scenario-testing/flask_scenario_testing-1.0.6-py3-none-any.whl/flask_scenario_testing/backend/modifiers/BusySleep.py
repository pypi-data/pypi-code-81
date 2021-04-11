import time

from flask_scenario_testing.backend.modifiers.Modifier import Modifier


class BusySleep(Modifier):
    def identifier(self):
        return 'BUSY_SLEEP'

    def modify(self, fun, endpoint_name, modifier_args: dict):
        def wrapper(*args, **kwargs):
            sleep_for = int(modifier_args.get('time')) / 1000

            time_start = time.time()

            while time.time() < time_start + sleep_for:
                pass

            return fun(*args, **kwargs)

        return wrapper
