from swimlane_platform.lib.names import names
from swimlane_platform.lib.debug_decorators import info_function_start_finish
from swimlane_platform.shared_steps import enable_turbine
from swimlane_platform.upgrade_steps.upgrade_step import UpgradeStep
import semver


class UpgradeFrom1013To1020(UpgradeStep):
    FROM = semver.parse_version_info('10.1.3')  # type: semver.VersionInfo
    TO = semver.parse_version_info('10.2.0')  # type: semver.VersionInfo

    @info_function_start_finish('Upgrade From 10.1.3 To 10.2.0.')
    def process(self):
        # type: () -> None
        enable_turbine.run(self.config)
        self.upgrade_standard_images(self.config.args.dev, names.INSTALL_DIR).save()
