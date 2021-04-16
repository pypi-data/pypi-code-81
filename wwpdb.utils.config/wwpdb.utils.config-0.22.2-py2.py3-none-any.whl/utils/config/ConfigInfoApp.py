#
# File:    ConfigInfoApp.py
# Date:    17-Oct-2020
#
# Updates:
#
#
##
"""
Provides common access patterns for application configuration locations to minimize verbose site-config files
"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.01"

import os.path
import sys
import logging
import warnings

from wwpdb.utils.config.ConfigInfo import ConfigInfo

logger = logging.getLogger(__name__)


class ConfigInfoAppBase(object):
    """Base class to provide common application lookups"""

    def __init__(self, siteId=None, verbose=True, log=sys.stderr):
        self._cI = ConfigInfo(siteId=siteId, verbose=verbose, log=log)
        self._resourcedir = None
        self._referencedir = None

    def _getlegacy(self, key, default=None):
        """Retrieves key from configuration.  If key is found, provide a warning"""
        val = self._cI.get(key)
        if val is not None:
            # logging will repeat with each occurance
            self.__warndeprecated("Access key %s has been used but is deprecated" % key)
        else:
            val = default
        return val

    def _getresourcedir(self):
        if self._resourcedir is None:
            self._resourcedir = self._cI.get("RO_RESOURCE_PATH")
        return self._resourcedir

    def _getreferencedir(self):
        if self._referencedir is None:
            self._referencedir = self._cI.get("REFERENCE_PATH")
        return self._referencedir

    def __warndeprecated(self, msg):
        """Logs warning message"""
        # stacklevel is to get up high enough to get caller
        warnings.warn(msg, DeprecationWarning, stacklevel=4)


class ConfigInfoAppCommon(ConfigInfoAppBase):
    def __init__(self, siteId=None, verbose=True, log=sys.stderr):
        super(ConfigInfoAppCommon, self).__init__(siteId=siteId, verbose=verbose, log=log)

    def _get_pdbx_dictionary_name_dict(self):
        return self._cI.get("PDBX_DICTIONARY_NAME_DICT", {})

    def get_mmcif_deposit_dict_filename(self):
        return self._get_pdbx_dictionary_name_dict().get("DEPOSIT")

    def get_mmcif_archive_current_dict_filename(self):
        return self._get_pdbx_dictionary_name_dict().get("ARCHIVE_CURRENT")

    def get_mmcif_archive_next_dict_filename(self):
        return self._get_pdbx_dictionary_name_dict().get("ARCHIVE_NEXT")

    def get_mmcif_dict_path(self):
        reference_path = self._getreferencedir()
        site_pdbx_dict_path = os.path.join(reference_path, "dict")
        return self._getlegacy("SITE_PDBX_DICT_PATH", site_pdbx_dict_path)

    def get_mmcif_next_dictionary_file_path(self):

        mmcif_dictionary_name = self.get_mmcif_deposit_dict_filename()
        mmcif_dictionary_file_name = mmcif_dictionary_name + ".dic"
        newpath = os.path.join(self.get_mmcif_dict_path(), mmcif_dictionary_file_name)
        return self._getlegacy("SITE_MMCIF_DICT_FILE_PATH", newpath)


class ConfigInfoAppDepUI(ConfigInfoAppBase):
    def __init__(self, siteId=None, verbose=True, log=sys.stderr):
        super(ConfigInfoAppDepUI, self).__init__(siteId=siteId, verbose=verbose, log=log)

    def __get_depui_dir(self):
        """Returns the preferred path to depui subdir of resources_ro"""
        return os.path.join(self._getresourcedir(), "depui")

    def get_depui_resources_ro_dir(self):
        """Performs legacy lookup of depUI subdir referenced through DEPUI_RESOURCE_PATH.
        Returns either legacy or new hardcoded lookup"""
        return self._getlegacy("DEPUI_RESOURCE_PATH", self.__get_depui_dir())

    def get_site_access_info_file_path(self):
        newpath = os.path.join(self.__get_depui_dir(), "site_access_info.json")
        return self._getlegacy("SITE_ACCESS_INFO_FILE_PATH", newpath)

    def get_site_dataset_siteloc_file_path(self):
        newpath = os.path.join(self.__get_depui_dir(), "site_dataset_siteloc_info.json")
        return self._getlegacy("SITE_DATASET_SITELOC_FILE_PATH", newpath)


class ConfigInfoAppEm(ConfigInfoAppBase):
    """Access configuration for EM schema, resources, etc."""

    def __init__(self, siteId=None, verbose=True, log=sys.stderr):
        super(ConfigInfoAppEm, self).__init__(siteId=siteId, verbose=verbose, log=log)

    def __getemddir(self):
        """Returns preferred path to emd subdir of resources_ro"""
        return os.path.join(self._getresourcedir(), "emd")

    def __getlegacyemdpath(self):
        """Performs legacy lookup of emd subdir referenced through SITE_EM_DICT_PATH.
        Returns either legacy or new hardcoded lookup"""
        return self._getlegacy("SITE_EM_DICT_PATH", self.__getemddir())

    def get_emd_mapping_file_path(self):
        """Returns the full path to the em <-> emd translator configuration file"""
        # Formerly SITE_EXT_DICT_MAP_EMD_FILE_PATH provided the full path
        newpath = os.path.join(self.__getemddir(), "emd_map_v2.cif")
        val = self._getlegacy("SITE_EXT_DICT_MAP_EMD_FILE_PATH", newpath)
        return val

    def get_emd_fsc_scheme_file_path(self):
        """Returns the full path the EMD FSC schema file"""
        # Former access was through SITE_EM_DICT_PATH
        return os.path.join(self.__getlegacyemdpath(), "emdb_fsc.xsd")
