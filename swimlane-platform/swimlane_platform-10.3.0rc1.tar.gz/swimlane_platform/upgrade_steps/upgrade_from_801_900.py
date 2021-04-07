from os import path
from swimlane_platform.lib import DockerComposeFileManager, DockerImage, names, \
    info_function_start_finish, debug_function_args
from swimlane_platform.upgrade_steps.upgrade_step import UpgradeStep
import semver


class UpgradeFrom801To900(UpgradeStep):
    FROM = semver.parse_version_info('8.0.1')  # type: semver.VersionInfo
    TO = semver.parse_version_info('9.0.0')  # type: semver.VersionInfo

    @info_function_start_finish('Upgrade From 8.0.1 To 9.0.0')
    def process(self):
        # type: () -> None
        self.upgrade_image_versions(names.INSTALL_DIR, self.config.args.dev)

    @debug_function_args
    def upgrade_image_versions(self, install_dir, dev):
        # type: (str, bool) -> None
        """
        Changes image versions to the new ones
        :param dev: If the images will be pulled from development repository.
        :param install_dir: Root folder for installation. Where docker-compose resides.
        """
        docker_compose = self.upgrade_standard_images(dev, install_dir)
        docker_compose.set('mongo:4.0.9', 'services', names.SW_MONGO, 'image')
        docker_compose.save()

