from salal.core import config, actions
config.initialize()
actions.initialize()
actions.execute(config.action)
