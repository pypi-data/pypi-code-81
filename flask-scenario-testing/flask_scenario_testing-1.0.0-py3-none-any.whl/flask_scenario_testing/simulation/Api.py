import requests
from Host import Host


class Api(object):
    def __init__(self, host: Host):
        self.host = host

    def start_simulation(self):
        response = requests.post(self.host.url('api/simulation/start'))

        assert response.status_code == 200, 'Request to start simulation failed, are you sure the host is up?'

    def stop_simulation(self, adjust_ms: float):
        response = requests.post(self.host.url('api/simulation/stop'), json=dict(
            adjust_ms=str(adjust_ms)
        ))

        assert response.status_code == 200, 'Request to stop simulation failed due to an unknown error'

        return response.json()

    def start_scenario(self, name, modifiers, meta):
        response = requests.post(self.host.url('/api/simulation/start-scenario'), json=dict(
            modifiers=modifiers,
            meta=meta,
            name=name
        ))

        assert response.status_code == 200

    def host_url(self):
        return self.host.url()

    def stop_running_scenario(self):
        response = requests.post(self.host.url('/api/simulation/stop-running-scenario'))

        assert response.status_code == 200

    def measure_travel_time(self):
        response = requests.post(self.host.url('/api/measure-travel-time'))

        assert response.status_code == 200

        return response.json()
