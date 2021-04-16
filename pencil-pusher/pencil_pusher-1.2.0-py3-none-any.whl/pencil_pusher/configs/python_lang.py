from typing import Any
from pencil_pusher.configs.manager import ConfigManager
from pencil_pusher.configs.base import ConfigParamBase
from pencil_pusher.configs import config_manager


@config_manager.register("python")
class PythonConfigParam(ConfigParamBase):
    """
    Processes the python config parameter

    Note: validation only validates config name
        and config type (string array)
    """

    _param_subtype = {
        # param name          type   requried   default
        "include_init_files": (bool, False, False),
        "include_main_file": (bool, False, False),
        "module": (str, False, ""),
    }

    def on_find(self, data: Any) -> Any:
        if data["type"] != ConfigManager.PROCESS_LANG_FILE:
            return super().on_find(data)

        if not data["contents"]["python"]["include_init_files"] and data[
            "file_path"
        ].endswith("__init__.py"):
            return (False, data["file_path"])
        if not data["contents"]["python"]["include_main_file"] and data[
            "file_path"
        ].endswith("__main__.py"):
            return (False, data["file_path"])
        return (True, data["file_path"])

    def on_register(self, data: Any):
        data["manager"].add_lang("python", ["py"])

    def on_iterate(self, data: Any):
        """
        This is the validate function
        """
        if data["type"] == ConfigManager.VALIDATE:
            self._validate(data["contents"])
            self.set_defined()

    def _validate(self, contents: dict) -> bool:
        """
        Validates the parameter is included in the
        config file since it is a required field
        """
        if "python" not in contents:
            contents["python"] = None
            return True

        if not isinstance(contents["python"], dict):
            raise ValueError("python config parameter is not of type dict")

        for key, value in self._param_subtype.items():
            if key not in contents["python"]:
                if value[1]:
                    raise ValueError(
                        f"python config key [{key}] is required but was not defined"
                    )
                contents["python"][key] = value[2]
                continue
            if not isinstance(contents["python"][key], value[0]):
                raise ValueError(
                    f"python config key [{key}] is invalid type, expected [{value[0]}] but found [{type(contents['python'][key])}]"
                )

        return True
