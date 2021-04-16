from pencil_pusher.configs.base import ConfigParamBase
from pencil_pusher.configs import config_manager


@config_manager.register("titles")
class TitlesConfigParam(ConfigParamBase):
    """
    Processes the titles config parameter

    Note: validation only validates config name
        and config type (string array)
    """

    _param_subtype = {"source": (str, True), "title": (str, True)}

    def _validate(self, contents: dict) -> bool:
        """
        Validates the parameter is included in the
        config file since it is a required field
        """
        if "titles" not in contents:
            # not required
            return True

        if not isinstance(contents["titles"], list):
            raise ValueError("titles config parameter is not of type list")

        for element in contents["titles"]:
            if not isinstance(element, dict):
                raise ValueError("titles config entry must be of type dict")

            for key, value in self._param_subtype.items():
                if key not in element:
                    if value[1]:
                        raise ValueError(
                            f"titles config key [{key}] is required but was not defined"
                        )
                    continue
                if not isinstance(element[key], value[0]):
                    raise ValueError(
                        f"titles config key [{key}] is invalid type, expected [{value[0]}] but found [{type(element[key])}]"
                    )

        return True
