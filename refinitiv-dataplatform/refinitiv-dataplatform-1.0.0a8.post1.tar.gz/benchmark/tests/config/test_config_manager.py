from benchmark.config import ConfigManager


def test_config_manager_init():
    manager = ConfigManager('../config.ini')

    assert manager.config_console == {}

    assert manager.config_benchmark == ""

    assert manager.basic_config.get_web_port()
