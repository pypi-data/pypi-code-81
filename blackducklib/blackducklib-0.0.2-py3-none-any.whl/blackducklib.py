"""Some data loading module."""
import os
import json
from argparse import ArgumentParser

def parse_args():
    # parser = argparse.ArgumentParser(description='Execute BlackDuck on a defined project')
    parser = ArgumentParser()
    parser.add_argument('--jsonfilepath', metavar='', help='Path to JSON File. Required when user wants to read values from JSON')
    parser.add_argument('--javahome', metavar='', help='Path to Java Home upto bin directory')
    parser.add_argument('--blackduckjarpath', metavar='', help='Path to BlackDuck')
    parser.add_argument('--blackduckurl', metavar='', help='BlackDuck URL')
    parser.add_argument('--projectname', metavar='', help='Project Name.')
    parser.add_argument('--sourcepath', metavar='', help='Project Source Path')
    parser.add_argument('--inspectorpath', metavar='', help='Nuget Inspector Path')
    parser.add_argument('--bomaggregatename', metavar='', help='BOM Aggregate Name')
    parser.add_argument('--buildid', metavar='', help='Respective Build Id')
    return parser.parse_args()

def getArguments():
    args = parse_args()
    if args.jsonfilepath == None:
        if (args.javahome != None and args.blackduckjarpath != None and args.blackduckurl != None and args.projectname != None and args.sourcepath != None and args.inspectorpath != None and args.buildid != None):
            executeBlackDuck(args.javahome,args.blackduckjarpath,args.projectname,args.buildid,args.blackduckurl,args.sourcepath,args.inspectorpath,args.bomaggregatename)
        else:
            print("Required positional arguments: 'javahome', 'blackduckpath', 'projectname', 'buildid', 'blackduckurl', 'sourcepath', and 'inspectorpath'")
    else:
        fromJSON(args.jsonfilepath)

def fromJSON(jsonfile):
    if os.path.exists(jsonfile):
        print ("Getting argument value from JSON file.")
        with open(jsonfile) as jfile:
            data = json.load(jfile)
        
        javahome = data["MasterConfiguration"][0]["JAVA_Home"]
        blackduckjarpath = data["MasterConfiguration"][0]["BlackDuckJarPath"]
        blackduckurl = data["MasterConfiguration"][0]["BlackDuckURL"]
        projectname = data["MasterConfiguration"][0]["ProjectName"]
        inspectorpath = data["MasterConfiguration"][0]["nuget_inspector_path"]
        buildid = data["MasterConfiguration"][0]["build_id"]
        print("There are " + len(data["BlackDuck"]))
        i = 0
        while i < (len(data["BlackDuck"])):
            print (i)
            sourcepath = data["BlackDuck"][i]["SourcePath"]
            bomaggregatename = data["BlackDuck"][i]["bom_aggregate_name"]
            executeBlackDuck(javahome,blackduckjarpath,projectname,buildid,blackduckurl,sourcepath,inspectorpath,bomaggregatename)
            i += 1
    else:
        print("Could Not find the JSON file")

def executeBlackDuck(javahome,blackduckpath,projectname,buildid,blackduckurl,sourcepath,inspectorpath,bomaggregatename):
    os.chdir(javahome)
    javacmd = 'java.exe -jar '+ blackduckpath +' --detect.project.name='+ projectname +'-github  --detect.project.version.name='+ projectname +'-github_'+ buildid +' --blackduck.url='+ blackduckurl +' --detect.source.path='+ sourcepath +' --blackduck.trust.cert=true --blackduck.api.token=YWJhZjNhYzUtNWRiMy00Zjc3LTk2MTEtNzQzODMyZjczNzUyOmI0MTdjOGZlLThlOTktNDM1ZC04YWRhLTI3ODM1YTg3MTc4Zg== --detect.nuget.inspector.air.gap.path='+ inspectorpath +' --detect.bom.aggregate.name='+ bomaggregatename +'_'+ buildid
    os.system (javacmd)