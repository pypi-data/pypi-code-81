import os
import configparser
from os.path import expanduser
from awsee.emoticons import Emoticons

USER_DIR    = expanduser("~") + "/.awsee/"
FILE_INI    = USER_DIR + "awsee.ini"
GENERAL     = "GENERAL"
WINDOWS     = "WINDOWS"
LINUX       = "LINUX"

class Preferences:

    @property
    def defaultProfile(self):
        return self._defaultProfile
    
    @property
    def emoticonsEnabled(self):
        return self._emoticonsEnabled
    
    @property
    def noColor(self):
        return self._noColor

    @property
    def windows(self):
        return self._windows

    @property
    def linux(self):
        return self._linux

    def __init__(self):
        if not os.path.exists(FILE_INI):
            configFileIni = configparser.ConfigParser(allow_no_value=True)
            configFileIni.add_section(GENERAL)
            configFileIni.add_section(WINDOWS)
            configFileIni.add_section(LINUX)
            configFileIni.set(GENERAL, "default-profile","default")
            configFileIni.set(GENERAL, "emoticons-enabled","true")
            configFileIni.set(GENERAL, "no-color","false")

            configFileIni.set(WINDOWS, "; For Git-Bash, use one of this options (pointing to your installation path)")
            configFileIni.set(WINDOWS, "; Option 1: terminal-command = C:\\Program Files\\Git\\apps\\Git\\bin\\sh.exe")
            configFileIni.set(WINDOWS, "; Option 2: terminal-command = C:\\Program Files\\Git\\apps\\Git\\git-bash.exe")
            configFileIni.set(WINDOWS, "terminal-command","")

            configFileIni.set(LINUX, "terminal-command","")

            with open(FILE_INI,'w') as configfile:
                configFileIni.write(configfile)
                configFileIni = configparser.ConfigParser(allow_no_value=True)
        
        configFileIni = configparser.ConfigParser()
        configFileIni.read(FILE_INI)
        self._defaultProfile   = configFileIni[GENERAL]["default-profile"]
        self._emoticonsEnabled = configFileIni[GENERAL]["emoticons-enabled"] in ['True','true']
        self._noColor          = configFileIni[GENERAL]["no-color"] in ['True','true'] 
        self._windows          = Windows(configFileIni[WINDOWS]["terminal-command"])
        self._linux            = Windows(configFileIni[LINUX]["terminal-command"])

        Emoticons.ENABLED = self._emoticonsEnabled

class Windows:

    @property
    def terminalCommand(self):
        return self._terminal_command

    def __init__(self, _terminal_command):
        self._terminal_command = _terminal_command

class Linux:

    @property
    def terminalCommand(self):
        return self._terminal_command

    def __init__(self, _terminal_command):
        self._terminal_command = _terminal_command
