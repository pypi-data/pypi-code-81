from palaestrai.agent.objective import Objective


class DummyObjective(Objective):
    def __init__(self, reward=0, params={}):
        self.reward = reward
        self.params = params

    def internal_reward(self, **kwargs):
        return self.reward
