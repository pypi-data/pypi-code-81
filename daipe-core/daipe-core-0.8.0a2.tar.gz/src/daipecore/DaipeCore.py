from injecta.package.path_resolver import resolve_path
from pyfonycore.bootstrap.config.config_reader import read  # noqa: F401
from pyfonybundles.Bundle import Bundle


class DaipeCore(Bundle):

    config_reader = read

    def modify_raw_config(self, raw_config: dict) -> dict:
        bootstrap_config = DaipeCore.config_reader()

        if "daipe" in raw_config["parameters"]:
            raise Exception("parameters.daipe must not be explicitly defined")

        raw_config["parameters"]["daipe"] = {
            "root_module": {
                "name": bootstrap_config.root_module_name,
                "path": resolve_path(bootstrap_config.root_module_name).replace("\\", "/"),
            }
        }

        return raw_config
