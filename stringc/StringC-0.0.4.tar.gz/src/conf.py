from datetime import datetime
import os

def CountIt():
    i = 1
    while True:
        yield i
        i += 1

# Error Counter For OutPut Report:
ErrorCounter = CountIt()

# ProjectCode:
ProjectCode = "STC"
# Log File Path
LogFilePath = f"{os.getcwd()}/Logs/"
# Log File Name:
LogFileName = f"{ProjectCode}-{datetime.now().strftime('%Y-%m-%d')}"

# General Log Level:
GeneralLogLevel = "DEBUG"


