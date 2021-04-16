from autosync import lib
import copy
from meraki.exceptions import AsyncAPIError

class GetAttr(type):
    def __getitem__(cls, x):
        return getattr(cls, x)
class switch(object):
    def __init__(self):
        self.NetworkSwitchMtu = None
        self.NetworkSwitchSettings = 'Test'
        self.NetworkSwitchDscpToCosMappings = None
        self.NetworkSwitchRoutingMulticast = None
        self.NetworkSwitchAccessControlLists = None
        self.NetworkSwitchStormControl = None
        self.NetworkSwitchQosRules = None
        self.NetworkSwitchQosRulesOrder = None
        self.ReSync = False
    def settings(self):
        skip =  ['ReSync']
        items = [ i for i in self.__dict__.keys() if i not in skip]
        return items

    async def Update_NetworkSwitchAccessControlLists(self, master,
                                                     appcfg,
                                                     db, net_id, task,
                                                     netName):
        if not await lib.compare(master.NetworkSwitchAccessControlLists,
								 self.NetworkSwitchAccessControlLists):
            if appcfg.WRITE:
                acls = copy.deepcopy(
                        master.NetworkSwitchAccessControlLists)
                acls['rules'].remove(acls['rules'][len(acls[
                                                           'rules']) - 1])  # remove the default rule at the end
                self.ReSync = True
                print(
                        f'\t {lib.bc.OKGREEN}-Updating Switch ACL rules...{lib.bc.ENDC}')
                await db.switch.updateNetworkSwitchAccessControlLists(
                        net_id, **acls)
        else:
            print(
                    f'\t{lib.bc.OKBLUE} {netName} {lib.bc.OKGREEN}-Settings for  {task} Matched Master{lib.bc.ENDC}')

    async def Update_NetworkSwitchQosRules(self, master, appcfg, db,
                                           net_id, task, netName):
        if not await lib.soft_compare(master.NetworkSwitchQosRules,
									  self.NetworkSwitchQosRules):
        
            # {'ruleIds': ['577586652210270187', '577586652210270188', '577586652210270189']}
            rOrder_src = master.NetworkSwitchQosRules
            rOrder_dst = self.NetworkSwitchQosRules
            qosRuns = 0
            for rid in rOrder_src:
                for rid2 in rOrder_dst:
                    if rid['vlan'] is None or rid['vlan'] == rid2['vlan']:
                        if rid['protocol'] is None or rid['protocol'] == \
                                rid2['protocol']:
                            if rid['srcPort'] is None or rid['srcPort'] == \
                                    rid2['srcPort']:
                                if rid['dstPort'] is None or rid[
                                    'dstPort'] == rid2['dstPort']:
                                    if rid['dstPort'] is None or rid[
                                        'dscp'] == rid2['dscp']:
                                        continue
            
                ##	# print(f'Duplicate rule, skipping!')
                #		continue
                if qosRuns == 0:
                    qosRuns += 1
                    print(
                        f'\t{lib.bc.OKGREEN}-Cloning Switch QoS Rules...')
                # [{'id': '577586652210270187','vlan': None,'protocol': 'ANY','srcPort': None,'dstPort': None,'dscp': -1}, .. ]
                for r in master.NetworkSwitchQosRules:
                    if r['id'] == rid['id']:
                        rule = copy.deepcopy(r)
                        # try:
                        # pop the id, and srcPort/dstPort if they're empty, otherwismne it'll throw an error
                        rule.pop('id')
                        if rule['srcPort'] is None: rule.pop('srcPort')
                        if rule['dstPort'] is None: rule.pop('dstPort')
                        try:
                            if appcfg.WRITE:
                                await db.switch.reateNetworkSwitchQosRule(
                                        net_id, **rule)
                                print(
                                        f'\t\t{lib.bc.OKGREEN}-Rule Created[{lib.bc.WARNING}{rule}{lib.bc.OKGREEN}]')
                        except AsyncAPIError as e:
                            print(
                                f'\t {lib.bc.FAIL} Error running api: {lib.bc.WARNING} {str(e)}{lib.bc.Default}')
                    # except Exception as e:
                    #    print(
                    #            f'\t\t{lib.bc.OKGREEN}-Rule already exists{lib.bc.ENDC} print Error: {str(e)}')
                    else:
                        print(
                            f'{lib.bc.FAIL}ERROR FINDING QoS RULE!!!{lib.bc.ENDC}')
    
        else:
            print(
                    f'\t{lib.bc.OKBLUE} {netName} {lib.bc.OKGREEN}-Settings for  {task} Matched Master{lib.bc.ENDC}')

