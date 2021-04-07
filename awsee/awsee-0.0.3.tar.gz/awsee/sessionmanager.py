import os
from os.path import expanduser
import datetime
from awsee.logmanager import LogManager
from awsee.preferences import Preferences
from awsee.functions import Functions
from arnparse import arnparse
from awsee.awsservices import AwsServices
from awsee.messages import Messages
from awsee.style import Style
from awsee.emoticons import Emoticons
from awsee.utils import Utils
from tinydb import Query, where
from shutil import which
from awsee.repository import Repository, CredentialsRepository, ConfigRepository, RoleRepository, MfaRepository

class SessionManager:

    SCRIPTS_PREFIX_NAME_FILE = "set-awssession-"

    def __init__(self):
        self.credentialsRepository = CredentialsRepository()
        self.roleRepository        = RoleRepository()
        self.mfaRepository         = MfaRepository()
        self.preferences           = Preferences()

    # Start a Session and immediatly Assume a Role 
    def startCredentialsOwnerSessionWithMFA(self, mfaToken, profile, mfa):
        # TODO:
        pass 

    # Assume a Role
    def assumeRole(self, role, profile=None, mfaToken=None):
        aws = AwsServices()

        stsToken = aws.assumeRole(role['role-arn'], profile, mfaToken)
        if not stsToken:
            return None, None, None
        
        return self.createAWSSessionOnTerminalUser(stsToken["Credentials"], role['profile'], role['role-name'])
    
    # Open Session using MFA (default or other profile)
    def startAWSSession(self, profile):
        aws = AwsServices()

        stsToken = {}
        stsToken["AccessKeyId"]     = profile['accessKey']
        stsToken["SecretAccessKey"] = profile['secretKey']
        stsToken["SessionToken"]    = None
        stsToken["Expiration"]      = datetime.datetime.now() + datetime.timedelta(minutes=525600)

        return self.createAWSSessionOnTerminalUser(stsToken, profile['profile'], None)

    # Open Session (other profile - no need MFA)
    def startAWSSessionWithMFA(self, profile, mfa, mfaToken, role=None):
        aws = AwsServices()

        stsToken = aws.getSessionToken(mfaSerial=mfa['mfa-device'],mfaToken=mfaToken, profile=profile['profile'])
        if not stsToken:
            return None, None, None

        roleName = None
        if role:
           # If a Role was also passed, 
           # Initiate a session the the Profile given, and using it, immediately, create a Session with the Role passed
           roleName =  role['role-name']
           stsToken = aws.startSessionWithTokenAndAssumeRole(stsToken,role['role-arn'])

        return self.createAWSSessionOnTerminalUser(stsToken["Credentials"], profile['profile'], roleName)

    def createAWSSessionOnTerminalUser(self, stsToken, profile, role):
        accessKey      = stsToken["AccessKeyId"]
        secretKey      = stsToken["SecretAccessKey"]
        sessionToken   = stsToken["SessionToken"]
        expiration     = stsToken["Expiration"]
        output         = None
        scriptFileWin  = None
        scriptFileBash = None

        role            = "" if not role else "_" + role.replace(" ","_").lower()
        nameProfile     = profile.replace(" ","_")
        roleTitle       = "" if role == "" else f"Role: {role.replace('_','')}" 
        windowTitle     = f"AWSEE Profile: {nameProfile}  {roleTitle}"

        if Utils.isWindows():
            
            scriptFileWin   = f"{self.SCRIPTS_PREFIX_NAME_FILE}{nameProfile}{role}.bat"
            scriptFileBash  = f"{self.SCRIPTS_PREFIX_NAME_FILE}{nameProfile}{role}.sh"

            terminalCommand = self.preferences.windows.terminalCommand
            # Check if there's a Terminal Commmand Set
            if not terminalCommand or terminalCommand.lstrip().rstrip() == "":
                # Check CMDER is installed (then use it)
                if which("cmder") and os.environ['CMDER_ROOT'] != "":
                    outputWin, environmentsWin = self.createEnvironment(False, scriptFileWin, accessKey, secretKey, sessionToken, expiration, role.replace('_',''))
                    output = outputWin
                    os.system(f"start %CMDER_ROOT%\\vendor\\conemu-maximus5\\ConEmu.exe /icon \"%CMDER_ROOT%\\cmder.exe\" /title \"{windowTitle}\" /loadcfgfile \"%CMDER_ROOT%\\config\\ConEmu.xml\" /cmd cmd /k " + environmentsWin)
                    #os.system(f"start %CMDER_ROOT%\\vendor\\conemu-maximus5\\ConEmu.exe /icon \"%CMDER_ROOT%\\cmder.exe\" /title \"{windowTitle}\" /cmd cmd /k " + environmentsWin)
                else:
                    # Last option (windows default cmd)
                    if which("cmd"):
                        outputWin, environmentsWin = self.createEnvironment(False, scriptFileWin, accessKey, secretKey, sessionToken, expiration, role.replace('_',''))
                        output = outputWin
                        os.system("start cmd.exe /c cmd /k" + environmentsWin)
                    else:
                        msg = f"""\n{Style.GREEN}    Please set a {Style.IBLUE}terminal-command{Style.GREEN} at your {Style.IBLUE}~/.awsee/awsee.ini{Style.GREEN}, WINDOWS section in order \n    to open a Terminal ready to use with your AWS Session Token configured.
                        \n    Example: \n    {Style.IBLUE}[WINDOWS]\n    terminal-command = {Style.IGREEN}d:\Program Files\Git\git-bash.exe{Style.RESET}
                        """
                        Messages.showError("No Terminal Found (CMDER or CMD)",msg)
                        return None, None
            else:
                if "git-bash.exe" in terminalCommand or "sh.exe" in terminalCommand:
                    outputBash, environmentsBash = self.createEnvironment(True, scriptFileBash, accessKey, secretKey, sessionToken, expiration, role.replace('_',''))
                    output = outputBash

                    # Regarding the place where Python is running (not the Target Console to Open, configured at awsee.ini)...  
                    # Check if the Call to open a Shell Script Terminal were made inside a GitBash, if not... change to Windows Style (the Output Python window)
                    if not Utils.isRunningOnGitBash():
                        outputWin, _ = self.createEnvironment(False, scriptFileWin, accessKey, secretKey, sessionToken, expiration, role.replace('_',''))
                        output = outputWin

                if "git-bash.exe" in terminalCommand:
                    os.system(f"start {terminalCommand} --needs-console --no-hide --command=usr\\bin\\bash.exe --login -i -c \"sh -c 'source ./{environmentsBash}; exec sh'\"")
                elif "sh.exe" in terminalCommand:
                    os.system(f"start {terminalCommand} --login -i -l -c \"sh -c 'source ./{environmentsBash}; exec sh'\"")
                else:
                    msg = f"""\n{Style.GREEN}    Please check the {Style.IBLUE}terminal-command{Style.GREEN} set at your {Style.IBLUE}~/.awsee/awsee.ini{Style.GREEN}, WINDOWS section in order \n    to open a Terminal ready to use with your AWS Session Token configured.
                    \n    Example: \n    {Style.IBLUE}[WINDOWS]\n    terminal-command = {Style.IGREEN}d:\Program Files\Git\sh.exe{Style.RESET}
                    """
                    Messages.showError(f"Terminal Command set \"{terminalCommand}\" not supported (Use git-bash.exe, sh.exe or let it blank, for system default",msg)
                    return None, None
        else:
            # LINUX
            # TODO:
              print("export AWS_ACCESS_KEY")

        return output, scriptFileWin, scriptFileBash

    # Script to Help clean environment variables, etc. 
    def createCleanEnvironmentScript(self, scriptFile):
        if ".bat" in scriptFile:
            cleanFileName = "clean.bat"
            content = f"""@ECHO OFF
set AWS_ACCESS_KEY_ID=
set AWS_SECRET_ACCESS_KEY=
set AWS_SESSION_TOKEN=
set AWS_EXPIRATION=
set AWS_SEE=CLOSED
DEL {self.SCRIPTS_PREFIX_NAME_FILE}*
            """
        else:
            cleanFileName = "clean.sh"
            content = f"""unset AWS_ACCESS_KEY_ID
unset AWS_SECRET_ACCESS_KEY
unset AWS_SESSION_TOKEN
unset AWS_EXPIRATION
set AWS_SEE=CLOSED
rm {self.SCRIPTS_PREFIX_NAME_FILE}*
            """
        with open(f"{cleanFileName}",'w') as fout:
            fout.write(content)

    # Create Contents, Script File for Environments Variables and Clipboard (Win and Bash)
    def createEnvironment(self, isBashEnv, scriptFile, accessKey, secretKey, sessionToken, expiration, roleTitle=None):
        output           = self.createOutputStartSession(isBashEnv, scriptFile, accessKey, secretKey, sessionToken, expiration, roleTitle)
        initFileContent  = self.createContentScriptFileStartSession(isBashEnv, accessKey, secretKey, sessionToken, expiration, roleTitle)
        with open(f"{scriptFile}",'w') as fout:
            fout.write(initFileContent)
        environments = f"\"{scriptFile}\""
        self.addEnvironmentVariablesConfigurationToClipboard(isBashEnv,accessKey, secretKey, sessionToken, expiration, roleTitle)
        self.createCleanEnvironmentScript(scriptFile)
        return output, environments

    def createOutputStartSession(self, forBash, scriptFile, accessKey, secretKey, sessionToken, expiration, roleTitle=None):
        commandEnvSet = "set"
        executeScript = f"{scriptFile}"
        if forBash:
            commandEnvSet = "export"
            executeScript = f"source ./{scriptFile}"

        awsToken = f"{Style.GREEN}{commandEnvSet} AWS_SESSION_TOKEN{Style.WHITE}={Style.IBLUE}{sessionToken}\r" if sessionToken else ""
        awsRole  = f"{Style.GREEN}{commandEnvSet} AWS_ROLE{Style.WHITE}={Style.IBLUE}{roleTitle}\r" if roleTitle else ""

        output  = "\n"
        output += f" {Style.GREEN}======================="
        output += f"\n {Style.IMAGENTA}  >>> AWS SESSION <<<\n"
        output += f" {Style.GREEN}======================="
        output += f"""\n {Style.GREEN}set AWS_ACCESS_KEY_ID{Style.WHITE}={Style.IBLUE}{accessKey}
 {Style.GREEN}{commandEnvSet} AWS_SECRET_ACCESS_KEY{Style.WHITE}={Style.IBLUE}{secretKey}
 {awsToken}
 {Style.GREEN}{commandEnvSet} AWS_EXPIRATION{Style.WHITE}={Style.IBLUE}{expiration}
 {awsRole}

 {Style.IMAGENTA}  >>> Opening in another window...

 {Style.GREEN}or...
 {Style.GREEN}To setup this AWS Session at this same Window
 Hit [Shift + Insert] or execute the script:

 {Style.IBLUE}  >>> {executeScript}{Style.RESET}
        """
        return output

    def addEnvironmentVariablesConfigurationToClipboard(self, forBash, accessKey, secretKey, sessionToken, expiration, roleTitle=None):
        command = "set" if not forBash else "export"
        awsToken = f"{Style.GREEN}{command} AWS_SESSION_TOKEN{Style.WHITE}={Style.IBLUE}{sessionToken}\r" if sessionToken else ""
        # Add to Clipboard (SETs environmentsWin)
        forClipboard  = f"{command} AWS_ACCESS_KEY_ID={accessKey}\r\n"
        forClipboard += f"{command} AWS_SECRET_ACCESS_KEY={secretKey}\r\n"
        forClipboard += f"{awsToken}\r\n"
        forClipboard += f"{command} AWS_SEE=gG99USedshwRIVSe\r\n"
        if forBash:
           forClipboard += f"{command} AWS_EXPIRATION=\"{expiration}\"\r\n"
        else:
           forClipboard += f"{command} AWS_EXPIRATION={expiration}\r\n" 
        Utils.addToClipboard(forClipboard)

    def createContentScriptFileStartSession(self, forBash, accessKey, secretKey, sessionToken, expiration, roleTitle=None):
        initFileContent = self.createBashScriptFile(accessKey, secretKey, sessionToken, expiration, roleTitle) if forBash else \
                          self.createCMDscriptFile(accessKey, secretKey, sessionToken, expiration, roleTitle)
        return initFileContent

    def createCMDscriptFile(self, accessKey, secretKey, sessionToken, expiration, roleTitle=None):
        awsToken = f"set AWS_SESSION_TOKEN={sessionToken}" if sessionToken else ""
        roleEcho = f"ECHO.Role.........: {roleTitle}" if roleTitle else ""
        roleSet  = f"{roleTitle}" if roleTitle else " " 

        return f"""
        @ECHO OFF
        ECHO.#awsee
        ECHO.=============================
        ECHO.  AWSCLI Session Configured
        ECHO.=============================
        set AWS_ACCESS_KEY_ID={accessKey}
        set AWS_SECRET_ACCESS_KEY={secretKey}
        {awsToken}
        set AWS_EXPIRATION={expiration}

        for /F "delims=" %%i in ('aws sts get-caller-identity') do (
            SET "string=%%i"
            echo %%i | findstr /C:"Account">nul && (
                SET ACCOUNT=%%i
            )
            echo %%i | findstr /C:"Arn">nul && (
                SET USERARN=%%i
            )
        )
        set ACCOUNT=%ACCOUNT:Account=%
        set ACCOUNT=%ACCOUNT::=%
        set ACCOUNT=%ACCOUNT:"=%
        set ACCOUNT=%ACCOUNT:,=%
        set ACCOUNT=%ACCOUNT: =%

        set USERARN=%USERARN: =%
        set USERARN=%USERARN:~7%
        set USERARN=%USERARN:"=%
        REM set USERARN=%USERARN:Arn=%
        REM set USERARN=%USERARN:,=%
        

        set AWS_ACCOUNT=%ACCOUNT%
        set AWS_USER=%USERARN%
        set AWS_ROLE={roleSet}
        set AWS_SEE=gG99USedshwRIVSe

        REM Shortcuts
        DOSKEY ls=dir /W
        DOSKEY w=ECHO. ^&^& ECHO.#awsee ^&^& ECHO.============================= ^&^& ECHO.       MY AWS SESSION ^&^& ECHO.============================= ^&^& ECHO.Account...........:%ACCOUNT% ^&^& ECHO.User..............:%USERARN% ^&^& ECHO.Access Key........:%AWS_ACCESS_KEY_ID% ^&^& ECHO.Secret Key........:%AWS_SECRET_ACCESS_KEY% ^&^& ECHO.Expiration........:%AWS_EXPIRATION% ^&^& ECHO.Role..............:%AWS_ROLE%

        ECHO.Expires at...: {expiration:%Y-%m-%d %H:%M}
        ECHO.Account......: %ACCOUNT%
        ECHO.User.........: %USERARN%
        {roleEcho} 
        ECHO.
        """

    def createBashScriptFile(self, accessKey, secretKey, sessionToken, expiration, roleTitle=None):
        awsToken = f"export AWS_SESSION_TOKEN={sessionToken}" if sessionToken else ""
        roleEcho = f"echo Role.........: {roleTitle}" if roleTitle else " "
        roleSet  = f"{roleTitle}" if roleTitle else " " 
        
        return f"""
        #!/bin/sh
        echo 
        echo =============================
        echo   AWSCLI Session Configured
        echo =============================
        export AWS_ACCESS_KEY_ID={accessKey}
        export AWS_SECRET_ACCESS_KEY={secretKey}
        {awsToken}
        export AWS_EXPIRATION="{expiration}"

        vlr="$(aws sts get-caller-identity)"
        account=$(echo "$vlr" | grep '"Account"' | sed s/\\"//g | sed s/,//g | sed s/"Account:"//g)
        arn=$(echo "$vlr" | grep '"Arn"' | sed s/\\"//g | sed s/,//g | sed s/"Arn:"//g )

        export AWS_ACCOUNT=$account
        export AWS_USER=$arn
        export AWS_ROLE={roleSet}
        export AWS_SEE=gG99USedshwRIVSe

        echo Expires at...: "{expiration}"
        echo Account......: $account
        echo User.........: $arn
        {roleEcho}
        echo
        """
        