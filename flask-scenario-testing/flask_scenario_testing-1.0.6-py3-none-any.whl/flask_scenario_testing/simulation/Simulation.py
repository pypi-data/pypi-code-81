import datetime

from flask_scenario_testing.simulation.Api import Api
from flask_scenario_testing.simulation.ScenariosConfig import ScenariosConfig
import subprocess
import json
from time import sleep

from flask_scenario_testing.support.Time import Time


class Simulation(object):
    def __init__(self, api: Api, config: ScenariosConfig, locustfile: str):
        self.locustfile = locustfile
        self.api = api
        self.config = config

    def run(self, outputfile: str):
        print('Measuring travel time')
        start_time = datetime.datetime.utcnow()

        time_ = self.api.measure_travel_time()['current_time']

        server_time = datetime.datetime.fromisoformat(time_)

        travel_time_ms = (server_time - start_time).total_seconds() * 1000

        print('Travel time: {}'.format(travel_time_ms))

        print('Starting simulation')
        self.api.start_simulation()
        print('Successfully started simulation')

        scenarios = self.config.scenarios()
        print('Total number of scenarios: {}'.format(len(scenarios)))

        for i, scenario in enumerate(scenarios):
            print('Deploying scenario "{}"'.format(scenario.name()))

            self.api.start_scenario(scenario.name(), scenario.modifiers(), scenario.users_count())

            print('Starting load ...')
            self._run_locust(scenario.users_count(), scenario.run_time())

            self.api.stop_running_scenario()

            is_last_scenario = i == len(scenarios) - 1

            if not is_last_scenario and self.config.cooldown_time().seconds() > 0:
                self.await_cooldown(self.config.cooldown_time())

            print('Done')

        print('Stopping simulation')
        result = self.api.stop_simulation(travel_time_ms)
        print('Successfully stopped simulation, writing results to disk')

        with open(outputfile, 'w') as outfile:
            json.dump(result, outfile)

    def _run_locust(self, users_count, total_run_time: Time):
        args = [
            'locust',
            '-f', self.locustfile,
            '--host', self.api.host_url(),
            '--headless',
            '-u', str(users_count),
            '-r', str(users_count),
            '-t', str(total_run_time),
        ]
        p = subprocess.Popen(args, stdout=subprocess.DEVNULL, stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        run_time_left = total_run_time.seconds()

        while p.poll() is None:
            progress = round((total_run_time.seconds() - run_time_left) / total_run_time.seconds() * 100, 1)
            print('\rSimulating scenario ... {}%'.format(progress), end='')
            sleep(1)
            run_time_left -= 1

        print()

    def await_cooldown(self, cooldown: Time):
        run_time_left = cooldown.seconds()

        while run_time_left > 0:
            progress = round((cooldown.seconds() - run_time_left) / cooldown.seconds() * 100, 1)

            print('\rCooling down ... {}%'.format(progress), end='')
            sleep(1)
            run_time_left -= 1

        print()
