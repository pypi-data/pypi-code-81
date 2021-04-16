from sd_utils.plugins.plugin_collector import collect_plugins
from pencil_pusher.configs.base import ConfigParamBase
from pencil_pusher.configs.manager import ConfigManager


config_manager = ConfigManager()
"""
Global config manager (needed for the config register decorator it provides)
"""

__all__ = collect_plugins(
    __file__, __name__, ConfigParamBase, ["base", "manager"]
)
"""
Loads all the plugins and makes them accessible throughout the lifespan
of the program
"""
