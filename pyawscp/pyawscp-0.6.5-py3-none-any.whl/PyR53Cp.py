# coding=utf-8
#
# Author: Ualter Azambuja Junior
# ualter.junior@gmail.com
#

import boto3
import logging
import sys, os
import json
import math
from pygments import highlight, lexers, formatters
from botocore.exceptions import ClientError
from datetime import datetime
from arnparse import arnparse
from pyawscp.Functions import Functions
from pyawscp.Utils import Utils, Style
from pyawscp.PrettyTable import PrettyTable
from pyawscp.PyAsciiGraphs import PyAsciiGraphs, Leaf
from pyawscp.Emoticons import Emoticons
from pyawscp.Config import Config
from pyawscp.TableArgs import TableArgs
from pyawscp.pymxgraph.PymxGraph import PymxGraph
from pyawscp.pymxgraph.PymxGraphTree import PymxGraphTree

LOG = logging.getLogger("app." + __name__)
LOG.setLevel(logging.INFO)

FORM_WIDTH   = 162 #185
LINE         = "-"
CROSSROAD    = "+"
LATERAL      = "|"
MARGIN       = " ".ljust(4, " ")
MARGIN_CONN1 = " " + CROSSROAD + LINE + LINE
MARGIN_CONN2 = " " + LATERAL   + "  "
MARGIN_CONN3 = " " + CROSSROAD + LINE + ">"
FIELD_SIZE   = 23

