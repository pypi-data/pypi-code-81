import json

# The name of the 'apply juniper config' task in junos_ansible project.
JUNIPER_CONFIG_TASK_NAME='apply templated configuration to juniper device'

class AnsibleResults:
    def __init__(self):
        self.results = {}
    
    def items(self):
        return self.results.items()

    def _initialize_task_results(self, task_name):
        if task_name not in self.results:
            self.results[task_name] = AnsibleTaskResults()

    def add_error(self, task_name, host_name, err):
        self._initialize_task_results(task_name)
        self.results[task_name].add_error(host_name, err)

    def add_diff(self, task_name, host_name, diff):
        self._initialize_task_results(task_name)
        self.results[task_name].add_diff(host_name, diff)


class AnsibleTaskResults:
    def __init__(self):
        self.errors = {}
        self.diffs = {}
    
    def add_error(self, host_name, err):
        self.errors[host_name] = err

    def add_diff(self, host_name, diff):
        self.diffs[host_name] = diff
    

class AnsibleJSONParser:
    def __init__(self):
        self.results = AnsibleResults()

    def parse(self, json_payload):
        """Take the json output of an ansible-playbook run, determine success or failure, and return a relevent message.

        Args:
            json_payload: The raw json output from running ansible-playbook. This can be configured in the ansible.cfg file under [Defaults] > stdout_callback = json
        Requirements:
            Playbook runs need to be ran with --diff to get the correct output.
        """
        try:
            output = json.loads(json_payload)
        except json.JSONDecodeError as e:
            msg = 'Unable to parse provided JSON argument due to a JSON Decode error -- there is something wrong with the provided JSON input.'
            raise ValueError(msg) from e

        # We should only have one play here, so let's make that assumption and allow the index error to take place otherwise.
        play = output['plays'][0]
        # Check if any hosts failed.
        for task in play['tasks']:
            task_name = task['task']['name']
            for host_name, host in task['hosts'].items():
                # Handle exception.
                if 'exception' in host:
                    self.results.add_error(task_name, host_name, host['exception'])
                if 'failed' in host and host['failed']:
                    self.results.add_error(task_name, host_name, host['msg'])
                # Only grab the diff from the "apply templated configuration to juniper device" task.
                if task_name == JUNIPER_CONFIG_TASK_NAME:
                    # Only grab the diff if there is a 'prepared diff' available.
                    if 'changed' in host and host['changed'] and 'diff' in host and 'prepared' in host['diff']:
                        self.results.add_diff(task_name, host_name, host['diff']['prepared'])
                    else:
                        # TODO Ensure that 'no changes' message really makes sense here (we should inspect the 'diff' object in some more scenarios maybe).
                        self.results.add_diff(task_name, host_name, "++++ No changes ++++\n(There was no 'Prepared' diff in the provided json.)")

        return self.results