class ParetosError(Exception):
    pass


class ConfigError(ParetosError):
    pass


class InitializationError(ParetosError):
    pass


class KpiNotFoundInEvaluationResult(ParetosError):
    pass


class ProjectNotFoundError(ParetosError):
    pass