class PyR53CP:
    config = None

    def __init__(self, config):
        self.config = config
    
    def _print_there(self, x, y, text):
        sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x, y, text))
        sys.stdout.flush()

    def nslookupEc2R53(self):
        r53api       = self.botoSession().client('route53')
        dnsName      = ""
        tableArgs    = TableArgs()
        tableArgs.setArguments(self.config.commandArguments)
        thinForm     = False
        graphDisplay = False

        if "," in self.config.commandArguments:
           dnsName = self.config.commandArguments.split(",")[0]
           tableArgs.setArguments(self.config.commandArguments)
           if "thin" in self.config.commandArguments:
              thinForm = True
           elif "graph" in self.config.commandArguments:
              graphDisplay = True   
        else:    
           dnsName = tableArgs.cleanPipelineArguments()

        if not dnsName:
           resultTxt = "Where is the DNS? You didn't tell me which DNS to look for " + Emoticons.ops() +  Style.RESET
           return Utils.formatResult(Functions.NSLOOKUP_EC2_R53,resultTxt, self.config, "", True, tableArgs)

        filters=[]
        if self.config.awsTagsToFilter():
           # Environment Tags set
           for tag in self.config.awsTags: 
               filters.append(
                   {'Name':'tag:' + tag,'Values':[self.config.awsTags[tag]]}
               )

        # Tags from command line arguments
        if len(tableArgs.tagsTemp) > 0:
           for tag in tableArgs.tagsTemp: 
               filters.append(
                   {'Name':'tag:' + tag,'Values':[tableArgs.tagsTemp[tag]]}
               )

        if dnsName.endswith("."):
           dnsName = dnsName[:len(dnsName)-1]
        words = dnsName.split(".")

        w                 = ""
        pos               = len(words) - 1
        found             = False
        result            = {}
        result["dnsName"] = dnsName

        # Seek for the Hosted Zoned and the
        # ResourceRecordSet with the DNSName passed as entry paramater
        Utils.clearScreen()
        while pos >= 0 and not found:
            w = "." + words[pos] + w
            if pos < len(words) - 1:
               domain = w + "."    
               if domain.startswith("."):
                  domain = domain[1:]
               self._print_there(3, 1, "Searching \033[35m{} \033[0mat \033[32m{}\033[0m".format(dnsName, domain))
               listHostedZones = r53api.list_hosted_zones_by_name(DNSName=domain,MaxItems='1') 
               if listHostedZones and len(listHostedZones["HostedZones"]) > 0:
                  for hz in listHostedZones["HostedZones"]:
                      nextRecordName          = None
                      nextRecordType          = None
                      listResourceResourceSet = r53api.list_resource_record_sets(HostedZoneId=hz["Id"])
                      if "IsTruncated" in listResourceResourceSet and listResourceResourceSet["IsTruncated"] == True:
                          nextRecordName      = listResourceResourceSet["NextRecordName"]
                          nextRecordType      = listResourceResourceSet["NextRecordType"]

                      line  = 0
                      page  = 0
                      while listResourceResourceSet and len(listResourceResourceSet["ResourceRecordSets"]) > 0:
                            for rs in listResourceResourceSet["ResourceRecordSets"]:
                                line += 1
                                if dnsName in rs["Name"] and  rs["Type"] == "A": 
                                   self._print_there(4, 1, "--> Page {} \033[32m <-- Found it!\033[0m".format(page+1) )
                                   result["route53"] = {}
                                   result["route53"]["hostedZoneId"] = hz["Id"] 
                                   found = True
                                   if "ResourceRecords" in rs:
                                       result["route53"]["ResourceRecords"] = []
                                       for v in rs["ResourceRecords"]:
                                           result["route53"]["ResourceRecords"].append(v)
                                   if "AliasTarget" in rs:
                                      result["route53"]["AliasTarget"] = {}
                                      result["route53"]["AliasTarget"]["DNSName"] = rs["AliasTarget"]["DNSName"]
                                      result["route53"]["AliasTarget"]["Type"]    = rs["Type"]
                                   break
                            # Not Found and there's more page, keep searching...     
                            if not found and nextRecordName:
                               self._print_there(4, 1, "--> Page {}".format(page+1) + " ".ljust(80," "))
                               listResourceResourceSet = r53api.list_resource_record_sets(HostedZoneId=hz["Id"],StartRecordName=nextRecordName,StartRecordType=nextRecordType)
                               #Utils.saveDictAsJson("listResourceResourceSet",listResourceResourceSet)
                               if "IsTruncated" in listResourceResourceSet and listResourceResourceSet["IsTruncated"] == True:
                                   nextRecordName = listResourceResourceSet["NextRecordName"]
                                   nextRecordType = listResourceResourceSet["NextRecordType"]
                                   page += 1
                               else:
                                   nextRecordName = None
                                   nextRecordType = None
                            else:
                               break        
               else:
                  print("nothing found for \033[32m{domain}\033[0m".format(domain=domain))       
            pos -= 1

        if found:
           # Found Hosted Zoned and ResourceRecordset
           # In case DNSName of a Load Balance
           if "AliasTarget" in result["route53"]:
              elbv2Api     = self.botoSession().client('elbv2')
              loadBalancers = elbv2Api.describe_load_balancers()
              for lb in loadBalancers["LoadBalancers"]:
                 if lb["DNSName"] in result["route53"]["AliasTarget"]["DNSName"]:
                    result["elb"] = {}
                    result["elb"]["DNSName"]           = lb["DNSName"]
                    result["elb"]["AvailabilityZones"] = lb["AvailabilityZones"]
                    result["elb"]["LoadBalancerArn"]   = lb["LoadBalancerArn"]
                    result["elb"]["LoadBalancerName"]  = lb["LoadBalancerName"]
                    result["elb"]["Scheme"]            = lb["Scheme"]
                    result["elb"]["Type"]              = lb["Type"]
                    result["elb"]["VpcId"]             = lb["VpcId"]
                    result["elb"]["State"]             = lb["State"]
                    result["elb"]["SecurityGroups"]    = lb["SecurityGroups"]
                    result["elb"]["CreatedTime"]       = lb["CreatedTime"]
                    # Check For Existent Listener Rules
                    elbListeners  = elbv2Api.describe_listeners(LoadBalancerArn=result["elb"]["LoadBalancerArn"])
                    result["elb"]["TotalListeners"] = len(elbListeners)
                    result["elb"]["Listeners"]      = []
                    for elbListener in elbListeners["Listeners"]:
                        objDefaultActions = []
                        for defaultAction in elbListener["DefaultActions"]:
                            objRedirectConfig = None
                            if "RedirectConfig" in defaultAction:
                                objRedirectConfig = {
                                   "Protocol":defaultAction["RedirectConfig"]["Protocol"],
                                   "Port":defaultAction["RedirectConfig"]["Port"],
                                   "Host":defaultAction["RedirectConfig"]["Host"],
                                   "Path":defaultAction["RedirectConfig"]["Path"],
                                   "Query":defaultAction["RedirectConfig"]["Query"],
                                   "StatusCode":defaultAction["RedirectConfig"]["StatusCode"]
                                }
                            objDefaultAction = {
                               "Type":defaultAction["Type"],
                               "Order":defaultAction["Order"] if "Order" in defaultAction else ""
                            }    
                            if "TargetGroupArn" in defaultAction:
                               objDefaultAction["TargetGroupArn"] = defaultAction["TargetGroupArn"]
                            if objRedirectConfig:
                               objDefaultAction["RedirectConfig"] = objRedirectConfig
                            objDefaultActions.append(objDefaultAction)    
                        objListener = {
                           "ListenerArn": elbListener["ListenerArn"],
                           "LoadBalancerArn": elbListener["LoadBalancerArn"],
                           "Port": elbListener["Port"],
                           "Protocol": elbListener["Protocol"],
                           "DefaultActions": objDefaultActions
                        }

                        elbListenersRules = elbv2Api.describe_rules(ListenerArn=elbListener["ListenerArn"])
                        objListenerRules  = []
                        for elbListenerRule in elbListenersRules["Rules"]:
                            # Add CONDITIONS
                            conditions = []
                            if "Conditions" in elbListenerRule:
                               for condition in elbListenerRule["Conditions"]:
                                   conditions.append({
                                      "Field": condition["Field"],
                                      "Values": condition["Values"]
                                   })
                            # Add ACTIONS
                            actions = []
                            if "Actions" in elbListenerRule:
                               for action in elbListenerRule["Actions"]:
                                   actions.append({
                                      "Type": action["Type"],
                                      "TargetGroupArn": action["TargetGroupArn"] if "TargetGroupArn" in action else None,
                                      "Order": action["Order"] if "Order" in action else "",
                                   })
                            objListenerRule = {
                               "RuleArn": elbListenerRule["RuleArn"],
                               "Priority": elbListenerRule["Priority"],
                               "IsDefault": elbListenerRule["IsDefault"],
                               "Conditions": conditions,
                               "Actions": actions
                            }
                            objListenerRules.append(objListenerRule)

                        objListener["ListenerRules"] = objListenerRules
                        result["elb"]["Listeners"].append(objListener)
                    break
              
              target_groups = elbv2Api.describe_target_groups(LoadBalancerArn=result["elb"]["LoadBalancerArn"])
              result["targetGroup"] = []
              for tg in target_groups["TargetGroups"]:
                  t = {
                     "TargetGroupArn":tg["TargetGroupArn"],
                     "TargetGroupName":tg["TargetGroupName"],
                     "HealthCheckPath":tg["HealthCheckPath"],
                     "HealthCheckPort":tg["HealthCheckPort"],
                     "HealthCheckIntervalSeconds":tg["HealthCheckIntervalSeconds"],
                     "Port":tg["Port"],
                     "Protocol":tg["Protocol"],
                     "TargetType":tg["TargetType"],
                     "Targets": []
                  }
                  result["targetGroup"].append(t)

              ec2Api = self.botoSession().client('ec2')   
              for tg in result["targetGroup"]:
                  targetGroupHealth = elbv2Api.describe_target_health(TargetGroupArn=tg["TargetGroupArn"])
                  for tgh in targetGroupHealth["TargetHealthDescriptions"]:
                      id           = tgh["Target"]["Id"]    if ("Target"          in tgh and "Id"   in tgh["Target"]) else ""
                      port         = tgh["Target"]["Port"]  if ("Target"          in tgh and "Port" in tgh["Target"]) else ""
                      portHealth   = tgh["HealthCheckPort"] if ("HealthCheckPort" in tgh) else ""
                      descHealth   = tgh["TargetHealth"]["Description"]if ("TargetHealth" in tgh and "Description" in tgh["TargetHealth"]) else ""
                      reasonHealth = tgh["TargetHealth"]["Reason"]     if ("TargetHealth" in tgh and "Reason"      in tgh["TargetHealth"]) else ""

                      # Now, grab the rest of information about the Instance (IP, etc.) 
                      # in the ec2-describe-instance(InstanceIds="i-0c97d7df9ad273ee2 i-0c97d7df9ad273ee2")
                      privateIp       = ""
                      instanceType    = ""
                      privateDnsName  = ""
                      publicDnsName   = ""
                      securityGroups  = {}
                      state           = {}
                      subnetId        = ""
                      if id:
                         reservations = ec2Api.describe_instances(InstanceIds=[id])
                         for reservation in reservations["Reservations"]:
                            for instance in reservation["Instances"]:
                               if instance["InstanceId"] == id:
                                  privateIp       = instance["PrivateIpAddress"]
                                  instanceType    = instance["InstanceType"]
                                  privateDnsName  = instance["PrivateDnsName"]
                                  publicDnsName   = instance["PublicDnsName"]
                                  securityGroups  = instance["SecurityGroups"]
                                  state           = instance["State"]
                                  subnetId        = instance["SubnetId"]
                                  break

                         #print(highlight(Utils.dictToJson(ec2Info), lexers.JsonLexer(), formatters.TerminalFormatter()))      

                      target = {
                        "Id": id,
                        "Port": port,
                        "PrivateIpAddress": privateIp,
                        "InstanceType":instanceType,
                        "PrivateDnsName":privateDnsName,
                        "PublicDnsName":publicDnsName,
                        "SecurityGroups":securityGroups,
                        "State":state,
                        "SubnetId":subnetId,
                        "health": {
                           "Port": portHealth,
                           "Description": descHealth,
                           "Reason": reasonHealth
                        }
                      }
                      tg["Targets"].append(target)

           #print(highlight(Utils.dictToJson(result), lexers.JsonLexer(), formatters.TerminalFormatter()))      
           #print("\n----------------------------------------------------------------------------")   

           jsonResult = ""
           if self.config.printResults or tableArgs.verbose or tableArgs.saveToFile:
              jsonResult = Utils.dictToJson(result)

           tree       = {}
           formResult = None
           if thinForm:
              formResult = self._buildSummaryForm(dnsName, result)
           elif graphDisplay:
              tree["root"] = {}
              tree["root"]["dnsName"] = result["dnsName"]
              tree["root"]["children"] = []
              
              if "elb" in result:
                 groupListeners = []
                 for objListeners in result["elb"]["Listeners"]:
                     listener = {}
                     listener["label"]    = "Listener"
                     listener["Port"]     = objListeners["Port"]
                     listener["Protocol"] = objListeners["Protocol"]
                     listener["children"] = []

                     groupListenerRules = []
                     for objDefaultActions in objListeners["DefaultActions"]:
                         listenerRule               = {}
                         listenerRule["label"]      = "Rule"
                         listenerRule["Type"]       = objDefaultActions["Type"]

                         if objDefaultActions["Type"] == "redirect" and ("RedirectConfig" in objDefaultActions and objDefaultActions["RedirectConfig"] != ""):
                            listenerRule["Rule"] = "{}://{}:{}{}{}".format(objDefaultActions["RedirectConfig"]["Protocol"],objDefaultActions["RedirectConfig"]["Host"],objDefaultActions["RedirectConfig"]["Port"],objDefaultActions["RedirectConfig"]["Path"],objDefaultActions["RedirectConfig"]["Query"])
                            groupListenerRules.append(listenerRule)
                         #elif objDefaultActions["Type"] == "forward":   
                         #   listenerRule["TargetGroupArn"] = objDefaultActions["TargetGroupArn"]
                         #   groupListenerRules.append(listenerRule)

                     for objListenerRules in objListeners["ListenerRules"]:
                         listenerRule = {}
                         listenerRule["label"] = "Rule"
                         if "IsDefault" in objListenerRules and objListenerRules["IsDefault"]:
                             listenerRule["IsDefault"] = True
                         for objActions in objListenerRules["Actions"]:
                             listenerRule["Type"]           = objActions["Type"]
                             listenerRule["TargetGroupArn"] = objActions["TargetGroupArn"]
                             listenerRule["children"]       = []
                             for targetGroup in result["targetGroup"]:
                                 if targetGroup["TargetGroupArn"] == objActions["TargetGroupArn"]:
                                    tgs = []
                                    for target in targetGroup["Targets"]:
                                       tgs.append({
                                          "label":"Target",
                                          "PrivateIpAddress":target["PrivateIpAddress"],
                                          "Id":target["Id"] if "Id" in target else "",
                                          "SubnetId":target["SubnetId"],
                                          "Port":target["Port"],
                                          "InstanceType":target["InstanceType"],
                                       })
                                    tGroup = {
                                       "label":"TargetGroup",
                                       "TargetGroupName":targetGroup["TargetGroupName"],
                                       "Protocol":targetGroup["Protocol"],
                                       "Port":targetGroup["Port"],
                                       "children": tgs
                                    }
                                    listenerRule["children"].append(tGroup)
                                    break
                         listenerRule["Condition"] = ""     
                         for objConditions in objListenerRules["Conditions"]:   
                             if len(listenerRule["Condition"]) > 0:
                                listenerRule["Condition"] += " AND "
                             listenerRule["Condition"] += objConditions["Field"] + " = " + str(objConditions["Values"])
                         if listenerRule["Type"] != "redirect" or listenerRule["Condition"] != "":
                            groupListenerRules.append(listenerRule)  

                     listener["children"] = groupListenerRules
                     groupListeners.append(listener)  
                 elb = {
                    "label":"ELB",
                    "LoadBalancerName":result["elb"]["LoadBalancerName"],
                    "children": groupListeners
                 }
                 route53 = {
                    "label": "Route53",
                    "DNSName": result["route53"]["AliasTarget"]["DNSName"],
                    "hostedZoneId": result["route53"]["hostedZoneId"],
                    "children": []
                 }
                 route53["children"].append(elb)
                 tree["root"]["children"].append(route53)
              # No ELB, A Direct IP(s) Assigned   
              elif "ResourceRecords" in result["route53"]:
                 records = []
                 for record in result["route53"]["ResourceRecords"]:
                    records.append({
                       "Value":record["Value"]
                    })
                 route53 = {
                    "label": "Route53",
                    "hostedZoneId": result["route53"]["hostedZoneId"],
                    "children": records
                 }   
                 tree["root"]["children"].append(route53)

              #pathToResources = "./pymxgraph"
              pathToResources = "./"
              pymxGraph = PymxGraph(pathToResources)
              pymxGraphTree = PymxGraphTree(pathToResources, pymxGraph.images, pymxGraph.htmlSnippets)

              #Utils.addToClipboard(Utils.dictToJson(tree))
              #print(highlight(Utils.dictToJson(tree), lexers.JsonLexer(), formatters.TerminalFormatter()))
              
              nodes         = ""
              indexNodeR53  = 0
              for childR53 in tree["root"]["children"]:
                  indexNodeR53 += 1
                  label = "<b>" + childR53["label"] + " </b><br> " + childR53["hostedZoneId"].replace("/hostedzone/","")
                  nodes += "var v{indexR53} = graph.insertVertex(parent, 'v{indexR53}', '{lbl}', 0, 0, widthLeaf, heightLeaf,'whiteSpace=wrap;');".format(indexR53=indexNodeR53,lbl=label)
                  nodes += "graph.insertEdge(parent, null, '', root, v{indexR53});".format(indexR53=indexNodeR53)

                  indexNodeELB = 0
                  for childELB in childR53["children"]:
                     indexNodeELB += 1
                     label = "<b>" + childELB["label"] + " </b><br> " + childELB["LoadBalancerName"]
                     nodes += "var v{indexR53}{indexELB} = graph.insertVertex(parent, 'v{indexR53}{indexELB}', '{lbl}', 0, 0, widthLeaf, heightLeaf,'whiteSpace=wrap;');".format(indexR53=indexNodeR53,indexELB=indexNodeELB,lbl=label)
                     nodes += "graph.insertEdge(parent, null, '', v{indexR53}, v{indexR53}{indexELB});".format(indexR53=indexNodeR53,indexELB=indexNodeELB)

                     indexNodeListener = 0
                     for childListener in childELB["children"]:
                         indexNodeListener += 1
                         label  = "<b>" + childListener["label"] + "</b><br>{}:{}".format(childListener["Protocol"],childListener["Port"])
                         nodes += "var v{indexR53}{indexELB}{indexListener} = graph.insertVertex(parent, 'v{indexR53}{indexELB}{indexListener}', '{lbl}', 0, 0, 200, heightLeaf,'whiteSpace=wrap;');".format(indexR53=indexNodeR53,indexELB=indexNodeELB,indexListener=indexNodeListener,lbl=label)
                         nodes += "graph.insertEdge(parent, null, '', v{indexR53}{indexELB}, v{indexR53}{indexELB}{indexListener});".format(indexR53=indexNodeR53,indexELB=indexNodeELB,indexListener=indexNodeListener)

                         indexNodeListenerRule = 0
                         for childListenerRule in childListener["children"]:
                            indexNodeListenerRule += 1
                            label = "<b>{}</b><br><i>{}</i>".format(childListenerRule["label"],childListenerRule["Type"])
                            if "IsDefault" in childListenerRule and childListenerRule["IsDefault"]:
                                label += "<br>{}".format("Default")
                            else:
                                label += "<br>"
                            if childListenerRule["Type"] == "redirect":
                               if "Rule" in childListenerRule:
                                  label += childListenerRule["Rule"]
                               if "Condition" in childListenerRule and childListenerRule["Condition"] != "":
                                  label += childListenerRule["Condition"].replace("'","\\'")
                            elif childListenerRule["Type"] == "forward":
                               if "Condition" in childListenerRule and childListenerRule["Condition"] != "":
                                  label += childListenerRule["Condition"].replace("'","\\'")
                            nodes += "var v{indexR53}{indexELB}{indexListener}{indexListenerRule} = graph.insertVertex(parent, 'v{indexR53}{indexELB}{indexListener}{indexListenerRule}', '{lbl}', 0, 0, 200, heightLeaf + 30,'whiteSpace=wrap;');".format(indexR53=indexNodeR53,indexELB=indexNodeELB,indexListener=indexNodeListener,indexListenerRule=indexNodeListenerRule,lbl=label)
                            nodes += "graph.insertEdge(parent, null, '', v{indexR53}{indexELB}{indexListener}, v{indexR53}{indexELB}{indexListener}{indexListenerRule});".format(indexR53=indexNodeR53,indexELB=indexNodeELB,indexListener=indexNodeListener,indexListenerRule=indexNodeListenerRule)      
                            
                            if "children" in childListenerRule:
                               indexNodeTargetGroup = 0   
                               for childTargetGroup in childListenerRule["children"]:
                                  indexNodeTargetGroup += 1
                                  label  = "<b>" + childTargetGroup["label"] + "</b><br> " + childTargetGroup["TargetGroupName"] + " <br> " + "{}:{}".format(childTargetGroup["Protocol"],childTargetGroup["Port"])
                                  nodes += "var v{indexR53}{indexELB}{indexListener}{indexListenerRule}{indexTargetGroup} = graph.insertVertex(parent, 'v{indexR53}{indexELB}{indexListener}{indexListenerRule}{indexTargetGroup}', '{lbl}', 0, 0, 200, heightLeaf + 5,'whiteSpace=wrap;');".format(indexR53=indexNodeR53,indexELB=indexNodeELB,indexListener=indexNodeListener,indexListenerRule=indexNodeListenerRule,indexTargetGroup=indexNodeTargetGroup,lbl=label)
                                  nodes += "graph.insertEdge(parent, null, '', v{indexR53}{indexELB}{indexListener}{indexListenerRule}, v{indexR53}{indexELB}{indexListener}{indexListenerRule}{indexTargetGroup});".format(indexR53=indexNodeR53,indexELB=indexNodeELB,indexListener=indexNodeListener,indexListenerRule=indexNodeListenerRule,indexTargetGroup=indexNodeTargetGroup)
      
                                  indexNodeTarget = 0
                                  for childTarget in childTargetGroup["children"]:
                                     indexNodeTarget += 1
                                     label  = "<b>" + childTarget["label"] + " </b><br> " + childTarget["PrivateIpAddress"] 
                                     if "Id" in childTarget:
                                         label += " <br> " + childTarget["Id"]
                                     if "InstanceType" in childTarget:
                                         label += " <br> " + childTarget["InstanceType"]    
                                     if "SubnetId" in childTarget:
                                         label += " <br> " + childTarget["SubnetId"]
                                     nodes += "var v{indexR53}{indexELB}{indexListener}{indexListenerRule}{indexTargetGroup}{indexTarget} = graph.insertVertex(parent, 'v{indexR53}{indexELB}{indexListener}{indexListenerRule}{indexTargetGroup}{indexTarget}', '{lbl}', 0, 0, 200, 85,'whiteSpace=wrap;');".format(indexR53=indexNodeR53,indexELB=indexNodeELB,indexListener=indexNodeListener,indexListenerRule=indexNodeListenerRule,indexTargetGroup=indexNodeTargetGroup,indexTarget=indexNodeTarget,lbl=label)
                                     nodes += "graph.insertEdge(parent, null, '', v{indexR53}{indexELB}{indexListener}{indexListenerRule}{indexTargetGroup}, v{indexR53}{indexELB}{indexListener}{indexListenerRule}{indexTargetGroup}{indexTarget});".format(indexR53=indexNodeR53,indexELB=indexNodeELB,indexListener=indexNodeListener,indexListenerRule=indexNodeListenerRule,indexTargetGroup=indexNodeTargetGroup,indexTarget=indexNodeTarget)
              
              str_tree = """
                            var widthLeaf  = 200;
                            var heightLeaf = 50;

                            var w = graph.container.offsetWidth;
                            var root = graph.insertVertex(parent, 'treeRoot', '"""+ tree["root"]["dnsName"] + """', w/2 - 30, 20, 250, heightLeaf,'whiteSpace=wrap;');

                            """ + nodes + """
                           
                            //toggleSubtree(graph, v2, false);
                            //graph.model.setCollapsed(v2, true);
              """
              
              pymxGraphTree.drawTree(str_tree)
           else:   
              formResult = self._buildCompleteForm(dnsName, result)

           Utils.clearScreen()
           if formResult:
              return Utils.formatResult(Functions.FUNCTIONS[Functions.NSLOOKUP_EC2_R53]["name"], formResult, self.config, jsonResult, False, tableArgs)
           else:
              if graphDisplay:
                 resultTxt = "  " + Emoticons.thumbsUp() + " The graphic for {} should be \n     opened in external browser window".format(Style.IBLUE + dnsName + Style.RESET) 
                 return Utils.formatResult(Functions.FUNCTIONS[Functions.NSLOOKUP_EC2_R53]["name"],resultTxt, self.config, jsonResult, False, tableArgs)
              else:
                 return ""   
        else:   
           Utils.clearScreen()
           resultTxt = "  " + Emoticons.ops() + " Nothing was found for the DNSName " + Style.IBLUE + dnsName + Style.RESET
           return Utils.formatResult(Functions.NSLOOKUP_EC2_R53,resultTxt, self.config, "", False, tableArgs)

    def _buildCompleteForm(self, dnsName, result):
         asciiForm     = ""
         lineSeparator = MARGIN + CROSSROAD + LINE.ljust(FORM_WIDTH, LINE) + CROSSROAD + "\n"
         lineEmtpy     = MARGIN + LATERAL + " ".ljust(FORM_WIDTH," ") + LATERAL + "\n" 
         asciiForm    += lineSeparator
         asciiForm    += lineEmtpy                    
         # DNS Name Seeked
         line           = MARGIN_CONN1 + LATERAL + Style.IYELLOW + "  " + dnsName + Style.RESET
         asciiForm     += line + self._calculateRemainingSpace(line) + LATERAL + "\n"
         lineEmtpy2     = MARGIN_CONN2 + LATERAL + " ".ljust(FORM_WIDTH," ") + LATERAL + "\n" 
         asciiForm     += lineEmtpy2
         lineSeparator2 = MARGIN_CONN2 + CROSSROAD + LINE.ljust(FORM_WIDTH, LINE) + CROSSROAD + "\n"
         asciiForm     += lineSeparator2
         # Route 53
         asciiForm    += self._buildHeader(MARGIN_CONN3, "ROUTE R53")
         if "AliasTarget" in result["route53"]:
             asciiForm    += lineSeparator2
             asciiForm    += lineEmtpy2
             asciiForm    += self._buildLine(MARGIN_CONN2, "DNS Name", result["route53"]["AliasTarget"]["DNSName"])
             asciiForm    += self._buildLine(MARGIN_CONN2, "Type", result["route53"]["AliasTarget"]["Type"])
             asciiForm    += self._buildLine(MARGIN_CONN2, "Hosted Zone Id", result["route53"]["hostedZoneId"])
             asciiForm    += lineEmtpy2
             asciiForm    += lineSeparator2
             # ELB
             asciiForm    += self._buildHeader(MARGIN_CONN3, "ELB")
             asciiForm    += lineSeparator2
             asciiForm    += self._buildLine(MARGIN_CONN2, "Name", result["elb"]["LoadBalancerName"])
             asciiForm    += self._buildLine(MARGIN_CONN2, "DNS Name", result["elb"]["DNSName"])
             asciiForm    += self._buildLine(MARGIN_CONN2, "ARN", result["elb"]["LoadBalancerArn"])
             asciiForm    += self._buildLine(MARGIN_CONN2, "Create At", result["elb"]["CreatedTime"].strftime("%Y%m%d-%H%M%S"))
             asciiForm    += self._buildLine(MARGIN_CONN2, "Scheme", result["elb"]["Scheme"])
             asciiForm    += self._buildLine(MARGIN_CONN2, "Type", result["elb"]["Type"])
             asciiForm    += self._buildLine(MARGIN_CONN2, "Vpc Id", result["elb"]["VpcId"])
             asciiForm    += lineEmtpy2
    
             # AZs 
             line          = MARGIN_CONN2 + LATERAL + Style.BLUE + "  AVAILABILITY ZONES ({:02d})".format(len(result["elb"]["AvailabilityZones"])) + Style.RESET
             asciiForm    += line + self._calculateRemainingSpace(line) + LATERAL + "\n"
             for az in result["elb"]["AvailabilityZones"]:
                asciiForm += self._buildLineSubItemHeader(MARGIN_CONN2,az["ZoneName"], az["SubnetId"])
             asciiForm    += lineEmtpy2 
             
             # Listeners 
             line       = MARGIN_CONN2 + LATERAL + Style.BLUE + "  LISTENERS ({:02d})".format(len(result["elb"]["Listeners"])) + Style.RESET
             asciiForm += line + self._calculateRemainingSpace(line) + LATERAL + "\n"
             for listener in result["elb"]["Listeners"]:
                asciiForm += self._buildLineSubItemHeader(MARGIN_CONN2,"Listener",listener["ListenerArn"])
                asciiForm += self._buildLineSubItem(MARGIN_CONN2,"Protocol / Port",listener["Protocol"] + " / " + str(listener["Port"]))
    
                if "DefaultActions" in listener:
                   asciiForm += self._addLine(MARGIN_CONN2, Style.BLUE + "     DEFAULT ACTIONS" + Style.RESET)
                   for defaultAction in listener["DefaultActions"]:
                      asciiForm += self._buildLineSubItemHeaderSecondLevel(MARGIN_CONN2, "Type", defaultAction["Type"])
                      asciiForm += self._buildLineSubItemSecondLevel(MARGIN_CONN2, "Order", str(defaultAction["Order"]))
                      if "RedirectConfig" in defaultAction:
                            label = "{}://{}:{}/{}?{} -- (Status Code: {})".format(defaultAction["RedirectConfig"]["Protocol"],defaultAction["RedirectConfig"]["Host"],defaultAction["RedirectConfig"]["Port"],defaultAction["RedirectConfig"]["Path"],defaultAction["RedirectConfig"]["Query"],defaultAction["RedirectConfig"]["StatusCode"])
                            asciiForm += self._buildLineSubItemSecondLevel(MARGIN_CONN2, "Redirect Config", label)
                      if "TargetGroupArn" in defaultAction:
                            asciiForm += self._buildLineSubItemSecondLevel(MARGIN_CONN2, "Target Group", str(defaultAction["TargetGroupArn"]))    
    
                if "ListenerRules" in listener:
                   asciiForm += self._addLine(MARGIN_CONN2, Style.BLUE + "     LISTENER RULES ({:02d})".format(len(listener["ListenerRules"])) + Style.RESET)
                   for rule in listener["ListenerRules"]:
                      asciiForm += self._buildLineSubItemHeaderSecondLevelTitle(MARGIN_CONN2, "RULE --> Priority \033[94m{}\033[0m".format(rule["Priority"]))
    
                      labelCondition = None
                      if "Conditions" in rule:
                         for condition in rule["Conditions"]:
                               labelCondition = "       \033[34mIF\033[32m {} \033[34m==\033[32m {} \033[34mTHEN\033[32m".format(condition["Field"],condition["Values"])
    
                      labelActions1 = None
                      labelActions2 = None
                      if "Actions" in rule:
                         for action in rule["Actions"]:
                               labelActions1     = "          {} \033[34m{}\033[34m".format(action["Type"],"TO" if action["TargetGroupArn"] else "")
                               if action["TargetGroupArn"]:
                                  labelActions2  = "          \033[32m{}\033[34m".format(action["TargetGroupArn"])
    
                      if labelCondition:
                         asciiForm += self._buildLine(MARGIN_CONN2, None, labelCondition)       
                      if labelActions1:   
                         asciiForm += self._buildLine(MARGIN_CONN2, None, labelActions1)   
                      if labelActions2:   
                         asciiForm += self._buildLine(MARGIN_CONN2, None, labelActions2)   

         if "targetGroup" in result:
            asciiForm      += lineEmtpy2
            asciiForm      += lineSeparator2
            margin          = MARGIN_CONN2
            idxTargetGroups = len(result["targetGroup"])
            # TARGET GROUPS
            asciiForm    += self._buildHeader(MARGIN_CONN3, "TARGET GROUPS ({:02d})".format(idxTargetGroups))
            asciiForm    += lineSeparator2
            index = 0
            for targetGroup in result["targetGroup"]:
               index += 1
               if index == idxTargetGroups:
                  margin = MARGIN
               asciiForm    += self._buildHeader(MARGIN_CONN3, "TARGET GROUP ({:02d})".format(index))
               asciiForm += self._buildLine(margin, "\033[37m•\033[94m Name", targetGroup["TargetGroupName"]) 
               asciiForm += self._buildLine(margin, "  ARN", targetGroup["TargetGroupArn"]) 
               asciiForm += self._buildLine(margin, "  Type", targetGroup["TargetType"]) 
               asciiForm += self._buildLine(margin, "  Protocol / Port","{} / {}".format(targetGroup["Protocol"], targetGroup["Port"])) 
               line       = margin + LATERAL + Style.BLUE + "    HEALTH CHECK" + Style.RESET
               asciiForm += line + self._calculateRemainingSpace(line) + LATERAL + "\n"
               asciiForm += self._buildLineSubItem(margin,"  Interval Seconds", "{:02d}".format(targetGroup["HealthCheckIntervalSeconds"]))
               asciiForm += self._buildLineSubItem(margin,"  Path", targetGroup["HealthCheckPath"])
               asciiForm += self._buildLineSubItem(margin,"  Port", targetGroup["HealthCheckPort"])
                  
               totalTargets = len(targetGroup["Targets"])
               asciiForm += self._addLine(margin, Style.BLUE + "    TARGETS ({:02d})".format(totalTargets) + Style.RESET) 
               for target in targetGroup["Targets"]:
                     asciiForm += self._buildLineSubItemHighlighted(margin,"\033[37m•\033[94m Instance Id", target["Id"])
                     asciiForm += self._buildLineSubItem(margin,"  Instance Type", target["InstanceType"])
                     asciiForm += self._buildLineSubItem(margin,"  Port", "{}".format(target["Port"]))
                     asciiForm += self._buildLineSubItem(margin,"  Private IP", target["PrivateIpAddress"])
                     asciiForm += self._buildLineSubItem(margin,"  Private DNS Name", target["PrivateDnsName"])
                     asciiForm += self._buildLineSubItem(margin,"  Public DNS Name", target["PublicDnsName"])
                     asciiForm += self._buildLineSubItem(margin,"  State", target["State"]["Name"])
                     asciiForm += self._buildLineSubItem(margin,"  Subnet Id", target["SubnetId"])
                     line       = margin + LATERAL + Style.BLUE + "       SECURITY GROUPS ({:02d})".format(len(target["SecurityGroups"])) + Style.RESET
                     asciiForm += line + self._calculateRemainingSpace(line) + LATERAL + "\n"
                     for sg in target["SecurityGroups"]:
                        asciiForm += self._buildLineSubItem(margin,"  \033[37m•\033[94m Group Id", sg["GroupId"])
                        asciiForm += self._buildLineSubItem(margin,"    Group Name", sg["GroupName"])
                     line       = margin + LATERAL + Style.BLUE + "       HEALTH" + Style.RESET
                     asciiForm += line + self._calculateRemainingSpace(line) + LATERAL + "\n"
                     asciiForm += self._buildLineSubItem(margin,"    Port", "{}".format(target["health"]["Port"]))
                     asciiForm += self._buildLineSubItem(margin,"    Description", target["health"]["Description"])
                     asciiForm += self._buildLineSubItem(margin,"    Reason", target["health"]["Reason"])
               asciiForm    += margin + LATERAL + " ".ljust(FORM_WIDTH," ") + LATERAL + "\n" 

         if "ResourceRecords" in result["route53"]:
            asciiForm   += lineSeparator
            asciiForm   += lineEmtpy
            asciiForm   += self._buildLine(MARGIN, "  Hosted Zoned Id", result["route53"]["hostedZoneId"])
            totalRecords = len(result["route53"]["ResourceRecords"])
            line         = MARGIN + LATERAL + Style.BLUE + "    RECORDS ({:02d})".format(totalRecords) + Style.RESET
            asciiForm   += line + self._calculateRemainingSpace(line) + LATERAL + "\n" 
            for records in result["route53"]["ResourceRecords"]:
               asciiForm += self._buildLineSubItem(MARGIN,"  Value", "{}".format(records["Value"]))
            asciiForm    += lineEmtpy

         asciiForm += lineSeparator
         return asciiForm

    def _buildSummaryForm(self, dnsName, result):
         asciiForm     = ""
         lineSeparator = MARGIN + CROSSROAD + LINE.ljust(FORM_WIDTH, LINE) + CROSSROAD + "\n"
         lineEmtpy     = MARGIN + LATERAL + " ".ljust(FORM_WIDTH," ") + LATERAL + "\n" 
         asciiForm    += lineSeparator
         asciiForm    += lineEmtpy                    
         # DNS Name Seeked
         line           = MARGIN_CONN1 + LATERAL + Style.IYELLOW + "  " + dnsName + Style.RESET
         asciiForm     += line + self._calculateRemainingSpace(line) + LATERAL + "\n"
         lineEmtpy2     = MARGIN_CONN2 + LATERAL + " ".ljust(FORM_WIDTH," ") + LATERAL + "\n" 
         asciiForm     += lineEmtpy2
         lineSeparator2 = MARGIN_CONN2 + CROSSROAD + LINE.ljust(FORM_WIDTH, LINE) + CROSSROAD + "\n"
         asciiForm     += lineSeparator2
         # Route 53
         asciiForm    += self._buildHeader(MARGIN_CONN3, "ROUTE R53")
         asciiForm    += lineSeparator2
         asciiForm    += lineEmtpy2
         asciiForm    += self._buildLine(MARGIN_CONN2, "DNS Name", result["route53"]["AliasTarget"]["DNSName"])
         asciiForm    += lineEmtpy2
         asciiForm    += lineSeparator2
         # ELB
         asciiForm    += self._buildHeader(MARGIN_CONN3, "ELB")
         asciiForm    += lineSeparator2
         asciiForm    += lineEmtpy2
         asciiForm    += self._buildLine(MARGIN_CONN2, "Name", result["elb"]["LoadBalancerName"])
         asciiForm    += lineEmtpy2
         
         asciiForm      += lineSeparator2
         margin          = MARGIN_CONN2
         idxTargetGroups = len(result["targetGroup"])
         # TARGET GROUPS
         asciiForm    += self._buildHeader(MARGIN_CONN3, "TARGET GROUPS ({:02d})".format(idxTargetGroups))
         asciiForm    += lineSeparator2
         index = 0
         for targetGroup in result["targetGroup"]:
            index += 1
            if index == idxTargetGroups:
               margin = MARGIN
            asciiForm    += self._buildHeader(MARGIN_CONN3, "TARGET GROUP ({:02d})".format(index))
            asciiForm += self._buildLine(margin, "\033[37m•\033[94m Name", targetGroup["TargetGroupName"]) 
            
            totalTargets = len(targetGroup["Targets"])
            asciiForm += self._addLine(margin, Style.BLUE + "    TARGETS ({:02d})".format(totalTargets) + Style.RESET) 
            for target in targetGroup["Targets"]:
                  asciiForm += self._buildLineSubItemHighlighted(margin,"\033[37m•\033[94m Instance Id", target["Id"])
                  asciiForm += self._buildLineSubItem(margin,"  Port", "{}".format(target["Port"]))
                  asciiForm += self._buildLineSubItem(margin,"  Private IP", target["PrivateIpAddress"])
                  asciiForm += self._buildLineSubItem(margin,"  State", target["State"]["Name"])
            asciiForm    += margin + LATERAL + " ".ljust(FORM_WIDTH," ") + LATERAL + "\n" 

         asciiForm += lineSeparator
         return asciiForm     

    def _builAsciiGraph(self, dnsName, result):
        pygraph = PyAsciiGraphs()
        leafR53 = Leaf(dnsName)
        leafELB = Leaf("ELB: " + result["elb"]["LoadBalancerName"])
        leafR53.add(leafELB)
        for targetGroup in result["targetGroup"]:
            leafTargetGroup = Leaf(targetGroup["TargetGroupName"])
            for target in targetGroup["Targets"]:
                leafTarget = Leaf(target["Id"])
                leafTargetGroup.add(leafTarget)
            leafELB.add(leafTargetGroup)
               
        pygraph.drawTree(leafR53)

    def _buildHeader(self, margin, label):
        line  = margin + LATERAL + "  " + Style.GREEN + label + Style.RESET
        spaces        = self._calculateRemainingSpace(line) 
        return line + spaces + LATERAL + "\n"

    def _buildLineSubItemHeader(self, margin, label, value):
        suffix = ".".ljust((FIELD_SIZE-3) - len(Utils.removeCharsColors(label)),".") + ": "
        line = MARGIN_CONN2 + LATERAL + "   " + "• " + Style.IBLUE + label + Style.RESET + suffix + Style.GREEN + value + Style.RESET
        return line + self._calculateRemainingSpace(line) + LATERAL + "\n"
    def _buildLineSubItem(self, margin, label, value):
        suffix = ".".ljust((FIELD_SIZE-3) - len(Utils.removeCharsColors(label)),".") + ": "
        line = margin + LATERAL + "   " + "  " + Style.IBLUE + label + Style.RESET + suffix + Style.GREEN + value + Style.RESET
        return line + self._calculateRemainingSpace(line) + LATERAL + "\n"
    def _buildLineSubItemHighlighted(self, margin, label, value):
        suffix = ".".ljust((FIELD_SIZE-3) - len(Utils.removeCharsColors(label)),".") + ": "
        line = margin + LATERAL + "   " + "  " + Style.IBLUE + label + Style.RESET + suffix + Style.IYELLOW + value + Style.RESET
        return line + self._calculateRemainingSpace(line) + LATERAL + "\n"    

    def _buildLineSubItemHeaderSecondLevel(self, margin, label, value):
        suffix = ".".ljust((FIELD_SIZE-6) - len(Utils.removeCharsColors(label)),".") + ": "
        line = margin + LATERAL + "    " + "  • " + Style.IBLUE + label + Style.RESET + suffix + Style.GREEN + value + Style.RESET
        return line + self._calculateRemainingSpace(line) + LATERAL + "\n"        
    def _buildLineSubItemHeaderSecondLevelTitle(self, margin, label):
        line = margin + LATERAL + "    " + "  • " + Style.BLUE + label + Style.RESET
        return line + self._calculateRemainingSpace(line) + LATERAL + "\n"            
    def _buildLineSubItemSecondLevel(self, margin, label, value):
        suffix = ".".ljust((FIELD_SIZE-6) - len(Utils.removeCharsColors(label)),".") + ": "
        line = margin + LATERAL + "    " + "    " + Style.IBLUE + label + Style.RESET + suffix + Style.GREEN + value + Style.RESET
        return line + self._calculateRemainingSpace(line) + LATERAL + "\n"

    def _buildLine(self, margin, label, value):
        if label:
           suffix = ".".ljust(FIELD_SIZE - len(Utils.removeCharsColors(label)),".") + ": "
           line  = margin + LATERAL + "  " + Style.IBLUE + label + Style.RESET + suffix + Style.GREEN + value + Style.RESET 
        else:  
           line  = margin + LATERAL + "  " + Style.GREEN + value + Style.RESET 
        spaces = self._calculateRemainingSpace(line) 
        return line + spaces + LATERAL + "\n"

    def _addLine(self,margin,line):
        spaces = self._calculateRemainingSpace(margin + LATERAL + line)
        return margin + LATERAL + line + spaces + LATERAL + "\n"
    def _calculateRemainingSpace(self, line):
        spaces = (len(MARGIN) + len(LATERAL) + FORM_WIDTH) - len(Utils.removeCharsColors(line))
        return " ".ljust(spaces, " ")

    # Find the route to reach to a EC2(s)
    #  - Inspect if has Public access (DNS / PublicIP )
    #  - Added in TargetGroups (InstanceId or IP) --> Get the ELB point to this Target Group
    #  - Search in Route53 for Public/Private registers pointing to its Private/Public IP or reaching to it using ELB/TargetGroups
    def findRouteEc2s(self):
       ec2Client = self.botoSession().client('ec2')
       tableArgs   = TableArgs()
       tableArgs.setArguments(self.config.commandArguments)

       def _print_there(x, y, text):
          sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x, y, text))
          sys.stdout.flush()

       instancesToQuery = []
       if "," in self.config.commandArguments:
          for arg in self.config.commandArguments.split(","):
              if "i-" in arg:
                 instancesToQuery.append(arg)
       else:
          instancesToQuery.append(self.config.commandArguments)

       report         = "\n"
       data           = {}
       data["result"] = []
       filters        = []
       lineMsg        = 3

       filters.append({'Name': 'instance-id','Values': instancesToQuery})
       reservations = ec2Client.describe_instances( Filters=filters )
       if len(reservations) < 1:
          report = "Instance(s) {} was not found".format(instancesToQuery)
          return data, report

       #print(Utils.dictToJson(reservations))
       # Collect the EC2 Instances to "find the route"
       msg = "\033[32mRetrieving EC2 Instances information...                                     \033[0m"
       _print_there(lineMsg, 1, msg)  
       for instanceGroup in reservations["Reservations"]:
          for instance in instanceGroup["Instances"]:
            
             name = None
             for t in instance["Tags"]:
                if t["Key"].lower() == "name":
                   name = t["Value"]
                   break

             routes = []

             # Check if not Publicly Exposed (IP)
             if "PublicDnsName" in instance and instance["PublicDnsName"] != "":
                routes.append({
                  "routeType": "PUBLIC_IP_ADDRESS",
                  "publicDnsEc2": instance["PublicDnsName"],
                  "route53": {
                     "hostedZoneId": None,
                     "hostedZoneName": None,
                     "privateZone": None,
                     "record": {
                        "resourceName":None,
                        "type": None,
                        "target": instance["PublicDnsName"],
                     }
                  }
                })

             data["result"].append({
               "instanceId":      instance["InstanceId"],
               "instanceType":      instance["InstanceType"],
               "privateIpAddress":instance["PrivateIpAddress"],
               "privateDnsName":  instance["PrivateDnsName"],
               "publicDnsName":   instance["PublicDnsName"] if "PublicDnsName" in instance else None,
               "publicIpAddress": instance["PublicIpAddress"] if "PublicIpAddress" in instance else None,
               "name": name,
               "routes": routes
               #"tags": instance["Tags"],
            })

       def retrieveEc2ByInstanceId(instanceId):
          myEc2List = iter(data["result"])
          return next((item for item in myEc2List if item["instanceId"] == instanceId), None)
            
       def retrieveEc2ByType(typeInstance):
          myEc2List = iter(data["result"])
          listFound = []
          found = next((item for item in myEc2List if typeInstance in item["instanceType"]), None)
          while found:
             listFound.append(found)
             found = next((item for item in myEc2List if typeInstance in item["instanceType"]), None)  
          return listFound
      
       # Look TargetGroups related to the EC2 Instances
       elbv2 = self.botoSession().client('elbv2')
       target_groups = elbv2.describe_target_groups()
       loadBalancersToQuery = []
       msg = "\033[32mRetrieving Target Groups with EC2 Instances...                                     \033[0m"
       _print_there(lineMsg, 1, msg)  
       lineMsg     += 1
       lineMsgFound = lineMsg
       for tg in target_groups['TargetGroups']:
          targetsHealth = elbv2.describe_target_health(TargetGroupArn=tg["TargetGroupArn"])
          msg = "\033[32mChecking EC2 Instances at Target Group \033[94m{}\033[32m...                    \033[0m".format(tg["TargetGroupName"])
          _print_there(lineMsg, 1, msg)
          for targetHealthDescription in targetsHealth["TargetHealthDescriptions"]:
             if targetHealthDescription["Target"]["Id"] in instancesToQuery:
                lineMsgFound += 1
                msgFound = " \033[94m-->\033[93m Found \033[32mEC2 Instance \033[94m{}\033[32m at TARGET GROUP \033[94m{}\033[32m\033[0m".format(targetHealthDescription["Target"]["Id"],tg["TargetGroupName"])
                _print_there(lineMsgFound, 1, msgFound)  
                instanceIdFound =  targetHealthDescription["Target"]["Id"]
                
                """ print(targetHealthDescription["Target"]["Id"])
                print(tg)
                print(targetsHealth)
                print(targetHealthDescription) """

                loadBalancers = []
                elbsFound     = ""
                if len(tg['LoadBalancerArns']) > 0:
                   for loadBalancerArn in tg['LoadBalancerArns']:
                       arnELB   = arnparse(loadBalancerArn)
                       loadBalancers.append({
                          "arn": loadBalancerArn,
                          "elb": arnELB.resource,
                          "info": None,
                       })
                       elbsFound += " " + arnELB.resource
                       loadBalancersToQuery.append(loadBalancerArn)
                
                msg = msgFound.strip() + "\033[32m at ELB\033[94m{}\033[32m".format(elbsFound)
                report += msg + "\n"
                _print_there(lineMsgFound, 1, msg)
               
                ec2Instance = retrieveEc2ByInstanceId(instanceIdFound)
                route = {
                   "routeType": "TARGET_GROUP",
                   "targetType": tg['TargetType'],
                   "protocol": tg['Protocol'],
                   "port": tg['Port'],
                   "targetGroupName": tg['TargetGroupName'],
                   "targetGroupArn": tg['TargetGroupArn'],
                   "loadBalancers": loadBalancers,
                  ## In case need Health Info, add this
                  #  "health":{
                  #     "healthCheckProtocol":tg["HealthCheckProtocol"],
                  #     "healthCheckPath": tg["HealthCheckPath"],
                  #     "healthCheckPort": tg["HealthCheckPort"],
                  #     "healthCheckEnabled": tg["HealthCheckEnabled"],
                  #     "healthCheckIntervalSeconds": tg["HealthCheckIntervalSeconds"],
                  #     "healthCheckTimeoutSeconds": tg["HealthCheckTimeoutSeconds"],
                  #  }
                }
                ec2Instance["routes"].append(route)
      
       def addELBInfoByArn(elbArn, elbInfo):
          for inst in data["result"]:
             for route in inst["routes"]:
                if "loadBalancers" in route:
                  for elb in route["loadBalancers"]:
                     if elbArn == elb["arn"]:
                        elb["info"] = elbInfo

       lineMsg = lineMsgFound + 2
       # Look ELBs related to the EC2 Instances to get their data (TargetGroups where the EC2 Instances were found)
       load_balancers = elbv2.describe_load_balancers(LoadBalancerArns=loadBalancersToQuery)
       for loadBalancer in load_balancers["LoadBalancers"]:
          elbInfo = {
            "dnsName": loadBalancer["DNSName"],
            "canonicalHostedZoneId": loadBalancer["CanonicalHostedZoneId"],
            "loadBalancerName": loadBalancer["LoadBalancerName"],
            "scheme": loadBalancer["Scheme"],
            "type": loadBalancer["Type"],
            "availabilityZones": loadBalancer["AvailabilityZones"],
            "securityGroups": loadBalancer["SecurityGroups"] if "SecurityGroups" in loadBalancer else [],
            "ipAddressType": loadBalancer["IpAddressType"],
          }
          addELBInfoByArn(loadBalancer["LoadBalancerArn"], elbInfo)
       
       # Look through all Route53 records, registers that point to EC2 directly, or via ELB DNSNames
       r53api = self.botoSession().client('route53')
       hostedZones = r53api.list_hosted_zones_by_name()
       for hostedZone in hostedZones["HostedZones"]:

          hostedZoneId   = hostedZone["Id"]
          privateZone    = hostedZone["Config"]["PrivateZone"]
          hostedZoneName = hostedZone["Name"]
         
          nextRecordName = None
          nextRecordType = None
          recordsSets    = r53api.list_resource_record_sets(HostedZoneId=hostedZoneId)
          # Multiple Pages?
          if "IsTruncated" in recordsSets and recordsSets["IsTruncated"] == True:
             nextRecordName = recordsSets["NextRecordName"]
             nextRecordType = recordsSets["NextRecordType"]
          page = 1
          msg = "\033[32mSearching ELBs / IP Addresses related to EC2 Instances in Route 53 Records of \033[94m{}...                                                       \033[0m".format(hostedZoneName)
          report += msg + "\n"
          _print_there(lineMsg,   1, msg)  
          msg = "\033[32m--> Page \033[94m{}\033[0m".format(page) + " ".ljust(80," ") 
          _print_there(lineMsg+1, 1, msg)
          while recordsSets and len(recordsSets["ResourceRecordSets"]) > 0:
             for resource in recordsSets["ResourceRecordSets"]:
                targets = []
                if resource["Type"] == "A" or resource["Type"] == "CNAME" or resource["Type"] == "AAAA":
                   if "ResourceRecords" in resource:
                      for resourceRecord in resource["ResourceRecords"]:
                         targets.append(resourceRecord["Value"])
                   if "AliasTarget" in resource:
                      targets.append(resource["AliasTarget"]["DNSName"])
                   
                   for tgt in targets:
                      # Look for Target in ELB Load Balancers pointing to EC2 Instances (via Target Groups)
                      for inst in data["result"]:
                        for route in inst["routes"]:
                           if "loadBalancers" in route:
                              for elb in route["loadBalancers"]:
                                 if elb["info"]["dnsName"] in tgt:
                                    lineMsg += 1
                                    msg = "\033[94m-->\033[93m Found \033[32mELB \033[94m{}\033[32m at Route 53 Record \033[94m{}\033[32m\033[0m                                          ".format(elb["elb"],resource["Name"])
                                    report += msg + "\n"
                                    _print_there(lineMsg, 1, msg)
                                    elb["route53"] = {
                                       "hostedZoneId": hostedZoneId,
                                       "hostedZoneName": hostedZoneName,
                                       "privateZone": privateZone,
                                       "record": {
                                          "resourceName":resource["Name"],
                                          "type": resource["Type"],
                                          "target": tgt,
                                       }
                                    }
                                    """ print(hostedZoneName, " - ", resource["Name"])
                                    print(resource)
                                    print("\033[32m",tgt,"FOUND","\033[0m") """
                                    continue

                      # Look for Target using the EC2 Instances Private IP Address
                      for inst in data["result"]:
                        if inst["privateIpAddress"] == tgt:
                           lineMsg += 1
                           msg = "\033[94m-->\033[93m Found \033[32mPrivate IP Address \033[94m{}\033[32m at Route 53 Record \033[94m{}\033[32m\033[0m                                          ".format(tgt,resource["Name"])
                           report += msg + "\n"
                           _print_there(lineMsg, 1, msg)
                           inst["routes"].append({
                              "routeType": "PRIVATE_IP_ADDRESS",
                              "route53": {
                                 "hostedZoneId": hostedZoneId,
                                 "hostedZoneName": hostedZoneName,
                                 "privateZone": privateZone,
                                 "record": {
                                    "resourceName":resource["Name"],
                                    "type": resource["Type"],
                                    "target": tgt,
                                 }
                              }
                           })
                           continue

             if nextRecordName:
                 page += 1
                 msg = "\033[32m--> Page \033[94m{}\033[0m".format(page) + " ".ljust(80," ") 
                 lineMsg += 1
                 _print_there(lineMsg, 1, msg)
                 recordsSets = r53api.list_resource_record_sets(HostedZoneId=hostedZoneId,StartRecordName=nextRecordName,StartRecordType=nextRecordType)  
                 # More Pages?
                 if "IsTruncated" in recordsSets and recordsSets["IsTruncated"] == True:
                    nextRecordName = recordsSets["NextRecordName"]
                    nextRecordType = recordsSets["NextRecordType"]
                 else:
                    nextRecordName = None
                    nextRecordType = None
             else:
                 break

       return data, report
    
    def findRouteEc2sPrintResult(self, data, args):
       resultTxt       = ""
       showTargetGroup = False
       showLabelName   = False
       tableArgs       = TableArgs()
       tableArgs.setArguments(args)

       if "target-group" in args:
          showTargetGroup = True
       if "label-name" in args:
          showLabelName = True

       header = ["#","Instance Id", "Route Type", "Target (ELB / IP Address)", "R53 DNS Name", "R53 Visibility", "R53 Type"] 
       if showTargetGroup and showLabelName:
          headerB = header[:]
          headerB.insert(2,"Label Name")
          headerB.insert(4,"Target Group")
          header = headerB
       elif showTargetGroup:   
          headerB = header[:]
          headerB.insert(3,"Target Group")
          header = headerB
       elif showLabelName:
          headerB = header[:]
          headerB.insert(2,"Label Name")
          header = headerB
       
       prettyTable = PrettyTable(header)

       def addColumn():
          index = 0
          if len(instanceId) > sizeColumns[index]:
             sizeColumns[index] =  len(instanceId)
          if showLabelName:
             index += 1
             if len(labelName) > sizeColumns[index]:
               sizeColumns[index] = len(labelName)   
          index += 1
          if len(routeType) > sizeColumns[index]:
             sizeColumns[index] = len(routeType)
          if showTargetGroup:
            index += 1 
            if len(Utils.removeCharsColors(targetGroup)) > sizeColumns[index]:
               sizeColumns[index] = len(Utils.removeCharsColors(targetGroup))
          index += 1 
          if len(labelTarget) > sizeColumns[index]:
             sizeColumns[index] = len(labelTarget)
          index += 1   
          if len(r53Name) > sizeColumns[index]:
             sizeColumns[index] = len(r53Name)
          index += 1   
          if len(r53Visib) > sizeColumns[index]:
             sizeColumns[index] = len(r53Visib)
          index += 1   
          if len(r53Type) > sizeColumns[index]:
             sizeColumns[index] = len(r53Type)

          if showLabelName and showTargetGroup:
             columns = [ idx, instanceId, labelName, routeType, targetGroup, labelTarget, r53Name, r53Visib, r53Type ]
          elif showTargetGroup:
             columns = [ idx, instanceId, routeType, targetGroup, labelTarget, r53Name, r53Visib, r53Type ]
          elif showLabelName:
             columns = [ idx, instanceId, labelName, routeType, labelTarget, r53Name, r53Visib, r53Type ]   
          else:
             columns = [ idx, instanceId, routeType, labelTarget, r53Name, r53Visib, r53Type ]
          prettyTable.addRow(columns)

       idx         = 0
       sizeColumns = []
       for i,h in enumerate(header):
          if i > 0:
             sizeColumns.append(0)
       for instance in data["result"]:
          idx += 1
          instanceId  = instance["instanceId"]
          labelName   = instance["name"]

          labelTarget = ""
          r53Name     = ""
          r53Type     = ""
          r53Visib    = ""
          labelPublic = ""
          targetGroup = ""
          routeType   = ""

          if len(instance["routes"]) < 1:
            routeType   = "Not found"
            addColumn() 
          else:
            for route in instance["routes"]:
               targetGroup = ""
               routeType   = "NOT TRANSLATED - Check it!"
               if route["routeType"] == "TARGET_GROUP":
                  routeType   = "Load Balancer"
                  targetGroup = "{name} \033[36m-->\033[32m {protocol}:{port}".format(protocol=route["protocol"],port=route["port"],name=route["targetGroupName"]) 
               elif route["routeType"] == "PRIVATE_IP_ADDRESS":
                  routeType = "Private IP"
               elif route["routeType"] == "PUBLIC_IP_ADDRESS":
                  routeType = "Public IP"  

               labelTarget = ""
               r53Name     = ""
               r53Type     = ""
               r53Visib    = ""
               labelPublic = "\033[94mPUBLIC\033[32m"
               if "loadBalancers" in route:
                  for elb in route["loadBalancers"]:
                     labelTarget = elb["elb"]
                     if "route53" in elb:
                        r53Name  = elb["route53"]["record"]["resourceName"]
                        r53Type  = elb["route53"]["record"]["type"]
                        r53Visib = "PRIVATE" if elb["route53"]["privateZone"] == True else labelPublic
                        if elb["route53"]["privateZone"] == False:
                           r53Name  = "\033[94m" + r53Name + "\033[32m"
                     addColumn()
               elif route["routeType"] == "PUBLIC_IP_ADDRESS" and route["route53"]["hostedZoneName"] == None:
                  labelTarget = "\033[94m" + route["publicDnsEc2"] + "\033[32m"
                  r53Name     = "-----------"
                  r53Type     = "---"
                  r53Visib    = "-----------"
                  addColumn() 
               else:
                  labelTarget = route["route53"]["record"]["target"]
                  r53Name     = route["route53"]["record"]["resourceName"]
                  r53Type     = route["route53"]["record"]["type"]
                  r53Visib    = "PRIVATE" if route["route53"]["privateZone"] == True else labelPublic
                  if route["route53"]["privateZone"] == False:
                     r53Name  = "\033[94m" + r53Name + "\033[32m"
                  addColumn()  
          
          #Separator Instances
          colsSep = []
          colsSep.append(idx)
          for cl in sizeColumns:
             colsSep.append("-".ljust(int(cl),"-"))
          prettyTable.addRow(colsSep)
      
       #resultTxt = resultTxt + "\n\n Total of EC2s...: " + Style.GREEN + format(totalListed,",") + Style.RESET   

       tableArgs.sortCol = "1"
       prettyTable.sortByColumn(int(tableArgs.sortCol) - 1)
       prettyTable.ascendingOrder(not tableArgs.desc)

       if not prettyTable.isEmpty():
          result = resultTxt + "\n" + prettyTable.printMe("findRouteEc2s",self.config.tableLineSeparator, tableArgs)
          return Utils.formatResult(Functions.FUNCTIONS[Functions.FIND_ROUTE_EC2]["name"], result, self.config, Utils.dictToJson(data), True, tableArgs, shortName=Functions.FUNCTIONS[Functions.FIND_ROUTE_EC2]["shortName"])
       else:
          return "Nothing was found!"

    def botoSession(self):
        return self.config.botoSession()

if __name__ == '__main__':
    config = Config()
    config.awsProfile   = "ecomm"
    config.awsRegion    = "eu-central-1"
    config.printResults = True
    #config.awsTags["Environment"] = "production"
    config.tableLineSeparator = False
    
    # python pyr53cp.py services.preprod.aps2.aws.emagin.eu

    # aws elbv2 describe-rules --listener-arn arn:aws:elasticloadbalancing:eu-central-1:659915611011:listener/app/tf-lb-20200529110151957200000006/4d10ad47be839fbf/ef91534c7811e537 --profile ecomm --region eu-central-1env
    if len(sys.argv) > 1:
       config.commandArguments = sys.argv[1]
    pyr53CP = PyR53CP(config)
    report = pyr53CP.nslookupEc2R53()
    if report: 
       Utils.addToClipboard(report)
       print(report)

