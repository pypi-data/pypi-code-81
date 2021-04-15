"""Parametrization and options."""
from pathlib import Path
from . import desktop_file


class Default:
    """Default parameter (to be properly overridden)"""
    NAME = 'firefox-stable'
    LANG = 'en_US'
    VERBOSE = False
    INIDESKTOP = False
    INIPROFILEDESKTOP = False
    url_get_latest = ('https://download.mozilla.org/?product='
                      'firefox-latest-ssl&os=linux64&lang={lang}')
    tmp_folder = Path('/tmp')

    def __new__(cls, *args, **kwargs):
        """Polimorphism to get the wanted configuration class"""
        if kwargs.get('user') == 'root':
            return super().__new__(DefaultRoot)
        if kwargs.get('user'):
            return super().__new__(DefaultUser)
        return super().__new__(DefaultUser, *args, **kwargs)

    def __init__(self, user=None, **kwargs):
        global _CONFIGURATION  # pylint: disable=global-statement
        self.user = user
        for key, value in kwargs.items():
            self.set_value(key, value)
        _CONFIGURATION = self

    def set_value(self, key, value):
        """Properly set the extra parameters"""
        if not hasattr(self, key):
            raise SystemError(f"Parameter {key} not supported")
        if hasattr(self, f'_{key}'):
            getattr(self, f'_{key}')(value)
            return
        setattr(self, key, value)

    @property
    def binaries_path(self):
        """Where binaries will be installed"""
        return Path(self.BINARIES_FOLDER) / self.NAME

    @property
    def firefox_binary(self):
        """Executable of firefox binary"""
        return self.binaries_path / 'firefox'

    @property
    def desktop_file(self):
        """.desktop file definition"""
        return desktop_file.TEMPLATE.format(
                name=self.NAME,
                exec=f'{self.firefox_binary} %u',
                icon=self.binaries_path / 'browser/chrome/icons/default/default128.png')

    @property
    def profile_desktop_file(self):
        """.desktop file definition for profile switcher"""
        return desktop_file.TEMPLATE.format(
                name=f'{self.NAME}-profile',
                exec=f'{self.firefox_binary} --no-remote -P',
                icon=self.binaries_path / 'browser/chrome/icons/default/default128.png')

    @property
    def lang4download(self):
        """For download, substitude lower to middle dash"""
        return self.LANG.replace('_', '-')
    @property
    def desktop_file_path(self):
        """.desktop file position"""
        return Path(self.DESKTOP_FILES) / f'{self.NAME}.desktop'
    @property
    def profile_desktop_file_path(self):
        """.desktop file position"""
        return Path(self.DESKTOP_FILES) / f'{self.NAME}-profile.desktop'


class DefaultRoot(Default):
    """Default configuration setup"""

    USER = 'root'
    BINARIES_FOLDER = '/opt'
    DESKTOP_FILES = '/usr/share/applications'


class DefaultUser(DefaultRoot):
    """Install everything into user's path"""
    USER = ''
    BINARIES_FOLDER = '.local/bin'  # Prefixed by user's home
    DESKTOP_FILES = '.local/share/applications'  # Prefixed by user's home


_CONFIGURATION = None

def get_config():
    """Get configuration object"""
    return globals()['_CONFIGURATION']
