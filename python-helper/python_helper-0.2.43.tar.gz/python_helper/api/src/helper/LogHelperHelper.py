from python_helper.api.src.domain import Constant as c
from python_helper.api.src.service import LogHelper, SettingHelper, ObjectHelper, ReflectionHelper, StringHelper, EnvironmentHelper

NO_TRACEBACK_PRESENT = f'NoneType: None{c.NEW_LINE}'
NO_TRACEBACK_PRESENT_MESSAGE = 'Exception: '

FIRST_LAYER_COLOR = 'FIRST_LAYER_COLOR'
SECOND_LAYER_COLOR = 'SECOND_LAYER_COLOR'
LOG_TEXT = 'LOG_TEXT'

LEVEL_DICTIONARY = {
    LogHelper.LOG : {
        FIRST_LAYER_COLOR : c.BRIGHT_BLACK,
        SECOND_LAYER_COLOR: c.BRIGHT_BLACK,
        LOG_TEXT : c.LOG
    },
    LogHelper.SUCCESS : {
        FIRST_LAYER_COLOR : c.DARK_GREEN,
        SECOND_LAYER_COLOR: c.BRIGHT_GREEN,
        LOG_TEXT : c.SUCCESS
    },
    LogHelper.SETTING : {
        FIRST_LAYER_COLOR : c.DARK_BLUE,
        SECOND_LAYER_COLOR: c.BRIGHT_BLUE,
        LOG_TEXT : c.SETTING
    },
    LogHelper.DEBUG : {
        FIRST_LAYER_COLOR : c.DARK_CYAN,
        SECOND_LAYER_COLOR: c.BRIGHT_CYAN,
        LOG_TEXT : c.DEBUG
    },
    LogHelper.WARNING : {
        FIRST_LAYER_COLOR : c.DARK_YELLOW,
        SECOND_LAYER_COLOR: c.BRIGHT_YELLOW,
        LOG_TEXT : c.WARNING
    },
    LogHelper.WRAPPER : {
        FIRST_LAYER_COLOR : c.BRIGHT_WHITE,
        SECOND_LAYER_COLOR: c.DARK_WHITE,
        LOG_TEXT : c.WRAPPER
    },
    LogHelper.FAILURE : {
        FIRST_LAYER_COLOR : c.DARK_MAGENTA,
        SECOND_LAYER_COLOR: c.BRIGHT_MAGENTA,
        LOG_TEXT : c.FAILURE
    },
    LogHelper.ERROR : {
        FIRST_LAYER_COLOR : c.DARK_RED,
        SECOND_LAYER_COLOR: c.BRIGHT_RED,
        LOG_TEXT : c.ERROR
    },
    LogHelper.TEST : {
        FIRST_LAYER_COLOR : c.BRIGHT_BLACK,
        SECOND_LAYER_COLOR: c.BRIGHT_BLACK,
        LOG_TEXT : c.TEST
    }
}

def getStatus(level) :
    status = LogHelper.LOG_HELPER_SETTINGS.get(level)
    return status if isinstance(status, str) and StringHelper.isNotBlank(status) else c.TRUE

def getColors(level) :
    if SettingHelper.LOCAL_ENVIRONMENT == EnvironmentHelper.get(SettingHelper.ACTIVE_ENVIRONMENT) :
        firstLayerColor = LEVEL_DICTIONARY.get(level).get(FIRST_LAYER_COLOR) if LEVEL_DICTIONARY.get(level) and LEVEL_DICTIONARY.get(level).get(FIRST_LAYER_COLOR) else c.NOTHING
        secondLayerColor = LEVEL_DICTIONARY.get(level).get(SECOND_LAYER_COLOR) if LEVEL_DICTIONARY.get(level) and LEVEL_DICTIONARY.get(level).get(SECOND_LAYER_COLOR) else c.NOTHING
        tirdLayerColor = c.MUTTED_COLOR if c.MUTTED_COLOR else c.NOTHING
        resetColor = c.RESET_COLOR if c.RESET_COLOR else c.NOTHING
    else :
        firstLayerColor = c.NOTHING
        secondLayerColor = c.NOTHING
        tirdLayerColor = c.NOTHING
        resetColor = c.NOTHING
    return (firstLayerColor, secondLayerColor, tirdLayerColor, resetColor) if StringHelper.isNotBlank(firstLayerColor) else (c.NOTHING, c.NOTHING, c.NOTHING, c.NOTHING)

def softLog(origin, message, level, exception=None, newLine=False) :
    if ObjectHelper.isNotNone(exception) :
        hardLog(origin,message,exception,level)
    elif c.TRUE == getStatus(level) :
        firstLayerColor, secondLayerColor, tirdLayerColor, resetColor = getColors(level)
        LogHelper.logIt(StringHelper.join([firstLayerColor, LEVEL_DICTIONARY[level][LOG_TEXT], *getOriginPortion(origin, tirdLayerColor, resetColor), secondLayerColor, message, resetColor, getNewLine(newLine, exception=exception)]))
    elif not c.FALSE == getStatus(level) :
        levelStatusError(method, level)

