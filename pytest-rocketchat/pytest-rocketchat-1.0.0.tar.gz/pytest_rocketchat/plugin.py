import pytest

from .rocketchat import add_rocketchat_options, rocketchat_send_message


def pytest_addoption(parser):
    add_rocketchat_options(parser)


class TestResult:
    failed: int
    passed: int
    skipped: int
    error: int
    xfailed: int
    xpassed: int


@pytest.hookimpl(hookwrapper=True)
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    yield
    # special check for pytest-xdist plugin, cause we do not want to send report for each worker.
    if hasattr(terminalreporter.config, "workerinput"):
        return
    test_result = TestResult()
    test_result.failed = len(terminalreporter.stats.get("failed", []))
    test_result.passed = len(terminalreporter.stats.get("passed", []))
    test_result.skipped = len(terminalreporter.stats.get("skipped", []))
    test_result.error = len(terminalreporter.stats.get("error", []))
    test_result.xfailed = len(terminalreporter.stats.get("xfailed", []))
    test_result.xpassed = len(terminalreporter.stats.get("xpassed", []))
    if config.option.rocket_url and config.option.rocket_password:
        rocketchat_send_message(test_result, config, exitstatus)
