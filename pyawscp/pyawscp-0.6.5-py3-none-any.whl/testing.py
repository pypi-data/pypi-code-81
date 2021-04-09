# coding=utf-8

import sys
import json
import os, re
import random
from pyawscp.Functions import Functions
from pyawscp.Utils import Utils, Style
from pyawscp.Config import Config
from pyawscp.TableArgs import TableArgs
from pygments import highlight, lexers, formatters
from pyawscp.PyEc2Cp import PyEc2CP
from pyawscp.PyEc2NetSecCp import PyEc2NetSecCP
from pyawscp.PyElbCp import PyElbCP
from pyawscp.PyS3Cp import PyS3CP
from pyawscp.PyR53Cp import PyR53CP

class Test:
    def __init__(self):
        self.my_function(a=12, _vpcid=123456)

    def my_function(self, **args):
        print(args["_vpcid"])

def loadTmpSession():
    tempConfigFile = os.path.expanduser("~") + "/.pyawscp/myTempSession.tmp"
    if not os.path.exists(tempConfigFile):
       print("")
       print("=".ljust(80,"="))
       print("File {} not found".format(tempConfigFile))
       print("""
       FILE NAME: \033[32mmyTempSession.tmp\033[0m
       EXPECTED FIELDS:\033[32m
       assume-role=NaNaNaNa
       mfa-serial=NaNaNaNa
       region=NaNaNaNa
       profile=NaNaNaNa\033[0m
       """)
       print("=".ljust(80,"="))
       print("")
       sys.exit()
    
    config = Config()
    with open(tempConfigFile, "r") as fp:
        for idx, line in enumerate(fp):
            if not line.startswith("#"):
                if "assume-role=" in line:
                    config.assumeRole = line.replace("assume-role=","").rstrip().lstrip()
                elif "mfa-serial=" in line:
                    config.mfaSerial = line.replace("mfa-serial=","").rstrip().lstrip() 
                elif "region=" in line:
                    config.awsRegion = line.replace("region=","").rstrip().lstrip() 
    config.printResults = False
    config.tableLineSeparator = False

    if len(sys.argv) > 1:
       config.mfaPassCode=sys.argv[1]
    
    print("=".ljust(80,"="))
    print(" All set!")
    print("=".ljust(80,"="))
    return config

def test2():
    config = loadTmpSession()
    pyEc2CP = PyEc2CP(config)
    connBt, data, report, content = pyEc2CP.listEc2()
    print(report)

def testListVpc():
    config = loadTmpSession()
    config.commandArguments = "verbose"
    pyEc2Cp = PyEc2CP(config)
    report = pyEc2Cp.listVpc()
    print(report)

def testListEc2():
    config = loadTmpSession()
    pyEc2Cp = PyEc2CP(config)
    connBt, data, report, content = pyEc2Cp.listEc2()
    print(report)

def testFindRoute():
    config = loadTmpSession()
    #config.commandArguments = "i-0b5d342791d7ed2c4,i-0c54d18dc352d71e6,excel"
    #config.commandArguments = "i-0b5d342791d7ed2c4,i-0c54d18dc352d71e6,save,verbose"
    #config.commandArguments = "i-0b5d342791d7ed2c4,i-0c54d18dc352d71e6,target-group"
    #config.commandArguments = "i-0b5d342791d7ed2c4,i-0c54d18dc352d71e6"
    #config.commandArguments = "i-06f4a5c3bb81fec46,i-0d9a673532481f016,i-09117ce6865a30ab7,i-04a483aed2cf4a8c7"
    config.commandArguments = "i-06f4a5c3bb81fec46,i-0d9a673532481f016,i-09117ce6865a30ab7"

    #config.commandArguments = "i-0d9a673532481f016,i-09117ce6865a30ab7,label-name,target-group"
    #config.commandArguments = "i-0d9a673532481f016,i-09117ce6865a30ab7,target-group"
    #config.commandArguments = "i-0d9a673532481f016,i-09117ce6865a30ab7,label-name"
    config.tableLineSeparator = False

    Utils.clearScreen()
    py = PyR53CP(config)
    data, report = py.findRouteEc2s()
    print(Utils.formatPrettyJson(data))
    #print(report)

    # Utils.saveToFile("TestData.json",data)
    # Load previous data (saved before) to save time on testing only Result Format
    # with open("results/TestData.json", 'r') as f:
    #     jsonSaved = f.read()
    # data = json.loads(jsonSaved)    

    result = py.findRouteEc2sPrintResult(data, config.commandArguments)
    print(result)
   

## Troubleshoot
## in WSL (Bash), in case the Enter is resulting a ^M   use this command "stty sane" before call Python
def test1():
    pass
    # val = input("Enter your value: ") 
    # print(val) 
    # AWS_CREDENTIALS_DIR = "~/.aws/"
    # print("") 
    # print("")
    # print("\033[31m ---> Ops!\033[33m AWS CREDENTIALS NOT FOUND!")
    # print("") 
    # print("") 
    # print("\033[34m ---> \033[33mPlease, configure your AWS Credentials:")
    # print("\033[34m      \033[33m1. Create the folder \033[35m{}\033[0m".format(AWS_CREDENTIALS_DIR))
    # print("\033[34m      \033[33m2. Create the file \033[35m{}credentials\033[33m with the  content:".format(AWS_CREDENTIALS_DIR))
    # print("\033[34m      \033[94m   [default]")
    # print("\033[34m      \033[94m   aws_access_key_id = YOUR_ACCESS_KEY")
    # print("\033[34m      \033[94m   aws_secret_access_key = YOUR_SECRET_KEY")
    # print("\033[34m      \033[33m3. Optionally, create the file \033[35m{}config\033[33m with your default region:".format(AWS_CREDENTIALS_DIR))
    # print("\033[34m      \033[94m   [default]")
    # print("\033[34m      \033[94m   region=us-east-1")
    # print("")
    # print("")

def main():
    testFindRoute()
    #testListEc2()
    #testListVpc()

if __name__ == '__main__':
    main()
        