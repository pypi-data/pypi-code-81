#
#  Copyright (c) 2018-2019 Renesas Inc.
#  Copyright (c) 2018-2019 EPAM Systems Inc.
#

import logging
import os
import shutil
from distutils.dir_util import copy_tree, mkpath
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from tempfile import TemporaryDirectory

from aos_signer.service_config.config_manager import ConfigManager
from aos_signer.service_config.configuration import Configuration, ConfigurationKeys
from aos_signer.service_config.keys_manager import KeyLoadException
from .file_details import FileDetails

logger = logging.getLogger(__name__)


class SignerException(Exception):
    pass


class SignerNonRegularFileException(SignerException):
    pass


class Signer:
    SERVICE_FOLDER = "service"
    DEFAULT_STATE_NAME = "default_state.dat"
    THREADS = cpu_count()
    SERVICE_FILE_ARCHIVE_NAME = 'service'

    ARCHIVED_SERVICE_NAME = ".".join([SERVICE_FILE_ARCHIVE_NAME, "tar", "gz"])

    def __init__(self, src_folder, package_folder):
        self._configuration = Configuration()
        self._src = src_folder
        self._package_folder = package_folder

    def process(self):
        try:
            with TemporaryDirectory() as tmp_folder:
                self._copy_application(folder=tmp_folder)
                self._copy_yaml_conf(folder=tmp_folder)
                self._copy_state(folder=tmp_folder)

                try:
                    self._generate_config(folder=tmp_folder)
                except SignerNonRegularFileException:
                    logger.error("Source code folder contains non-regular file(s). Unable to compose config.xml.")
                    return 1

                self._compose_archive(folder=tmp_folder)
        except (SignerException, KeyLoadException,) as exc:
            logger.error(str(exc))
            return 1

        logger.info("Done")

        return 0

    def _copy_state(self, folder):
        state_filename = self._configuration[ConfigurationKeys.DEFAULT_STATE]
        if state_filename:
            logger.info("Copying default state . . .")
            try:
                shutil.copy(
                    os.path.join(self._configuration.meta_folder, state_filename),
                    os.path.join(folder, self.DEFAULT_STATE_NAME)
                )
            except FileNotFoundError:
                raise SignerException(
                    "State file '{}' defined in the configuration does not exist.".format(state_filename)
                )

    def _copy_application(self, folder):
        logger.info("Copying application . . .")
        full_service_folder = os.path.join(folder, self.SERVICE_FOLDER)
        mkpath(full_service_folder)
        copy_tree(self._src, full_service_folder, preserve_symlinks=True)

    def _copy_yaml_conf(self, folder):
        logger.info("Copying configuration . . .")
        shutil.copyfile(self._configuration.get_conf_path(), os.path.join(folder, 'config.yaml'))

    def _generate_config(self, folder):
        logger.info("Generating config.xml . . .")
        file_details = self._calculate_file_hashes(folder=folder)
        config_manager = ConfigManager(path=folder)
        config_manager.generate(file_details=file_details)

    def _calculate_file_hashes(self, folder):
        pool = ThreadPool(self.THREADS)
        file_details = []
        src_len = len([item for item in folder.split(os.path.sep) if item])

        regular_files_only = True

        for root, dirs, files in os.walk(folder):
            splitted_root = [item for item in root.split(os.path.sep) if item][src_len:]
            if splitted_root:
                root = os.path.join(*splitted_root)
            else:
                root = ""

            # Check for links in directories
            for dir_name in dirs:
                full_dir_name = os.path.join(folder, root, dir_name)
                if os.path.islink(full_dir_name):
                    if self._configuration.get_symlinks() == 'delete':
                        logger.info("Removing non-regular directory '{}'".format(os.path.join(root, dir_name)))
                        os.remove(full_dir_name)
                    elif self._configuration.get_symlinks() == 'raise':
                        logger.error("This is not a regular directory '{}'.".format(os.path.join(root, dir_name)))
                        regular_files_only = False

            # Process files
            for file_name in files:
                full_file_name = os.path.join(folder, root, file_name)

                if os.path.islink(full_file_name):
                    if self._configuration.get_symlinks() == 'delete':
                        logger.info("Removing non-regular file '{}'".format(os.path.join(root, file_name)))
                        os.remove(full_file_name)
                    elif self._configuration.get_symlinks() == 'raise':
                        logger.error("This is not a regular file '{}'.".format(os.path.join(root, file_name)))
                        regular_files_only = False
                    continue

                file_details.append(FileDetails(
                    root=folder,
                    file=os.path.join(root, file_name)
                ))

        if not regular_files_only:
            raise SignerNonRegularFileException("Source code folder contains non regular file(s).")

        pool.map(FileDetails.calculate, file_details)

        return file_details

    def _compose_archive(self, folder):
        logger.info("Creating archive . . .")
        shutil.make_archive(os.path.join(self._package_folder, self.SERVICE_FILE_ARCHIVE_NAME), "gztar", folder)
