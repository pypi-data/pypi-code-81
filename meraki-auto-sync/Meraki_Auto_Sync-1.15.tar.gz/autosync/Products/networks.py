from autosync import lib
import copy
from autosync.mnetutils.ReSync import reSYNC

class GetAttr(type):
    def __getitem__(cls, x):
        return getattr(cls, x)

class networks(object):
    __metaclass__ = GetAttr
    
    # Dashboard Network Settings
    def __init__(self):
        self.Network = 'Test'
        self.NetworkAlertsSettings = None
        self.NetworkGroupPolicies = None
        self.NetworkTrafficAnalysis = None
        self.NetworkSyslogServers = None
        self.NetworkSnmp = None
        self.NetworkWebhooksHttpServers = None
        self.ReSync = False
    
    def settings(self):
        """
        
        Returns:
            Settings to cycle through when updating configurate
        """
        skip =  ['ReSync'] # Settings to skip
        items = [ i for i in self.__dict__.keys() if i not in skip]
        return items

    async def Update_Network(self, master: object,
                                          appcfg: object, db: object,
                                          net_id: str, task, netName):
       #"No Seetins to Update here from master"
       pass
            
    async def Update_NetworkSyslogServers(self, master: object,
                                          appcfg: object, db: object,
                                          net_id: str, task, netName):
        """
        Compaires Network Syslog Servers Configuration to Master and Updates
        Configuration if anything changes on target network
        Args:
            netName:
            task:
            master(Object): Current Master COnfiguration Object
            appcfg(Object): Applaciton configuration object
            db(object): Meraki SDK Object
            net_id(str): Network ID

        Returns:
            Nothing Updates meraki Dashbioard
        """
        ## Clone Syslog Settings
        if not await lib.compare(master.NetworkSyslogServers['servers'],
								 self.NetworkSyslogServers['servers']):
        
            # kinda works.... will trigger "change" if the 'roles' are unordered
            if appcfg.WRITE:
                print(
                        f'\t{lib.bc.OKGREEN}Updating Syslog Settings in network {lib.bc.WARNING}{lib.bc.ENDC}')
                self.ReSync = True
                await db.networks.updateNetworkSyslogServers(net_id,
                                                    **{'servers': []})
                await db.networks.updateNetworkSyslogServers(net_id,
                                                    **master.NetworkSyslogServers)
        else:
            print(
                    f'\t{lib.bc.OKBLUE} {netName} {lib.bc.OKGREEN}-Settings for  {task} Matched Master{lib.bc.ENDC}')
        if self.ReSync or not appcfg.CLEAN:
            await  reSYNC(db, net_id, self, 'NetworkSyslogServers'
                          , 'networks', appcfg)
            appcfg.CLEAN = True
            self.ReSync = True
        ## / end-Syslog Settings

    async def Update_NetworkWebhooksHttpServers(self,
                                                master: object,
                                                appcfg: object, db: object,
                                                net_id: str, task,
                                                netName):
        """
            Compaires Network WebHook Configuration to Master and Updates
            Configuration if anything changes on target network
            Args:
                netName:
                task:
                master(Object): Current Master COnfiguration Object
                appcfg(Object): Applaciton configuration object
                db(object): Meraki SDK Object
                net_id(str): Network ID

            Returns:
                Nothing Updates meraki Dashbioard
            """
        # Webhooks
        if not await lib.compare(master.NetworkWebhooksHttpServers,
								 self.NetworkWebhooksHttpServers):
            curr_list = []
            for cwh in self.NetworkWebhooksHttpServers:
                curr_list.append(cwh['name'])
            for mwh in master.NetworkWebhooksHttpServers:
                if not mwh['name'] in curr_list:
                    if appcfg.WRITE:
                        print(
                            f'\t\t{lib.bc.OKBLUE}-Webhook {lib.bc.WARNING}{mwh["name"]}{lib.bc.ENDC}')
                        self.ReSync = True
                        mwh_tmp = copy.deepcopy(mwh)
                        mwh_tmp.pop('networkId')
                        await db.networks.createNetworkWebhooksHttpServer(
                                net_id, **mwh_tmp)
        else:
            print(
                    f'\t{lib.bc.OKBLUE} {netName} {lib.bc.OKGREEN}-Settings for  {task} Matched Master{lib.bc.ENDC}')
        if self.ReSync or not appcfg.CLEAN:
            await  reSYNC(db, net_id, self,
                          'NetworkWebhooksHttpServers', 'networks', appcfg)
            appcfg.CLEAN = True
            self.ReSync = False

    async def Update_NetworkGroupPolicies(self,
                                          master: object,
                                          appcfg: object,
                                          db: object,
                                          net_id: str, task, netName):
        """
        Compaires Network Group Policy Configuration to Master and Updates
        Configuration if anything changes on target network
        Args:
            netName:
            task:
            master(Object): Current Master COnfiguration Object
            appcfg(Object): Applaciton configuration object
            db(object): Meraki SDK Object
            net_id(str): Network ID

        Returns:
            Nothing Updates meraki Dashbioard
                """
        # Group Policies
        # TODO Move this to Batch Action Could be faster
    
        for master_gp in master.NetworkGroupPolicies:
            tempGP = copy.deepcopy(master_gp)
            tempGP.pop('groupPolicyId')
            if appcfg.WRITE:
                local_gp = await lib.idFromName(
                    self.NetworkGroupPolicies,
                    tempGP['name'])
            
                if local_gp is None:
                    print(f'\t\t{lib.bc.OKBLUE}Creating GP Policy named '
                          f'{tempGP["name"]}{lib.bc.ENDC}')
                    self.ReSync = True
                    try:
                        await db.networks.createNetworkGroupPolicy(net_id, **tempGP)
                    except:
                        print(
                            f'{lib.bc.FAIL}ERROR: Cannot create GP policy named {tempGP["name"]}')
            
                else:
                    local_gpid = local_gp['groupPolicyId']
                    tempGP['groupPolicyId'] = local_gpid
                    if not await lib.soft_compare(tempGP,
												  await lib.idFromName(
                                                          master.NetworkGroupPolicies,
                                                          tempGP['name'])):
                        print(
                            f'\t\t{lib.bc.OKBLUE}Updating GP Policy named {tempGP["name"]}{lib.bc.ENDC}')
                        self.ReSync = True
                        await db.networks.updateNetworkGroupPolicy(net_id,
                                                                   **tempGP)
        for localgp in self.NetworkGroupPolicies:
            mastergp = await lib.idFromName(self.NetworkGroupPolicies,
											localgp['name'])
            if mastergp is None:
                print(
                    f't{lib.bc.WARNING}{netName} - {task}\t\t{lib.bc.OKBLUE}Removing GP Policy named {localgp["name"]}{lib.bc.ENDC} not found in Master')
                await db.networks.deleteNetworkGroupPolicy(net_id, localgp['id'])
    
        if self.ReSync or not appcfg.CLEAN:
            await  reSYNC(db, net_id, self, 'NetworkGroupPolicies',
                          'networks', appcfg)
            appcfg.CLEAN = True
            self.ReSync = False


