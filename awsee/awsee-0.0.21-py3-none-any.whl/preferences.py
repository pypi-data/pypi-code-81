import os
import configparser
from os.path import expanduser
from awsee.emoticons import Emoticons
from awsee.general import *

FILE_INI    = os.path.join(expanduser("~"),".awsee","awsee.ini")
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

            configFileIni.set(WINDOWS, "; WINDOWS Options for New Terminal Window")
            configFileIni.set(WINDOWS, ";   Leave it blanks to use the default options CMDER or CMD")
            configFileIni.set(WINDOWS, ";   To use Git-Bash, use option 1 or 2 pointing to your installation path")
            configFileIni.set(WINDOWS, ";   To use Windows Terminal, use option 3")
            configFileIni.set(WINDOWS, "; Option 0) terminal-command =")
            configFileIni.set(WINDOWS, "; Option 1) terminal-command = C:\\Developer\\Git\\apps\\Git\\bin\\sh.exe")
            configFileIni.set(WINDOWS, "; Option 2) terminal-command = C:\\Developer\\Git\\apps\\Git\\git-bash.exe")
            configFileIni.set(WINDOWS, "; Option 3) terminal-command = wt")
            configFileIni.set(WINDOWS, "terminal-command","")

            configFileIni.set(LINUX, "; LINUX Options for New Terminal Window")
            configFileIni.set(LINUX, ";   Leave it blanks to use the default option (Still to be worked, not ready!)")
            configFileIni.set(LINUX, ";   ---")
            configFileIni.set(LINUX, "; Option 0) terminal-command =")
            configFileIni.set(LINUX, "; Option 1) terminal-command = ")
            configFileIni.set(LINUX, "terminal-command","")

            with open(FILE_INI,'w') as configfile:
                configFileIni.write(configfile)
                configFileIni = configparser.ConfigParser(allow_no_value=True)
        
        configFileIni = configparser.ConfigParser()
        configFileIni.read(FILE_INI)
        self._defaultProfile   = configFileIni[GENERAL]["default-profile"]
        self._emoticonsEnabled = configFileIni[GENERAL]["emoticons-enabled"] in ['True','true']
        if "no-color" in configFileIni[GENERAL]:
           self._noColor       = configFileIni[GENERAL]["no-color"] in ['True','true'] 
        else:
           self._noColor       = False
        self._windows          = Windows(configFileIni[WINDOWS]["terminal-command"])
        self._linux            = Linux(configFileIni[LINUX]["terminal-command"])

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
