# coding=utf-8
#
# Author: Ualter Otoni Pereira
# ualter.junior@gmail.com
#
import os
import logging
import sys
import re
import atexit 
from os.path import expanduser
import signal
import datetime
from datetime import timezone

from shutil import which
from tinydb import Query, where
from arnparse import arnparse
from awsee.messages import Messages
from awsee.style import Style
from awsee.emoticons import Emoticons
from awsee.utils import Utils
from awsee.tableargs import TableArgs
from awsee.prettytable import PrettyTable
from awsee.awsservices import AwsServices
from awsee.logmanager import LogManager
from awsee.preferences import Preferences
from awsee.functions import Functions
from awsee.rolemanager import RoleManager
from awsee.mfamanager import MFAManager
from awsee.repository import Repository, CredentialsRepository, ConfigRepository, RoleRepository, MfaRepository
from awsee.windowsenv import WindowsEnv
from awsee.sessionmanager import SessionManager
from awsee.profilemanager import ProfileManager

LOG = logging.getLogger("app." + __name__)
LOG.setLevel(logging.DEBUG)
FILE_LOG = expanduser("~") + "/.awsee/" + "log"

signal.signal(signal.SIGINT, signal.SIG_DFL)

class AwsSeePy:
    def __init__(self):
        myhomeFolder = expanduser("~") + "/.awsee/"
        if not os.path.exists(myhomeFolder):
           os.makedirs(myhomeFolder)

        self.mfaToken = None

        #LogManager().LOG.info("Starting...")
        self.credentialsRepository = CredentialsRepository()
        self.configRepository      = ConfigRepository()
        self.roleRepository        = RoleRepository()
        self.mfaRepository         = MfaRepository()
        self.preferences           = Preferences()
        self.executeFunction       = None
    
    def loadConfigProfiles(self):
        fileConfig  = expanduser("~") + "/.aws/config"

        if not os.path.exists(fileConfig):
            LogManager().LOG.warning("No file {} was found".format(fileConfig))
            return None
       
        configProfiles           = {}
        configProfiles["config"] = []
        currentProfileName = None 
        keys               = {}
        with open(fileConfig,'r') as fcfg:
            for line in fcfg.readlines():
                line = line.lstrip().rstrip()
                if line.lstrip().rstrip().startswith("["):
                   if currentProfileName:
                       configProfiles["config"].append({
                           "profile": currentProfileName,
                           "configurations": keys
                       })
                       keys = {}
                   # Read Current    
                   currentProfileName = Utils.cleanBreakLines(line).replace("[","").replace("]","")     
                else:
                   if Utils.cleanBreakLines(line).lstrip().rstrip() != "":
                      line = Utils.cleanBreakLines(re.sub('\s',"",line))
                      kv   = line.split("=")
                      keys[kv[0]] = kv[1]
            if currentProfileName:
               configProfiles["config"].append({
                   "profile": currentProfileName,
                   "configurations": keys
               })

        # Check if needs updates/inserts
        for c in configProfiles["config"]:
            dbRecordProfile = self.configRepository.findByProfile(c["profile"])
            # Insert the new one
            if not dbRecordProfile:
                self.configRepository.insert(c)
            else:
                # Update if needed
                update = False
                for config in c["configurations"]:
                    if config not in dbRecordProfile or \
                       c["configurations"][config] != dbRecordProfile["configurations"][config]:
                       update = True
                if update:
                   self.configRepository.update(c, c["profile"])

    def loadProfiles(self):
        fileCredentials = expanduser("~") + "/.aws/credentials"

        if not os.path.exists(fileCredentials):
            LogManager().LOG.warning("No file {} was found".format(fileCredentials))
            Messages.showWarning("Credentials Not Found!",f" The file {Style.IBLUE}/.aws/credentials{Style.GREEN} was not found, did you install and configure your {Style.IBLUE}awscli{Style.GREEN}?")
            sys.exit()

        currentProfileName                   = None
        accessKey                            = None
        secretKey                            = None
        credentialsProfiles                  = {}
        credentialsProfiles["credentials"]   = []
        with open(fileCredentials,'r') as fcred:
            for line in fcred.readlines():
                if line.lstrip().rstrip().startswith("["):
                   if currentProfileName:
                       defaultProfile = False
                       if currentProfileName == self.preferences.defaultProfile:
                           defaultProfile = True
                       # SAVE Previous
                       credentialsProfiles["credentials"].append({
                           "profile": currentProfileName,
                           "accessKey": accessKey,
                           "secretKey": secretKey,
                           "default": defaultProfile
                       })
                   # Read Current    
                   currentProfileName = Utils.cleanBreakLines(line).replace("[","").replace("]","") 
                else:
                   if Utils.cleanBreakLines(line).lstrip().rstrip() != "":
                      line = Utils.cleanBreakLines(re.sub('\s',"",line))
                      kv   = line.split("=")
                      if   "aws_access_key_id" in kv[0].lower():
                         accessKey = kv[1]
                      elif "aws_secret_access_key" in kv[0].lower():
                         secretKey = kv[1]
            if currentProfileName:
                defaultProfile = False
                if currentProfileName == self.preferences.defaultProfile:
                    defaultProfile = True
                # SAVE Previous
                credentialsProfiles["credentials"].append({
                    "profile": currentProfileName,
                    "accessKey": accessKey,
                    "secretKey": secretKey,
                    "default": defaultProfile
                })            

        # Check if needs updates/inserts
        awsServices = AwsServices()
        for c in credentialsProfiles["credentials"]:
            dbRecordProfile = self.credentialsRepository.findByProfile(c["profile"])
            # Insert the new one
            if not dbRecordProfile:
                account   = ""
                # Read Account and MFA Devices of the Profile at AWS
                try:
                    account = awsServices.getAccountOwner(c["profile"])["Account"]
                    for m in awsServices.getMFADevices(c["profile"])["MFADevices"]:
                        mfaRecord = self.mfaRepository.searchByQuery(Query().mfaDevice == m["SerialNumber"])
                        if not mfaRecord or len(mfaRecord) < 0:
                            self.mfaRepository.insert({
                                "profile": c["profile"],
                                "mfa-device": m["SerialNumber"],
                                "user-name": m["UserName"]
                            })
                except:
                    LogManager().LOG.warning(f"Not able to retrieve the MFA Devices for the {c['profile']}, probably some police might be blocking by the lack of MFA Token")
                c["account"] = account
                self.credentialsRepository.insert(c)
            else:
                # Check if needs to update the record (credentials change)
                if dbRecordProfile["accessKey"] != c["accessKey"]  or \
                   dbRecordProfile["secretKey"] != c["secretKey"]  or \
                   dbRecordProfile["default"]   != c["default"]:
                   # UPDATEIT
                   self.credentialsRepository.update(c, c["profile"])
                   
                # Try to Update its MFA Devices 
                # Removed to avoid remote connect all the time when the command --list is called
                #  TODO: Check to create a new function later, like --update-mfa-devices to explicitly update 
                #  the local credentials with MFA Devices remotely (if not blocked by polices)
                refreshMFA = False
                if refreshMFA:
                    try:
                        for m in awsServices.getMFADevices(c["profile"])["MFADevices"]:
                            mfaRecord = self.mfaRepository.searchByQuery(where('mfa-device') == m["SerialNumber"])
                            # Add a new MFA Device found at his/her Account (not in the MFA Device Repository yet)
                            if not mfaRecord or len(mfaRecord) < 0:
                                self.mfaRepository.insert({
                                    "profile": c["profile"],
                                    "mfa-device": m["SerialNumber"],
                                    "user-name": m["UserName"]
                                })
                    except:
                        pass

    def synchronize(self):
        print("")
        Messages.showStartExecution("Wait, synchronizing...")
        self.credentialsRepository.purge()
        self.configRepository.purge()
        self.loadProfiles()
        self.loadConfigProfiles()
        Messages.showStartExecution("Synchronization done!             ")
        print("")
    
    def listProfiles(self, more):
        profileManager = ProfileManager()
        profileManager.listProfiles(more)

    def addRole(self):
        roleManager = RoleManager()
        roleManager.addRole()

    def listRoles(self, filterByProfile):
        roleManager = RoleManager()
        roleManager.listRoles(filterByProfile)

    def removeRole(self, numberInList, roleName):
        roleManager = RoleManager()
        roleManager.removeRole(numberInList, roleName)
    
    def addMFADevice(self):
        mfaManager = MFAManager()
        mfaManager.addMfa()

    def listMFADevices(self, filterByProfile):
        mfaManager = MFAManager()
        mfaManager.listmfaDevices(filterByProfile)

    def removeRole(self, numberInList):
        mfaManager = MFAManager()
        mfaManager.removeRole(numberInList)

    def assumeRole(self, assumeRoleName, nameProfile=None, mfaToken=None, ):
        roleRecords = self.roleRepository.searchByQuery(where('role-name') == assumeRoleName)
        if not roleRecords or len(roleRecords) < 1:
           Messages.showWarning("Role not found!",f"     Role with the name {Style.IBLUE}{assumeRoleName}{Style.GREEN} was not found")
           sys.exit()

        role           = roleRecords[0]
        sessionManager = SessionManager()
        output, scriptFileWin, scriptFileBash = sessionManager.assumeRole(role, nameProfile, mfaToken)
        if output:
           output = Utils.removeCharsColors(output) if self.preferences.noColor else output
           print(output)

    def startAWSSessionWithMFAToken(self, nameProfile=None, mfaToken=None, assumeRole=None):
        if not nameProfile:
           # If not informed, use the Default Profile
           profiles = self.credentialsRepository.searchByQuery(where('default') == True)
           if not profiles or len(profiles) < 1:
               Messages.showWarning("Default profile not defined!")
               sys.exit()
           profile = profiles[0]
        else:
            # Get the Profile using the name informed
            profile = self.credentialsRepository.findByProfile(nameProfile)
            if not profile:
               Messages.showWarning(f"Profile {Style.IBLUE}{nameProfile}{Style.GREEN} not defined!")
               sys.exit()

        mfa = self.mfaRepository.findByProfile(profile['profile'])
        if not mfa:
           Messages.showWarning(f"MFA for the profile {profile['profile']} not found!")
           sys.exit()

        role = None
        if assumeRole:
            roles = self.roleRepository.searchByQuery(where('role-name') == assumeRole)
            if not roles or len(roles) < 1:
               Messages.showWarning(f"Role {assumeRole} not found!")
               sys.exit()
            role = roles[0]

        sessionManager = SessionManager()
        output, scriptFileWin, scriptFileBash = sessionManager.startAWSSessionWithMFA(profile, mfa, mfaToken, role)
        if output:
           output = Utils.removeCharsColors(output) if self.preferences.noColor else output
           print(output)
    
    def startAWSSession(self, nameProfile):
        profile = self.credentialsRepository.findByProfile(nameProfile)
        if not profile:
           Messages.showWarning(f"Profile {Style.IBLUE}{nameProfile}{Style.GREEN} not defined!")
           sys.exit()
        
        sessionManager = SessionManager()
        output, scriptFileWin, scriptFileBash = sessionManager.startAWSSession(profile)
        if output:
           output = Utils.removeCharsColors(output) if self.preferences.noColor else output
           print(output)
        

    def syntax(self, short=False):
        print("")
        functions = Functions()
        functions.showUsage(short)
        functions.showFunctions(short)
    
    def showInfo(self):
        sessionFound = False
        try:
            if os.environ['AWS_SEE']:
                if os.environ['AWS_SEE'] == "CLOSED":
                    Messages.showWarning("The AWSee Session was closed already!")
                    sys.exit()
                sessionFound = True
                account    = os.environ['AWS_ACCOUNT']
                user       = os.environ['AWS_USER']
                accessKey  = os.environ['AWS_ACCESS_KEY_ID']
                secretKey  = os.environ['AWS_SECRET_ACCESS_KEY']
                expiration = os.environ['AWS_EXPIRATION']
                role       = os.environ['AWS_ROLE']

                expDate = datetime.datetime.strptime(expiration,"%Y-%m-%d %H:%M:%S%z")
                diff    = (expDate - datetime.datetime.now(timezone.utc)).seconds / 60

                output = f"""\n{Style.IMAGENTA}#awsee{Style.GREEN}
=============================
     {Style.IMAGENTA}My AWSee Session{Style.GREEN}
=============================
{Style.GREEN}Account...........: {Style.IBLUE}{account}
{Style.GREEN}User..............: {Style.IBLUE}{user}
{Style.GREEN}Access Key........: {Style.IBLUE}{accessKey}
{Style.GREEN}Secret Key........: {Style.IBLUE}{secretKey}
{Style.GREEN}Expiration........: {Style.IBLUE}{expiration} ({Style.YELLOW}{diff:02.0f} {Style.IBLUE}minutes remaining)
{Style.GREEN}Role..............: {Style.IBLUE}{role}
                """
                output = Utils.removeCharsColors(output) if self.preferences.noColor else output
                print( output )
        except KeyError as e:
            LogManager().LOG.warning("KeyError while trying to read Environment variables")
            LogManager().LOG.warning("KeyError: " + str(e))
            sessionFound = False
        if not sessionFound:
            Messages.showWarning("No AWSee Session was started in this terminal!")
    
    def start(self):
        #executeFunction = False
        args = sys.argv
        if len(args) < 2:
           self.syntax()
           sys.exit()

        functions = Functions()
        if "-h" in args or "--help" in args:
            short = True if "-h" in args else False
            if len(args) > 2:
               f = functions.getFunctionByArgumentIdentifier(args[2])
               output = functions.showFunction(f)
               output = Utils.removeCharsColors(output) if self.preferences.noColor else output
               print(output)
            else:
               self.syntax(short)
            sys.exit()
        
        self.loadProfiles()
        self.loadConfigProfiles()

        args                 = args[1:]                          # Discard the first argument (our python function name)
        self.executeFunction = self.parseArgsFindFunction(args)  # Identify which function by the arguments/identifiers (-l --list, etc.)

        if  functions.INFO == self.executeFunction:
            self.showInfo()
        
        elif  functions.LIST_PROFILES == self.executeFunction:
            more = True if "full" in args or "-lf" in args else False
            self.listProfiles(more)

        elif functions.SYNC == self.executeFunction:
            self.synchronize()

        elif functions.ADD_ROLE == self.executeFunction:
            self.addRole()

        elif functions.LIST_ROLES == self.executeFunction:
            filterByProfile = None
            if len(args) > 1:
               filterByProfile = args[1]
            self.listRoles(filterByProfile)

        elif functions.REMOVE_ROLE == self.executeFunction:
            numberInList = -1
            roleName     = None
            if len(args) > 1:
               if Utils.isNumber(args[1]):
                   numberInList = int(args[1])
               else:
                   roleName = args[1]
            else:
                Messages.showWarning("Missing parameter! At least one of them must be informed:")
                output = Functions().showFunction(Functions.REMOVE_ROLE)
                output = Utils.removeCharsColors(output) if self.preferences.noColor else output
                print(output)
                sys.exit()
            self.removeRole(numberInList, roleName)

        elif functions.ADD_MFA == self.executeFunction:
             self.addMFADevice()

        elif functions.LIST_MFAS == self.executeFunction:
             filterByProfile = None
             if len(args) > 1:
                filterByProfile = args[1]
             self.listMFADevices(filterByProfile)

        elif functions.REMOVE_MFA == self.executeFunction:
            numberInList = -1
            if len(args) > 1:
               if Utils.isNumber(args[1]):
                   numberInList = int(args[1])
            else:
                Messages.showWarning("Missing parameter for Remove MFA...")
                output = Functions().showFunction(Functions.REMOVE_MFA)
                output = Utils.removeCharsColors(output) if self.preferences.noColor else output
                print(output)
                sys.exit()
            self.removeMFADevice(numberInList)

        elif functions.ASSUME_ROLE == self.executeFunction:
            if len(args) > 1:
               role = args[1]
               self.assumeRole(role,None,None)
            else:
               Messages.showWarning("Missing [ROLE] parameter...")
               output = Functions().showFunction(Functions.ASSUME_ROLE)
               output = Utils.removeCharsColors(output) if self.preferences.noColor else output
               print(output)
               sys.exit()

        elif functions.START_SESSION == self.executeFunction:
            if len(args) > 1:
                profile = args[1]
                self.startAWSSession(nameProfile=profile)
            else:
                Messages.showWarning("Missing [PROFILE] parameter...")
                output = Functions().showFunction(Functions.START_SESSION)
                output = Utils.removeCharsColors(output) if self.preferences.noColor else output
                print(output)
                sys.exit()

        elif functions.START_SESSION_MFA_TOKEN == self.executeFunction:
            # Parameters Already validated (if exists)
            mfaToken = args[0]
            profile  = args[2] if len(args) > 2 else None
            role     = args[4] if len(args) > 4 else None
            self.startAWSSessionWithMFAToken(nameProfile=profile, mfaToken=mfaToken, assumeRole=role)
        else:
             self.exitWithMessageInvalidUsage()

    
    def parseArgsFindFunction(self, args):
        functions = Functions()
        #
        # Looking for an auxiliar functions (Add Role, Add MFA, List Profiles, Remove Role, Sync, etc.)
        #
        for arg in args:
            func = functions.getFunctionByArgumentIdentifier(arg)
            if func:
               # Check if there's a MFA Token Informed, if it is, the funcion asked was not START_SESSION only, the argument -p must be the first one
               if func == functions.START_SESSION:
                  if args[0] == "-p":
                     return func
                  else:
                     continue
               # Check if there's a MFA Token Informed, if it is, the funcion asked was not ASSUME_ROLE, it is START_SESSION_MFA_TOKEN
               if func == functions.ASSUME_ROLE:
                  if args[0] == "-r":
                     return func
                  else:
                     continue 
               return func

        #
        # Check is command starting with a MFA Token (start AWS Session)
        #
        mfaToken = None
        if self.checkMFATokenValid(args[0]):
           mfaToken = args[0]
        else:
           Messages.showError(f"Invalid MFA Token {Style.GREEN}{args[0]}{Style.IMAGENTA}")
           sys.exit()
        # Check if a profile was passed: "-p [profile] or -p [profile] -r [role]"
        role = None
        if len(args) > 1:
           if len(args) == 4:
               self.exitWithMessageInvalidUsage()
           # Here, It should be -p [PROFILE]    
           elif len(args) == 3:
              if args[1] == "-p":
                 profile = args[2]
              elif args[1] != "-p":
                 self.exitWithMessageInvalidUsage()
           # Here, It should be -p [PROFILE] -r [ROLE]
           elif len(args) == 5:     
               if   args[1] == "-p":
                    profile = args[2]
               if   args[3] == "-p":
                    profile = args[4] 
               if args[1] == "-r":
                    role = args[2]  
               if args[3] == "-r":
                    role    = args[4]
               if (not profile or profile == "") or (not role or role == ""):
                   self.exitWithMessageInvalidUsage()
           else:
              Messages.showError(f"Missing parameter profile [-p profile], check syntax with {Style.GREEN}awsee -h{Style.RESET}")
              sys.exit()
        return functions.START_SESSION_MFA_TOKEN


    def exitWithMessageInvalidUsage(self):
        Messages.showError(f"Invalid usage!\n     Please, check syntax with {Style.GREEN}awsee -h{Style.RESET}")
        sys.exit() 

    def checkMFATokenValid(self, token):
        f = re.findall("[0-9]{6}$",token)
        if len(f) > 0:
            return True
        return False

@atexit.register 
def goodbye(): 
    pass
    #print("Bye!")
    

def main():
    """Start AwsSe"""
    try:
        awsee = AwsSeePy()
        awsee.start()
    except UnicodeEncodeError as e:
        if Utils.isWindows():
           output = f"\n{Style.IRED} --> {Style.IMAGENTA}UnicodeEncode Error{Style.GREEN}\n     If you are using GitBash at Windows\n     disable the use of emoticons at ~/.awsse/awsee.ini, {Style.IBLUE}emoticons-enabled = false{Style.RESET}\n\n"
           output = Utils.removeCharsColors(output) if Preferences().noColor else output
           print(output)

if __name__ == '__main__':
    main()




