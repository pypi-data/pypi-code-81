

class SimpleRouter:

    def __init__(self, services):
        self.services = services

    def invoke(self, command):
        result = self.services[command.method_name](*command.params)
        return result
