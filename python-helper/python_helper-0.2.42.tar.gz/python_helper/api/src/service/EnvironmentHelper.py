import os, sys, json
from python_helper.api.src.service import StringHelper, LogHelper, ObjectHelper, SettingHelper
from python_helper.api.src.domain import Constant as c

OS = os
SYS = sys
OS_SEPARATOR = OS.path.sep

LINUX_OS_NAME = 'linux'
WINDOWS_OS_NAME = 'win32'

clear = lambda: OS.system('cls')

def get(environmentKey, default=None) :
    environmentValue = default if ObjectHelper.isNone(environmentKey) else OS.environ.get(environmentKey)
    return environmentValue if ObjectHelper.isNotNone(environmentValue) else default

def update(environmentKey, environmentValue, default=None) :
    if ObjectHelper.isNotEmpty(environmentKey) :
        associatedValue = None
        if not environmentValue is None :
            associatedValue = str(StringHelper.filterString(environmentValue))
            OS.environ[environmentKey] = associatedValue
        elif not default is None :
            associatedValue = str(StringHelper.filterString(default))
            OS.environ[environmentKey] = associatedValue
        else :
            try:
                delete(environmentKey)
            except Exception as exception :
                LogHelper.warning(update, f'Failed to delete "{environmentKey}" enviroment variable key', exception=exception)
        return associatedValue
    else :
        LogHelper.debug(update, f'arguments: environmentKey: {environmentKey}, environmentValue: {environmentValue}, default: {default}')
        raise Exception(f'Error associating environment variable "{environmentKey}" key to environment variable "{environmentValue}" value')

def switch(environmentKey, environmentValue, default=None) :
    originalEnvironmentValue = get(environmentKey, default=default)
    update(environmentKey, environmentValue, default=default)
    return originalEnvironmentValue

def reset(environmentVariables, originalEnvironmentVariables) :
    if environmentVariables :
        for key in environmentVariables.keys() :
            if key in originalEnvironmentVariables :
                update(key, originalEnvironmentVariables[key])

def delete(environmentKey) :
    if ObjectHelper.isNotNone(environmentKey) :
        OS.environ.pop(environmentKey)

def getSet(avoidRecursiveCall=False) :
    try :
        return json.loads(str(OS.environ)[8:-1].replace(c.DOUBLE_QUOTE, c.BACK_SLASH_DOUBLE_QUOTE).replace(c.SINGLE_QUOTE, c.DOUBLE_QUOTE))
    except Exception as exception :
        LogHelper.error(getSet, 'Not possible to load os.environ as a json. Returning os.environ as string by default', exception)
        return str(OS.environ)[8:-1]

def listDirectoryContent(path) :
    return OS.listdir(path)

def appendPath(path) :
    SYS.path.append(path)

def getCurrentSoutStatus(avoidRecursiveCall=False) :
    return SYS.stdout, SYS.stderr

def overrideSoutStatus(stdout, stderr) :
    SYS.stdout = stdout
    SYS.stderr = stderr

def isLinux() :
    return SYS.platform == LINUX_OS_NAME

def isWindows() :
    return SYS.platform == WINDOWS_OS_NAME