def hardLog(origin, message, exception, level, newLine=False) :
    if c.TRUE == getStatus(level) :
        firstLayerColor, secondLayerColor, tirdLayerColor, resetColor = getColors(level)
        LogHelper.logIt(StringHelper.join([firstLayerColor, LEVEL_DICTIONARY[level][LOG_TEXT], *getOriginPortion(origin, tirdLayerColor, resetColor), secondLayerColor, message, *getErrorPortion(exception, firstLayerColor, secondLayerColor, tirdLayerColor, resetColor), resetColor, getNewLine(newLine, exception=exception)]))
    elif not c.FALSE == getStatus(level) :
        levelStatusError(method, level)

def printMessageLog(level, message, condition=False, newLine=True, margin=True, exception=None) :
    if condition :
        firstLayerColor, secondLayerColor, tirdLayerColor, resetColor = getColors(level)
        LogHelper.logIt(StringHelper.join([c.TAB if margin else c.NOTHING, firstLayerColor, LEVEL_DICTIONARY[level][LOG_TEXT], secondLayerColor, message, *getErrorPortion(exception, firstLayerColor, secondLayerColor, tirdLayerColor, resetColor), resetColor, getNewLine(newLine, exception=exception)]))

def getOriginPortion(origin, tirdLayerColor, resetColor) :
    if not origin or origin == c.NOTHING :
        return [c.NOTHING]
    else :
        moduleName = ReflectionHelper.getModuleName(origin)
        className = ReflectionHelper.getClassName(origin)
        moduleProtion = getLogThingName(moduleName)
        classPortion = getLogThingName(className)
        return [tirdLayerColor, *moduleProtion, *classPortion, ReflectionHelper.getName(origin), c.COLON_SPACE, resetColor]

def getLogThingName(thing) :
    return [] if thing in c.NATIVE_TYPES or (c.OPEN_TUPLE in thing and c.CLOSE_TUPLE in thing) else [thing, c.DOT]

def getErrorPortion(exception, firstLayerColor, secondLayerColor, tirdLayerColor, resetColor) :
    if ObjectHelper.isEmpty(exception) :
        return [c.NOTHING]
    eceptionMessage = LogHelper.getExceptionMessage(exception)
    traceBackMessage = LogHelper.getTracebackMessage()
    traceBackMessageSplited = LogHelper.getTracebackMessage().split(eceptionMessage)
    return [c.NEW_LINE, tirdLayerColor, *[t if t is not traceBackMessageSplited[-1] else t if t[-1] is not c.NEW_LINE else t[:-1] for t in traceBackMessageSplited if ObjectHelper.isNotNone(t)], secondLayerColor, eceptionMessage, resetColor]

def levelStatusError(method, level) :
    LogHelper.failure(method, f'"{level}" log level status is not properly defined: {getStatus(level)}', None)

def getNewLine(newLine, exception=None) :
    return c.NEW_LINE if (newLine and ObjectHelper.isNone(exception)) or (ObjectHelper.isNotNone(exception) and NO_TRACEBACK_PRESENT_MESSAGE == LogHelper.getTracebackMessage()) else c.NOTHING

# FORE_SIMPLE_RESET_COLOR = colorama.Fore.RESET
# LEVEL_DICTIONARY = {
#     SUCCESS : {
#         FIRST_LAYER_COLOR : colorama.Fore.GREEN,
#         SECOND_LAYER_COLOR: colorama.Fore.GREEN + colorama.Style.BRIGHT
#     },
#     SETTING : {
#         FIRST_LAYER_COLOR : colorama.Fore.BLUE,
#         SECOND_LAYER_COLOR: colorama.Fore.BLUE + colorama.Style.BRIGHT
#     },
#     DEBUG : {
#         FIRST_LAYER_COLOR : colorama.Fore.CYAN,
#         SECOND_LAYER_COLOR: colorama.Fore.CYAN + colorama.Style.BRIGHT
#     },
#     WARNING : {
#         FIRST_LAYER_COLOR : colorama.Fore.YELLOW,
#         SECOND_LAYER_COLOR: colorama.Fore.YELLOW + colorama.Style.BRIGHT
#     },
#     WRAPPER : {
#         FIRST_LAYER_COLOR : colorama.Fore.WHITE + colorama.Style.BRIGHT,
#         SECOND_LAYER_COLOR: colorama.Fore.WHITE
#     },
#     FAILURE : {
#         FIRST_LAYER_COLOR : colorama.Fore.MAGENTA,
#         SECOND_LAYER_COLOR: colorama.Fore.MAGENTA + colorama.Style.BRIGHT
#     },
#     ERROR : {
#         FIRST_LAYER_COLOR : colorama.Fore.RED,
#         SECOND_LAYER_COLOR: colorama.Fore.RED + colorama.Style.BRIGHT
#     }
# }

# def print_format_table():
#     """
#     prints table of formatted text format options
#     """
#     for style in range(8):
#         for fg in range(30,38):
#             s1 = ''
#             for bg in range(40,48):
#                 format = ';'.join([str(style), str(fg), str(bg)])
#                 s1 += '\x1b[%sm %s \x1b[0m' % (format, format)
#             print(s1)
#         print('\n')
#
# print_format_table()
#
# x = 0
# for i in range(24):
#   colors = ""
#   for j in range(5):
#     code = str(x+j)
#     colors = colors + "\33[" + code + "m\\33[" + code + "m\033[0m "
#   print(colors)
#   x=x+5
