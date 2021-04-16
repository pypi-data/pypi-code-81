import copy
from autosync import lib



class GetAttr(type):
    def __getitem__(cls, x):
        return getattr(cls, x)


class wireless(object):
    __metaclass__ = GetAttr

    def __init__(self):
        # Dahsboard Wireless Settings
        self.NetworkWirelessSettings = None
        self.NetworkWirelessBluetoothSettings = None
        self.NetworkWirelessRfProfiles = None
        self.ssids_range = []  # should hold array of SSID_IDs, ex. [0,1,2,4,6,7]
        self.NetworkWirelessSsid = []
        self.NetworkWirelessSsidFirewallL3FirewallRules = []
        self.NetworkWirelessSsidFirewallL7FirewallRules = []
        self.NetworkWirelessSsidTrafficShapingRules = []
        self.NetworkWirelessSsidIdentityPsks = []
        self.ReSync = False
        self.hasAironetIE = None
        self.aironetie = None

    def settings(self):
        skip = ['ReSync', 'hasAironetIE', 'ssids_range']
        items = [i for i in self.__dict__.keys() if i not in skip]
        return items

    async def Get_NetworkWirelessSsid(self, db: object, net_id: str,
                                      _appcfg: object):
        ssids = []
        dashabordssids = await db.wireless.getNetworkWirelessSsids(net_id)
        for ssid in dashabordssids:
            ssids.append(ssid)
            if not "Unconfigured SSID" in ssid['name'] \
                    and not ssid['number'] in self.ssids_range:
                self.ssids_range.append(ssid['number'])
        self.NetworkWirelessSsid = ssids
        self.ssids_range

    async def Get_aironetie(self, db: object, net_id: str,
                            _appcfg: object):
        if self.hasAironetIE is None:
            # print(f'Network {name} has aironetIE extensions!!!')
            self.hasAironetIE = False
        # print(f'Network {name} needs aironetIE NFO')
        else:
            self.hasAironetIE = True

        # only do the full refresh if it's been cloned, cloneFrom_MR will set the aironetie = None
        if self.hasAironetIE:
            self.aironetie = []
            for i in range(0, 15):
                if i in self.ssids_range:  # only query/refresh the active SSIDS
                    aie_code = await lib._aironetie(net_id, self, i,
                                                    _appcfg.MERAKI_DASHBOARD_API_KEY)
                    print(
                        f'\t\t\t{lib.bc.OKBLUE}Detecting AIE for SSID[{lib.bc.WARNING}{i}{lib.bc.OKBLUE}] '
                        f'Status[{lib.bc.WARNING}{aie_code}{lib.bc.OKBLUE}]{lib.bc.ENDC}')
                    self.aironetie.append(
                        aie_code)  # -1 for unkown, 0 for off, 1 for
            # self.aironetie
        # self.aironetie

    async def Get_NetworkWirelessSsidFirewallL3FirewallRules(self, db: object,
                                                             net_id: str,
                                                             _appcfg: object):
        ssids_l3 = []
        for ssid_num in range(0, 15):
            if ssid_num in self.ssids_range:
                ssids_l3.append(
                    await
                    db.wireless.getNetworkWirelessSsidFirewallL3FirewallRules(
                        net_id, ssid_num))
            else:
                ssids_l3.append([])
        self.NetworkWirelessSsidFirewallL3FirewallRules = ssids_l3

    async def Get_NetworkWirelessSsidFirewallL7FirewallRules(self, db: object,
                                                             net_id: str,
                                                             _appcfg: object):
        ssids_l7 = []
        for ssid_num in range(0, 15):
            if ssid_num in self.ssids_range:
                ssids_l7.append(
                    await
                    db.wireless.getNetworkWirelessSsidFirewallL7FirewallRules(
                        net_id, ssid_num))
            else:
                ssids_l7.append([])
        self.NetworkWirelessSsidFirewallL7FirewallRules = ssids_l7

    async def Get_NetworkWirelessSsidTrafficShapingRules(self, db: object,
                                                         net_id: str,

                                                         _appcfg: object):
        ssids_ts = []
        for ssid_num in range(0, 15):
            if ssid_num in self.ssids_range:
                ssids_ts.append(
                    await db.wireless.getNetworkWirelessSsidTrafficShapingRules(
                        net_id, ssid_num))
            else:
                ssids_ts.append([])
        self.NetworkWirelessSsidTrafficShapingRules = ssids_ts

    async def Get_NetworkWirelessSsidIdentityPsks(self, db: object, net_id: str,

                                                  _appcfg: object):
        NetworkWirelessSsidIdentityPsks = []
        for ssid_num in range(0, 15):
            if ssid_num in self.ssids_range:
                NetworkWirelessSsidIdentityPsks.append(await
                                                       db.wireless.getNetworkWirelessSsidIdentityPsks(
                                                           net_id,
                                                           ssid_num))
            else:
                NetworkWirelessSsidIdentityPsks.append([])
        self.NetworkWirelessSsidIdentityPsks = NetworkWirelessSsidIdentityPsks

    async def Update_NetworkWirelessSsid(self, master: object,
                                         appcfg: object, db: object,
                                         net_id: str, task, netName):
        """
        Compaires Wireless Network SSID Configuration to Master and Updates
        SSIDs if anything changes on target network
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
        # SSIDS
        # Process all SSIDs
        for i in range(0, 15):
            # Don't process SSIDs that are unconfigured
            if 'Unconfigured SSID' in self.NetworkWirelessSsid[i][
                'name'] \
                    and 'Unconfigured SSID' in \
                    master.NetworkWirelessSsid[i]['name']:
                continue

            if not await lib.soft_compare(master.NetworkWirelessSsid[i],
                                          self.NetworkWirelessSsid[i]):
                # Make a copy of the master SSID.... overrides will be needed to write
                temp_SSID = copy.deepcopy(master.NetworkWirelessSsid[i])
                print(f'\t-{lib.bc.OKBLUE} SSID_Num[{i}] configuring '
                     f'SSID[{master.NetworkWirelessSsid[i]["name"]}] ')

                ###  START OF THE OVERRIDES/EXCEPTIONS
                if 'encryptionMode' in temp_SSID and temp_SSID[
                    'encryptionMode'] == 'wpa-eap':
                    temp_SSID['encryptionMode'] = 'wpa'
                # If the SSID has a single radius server,
                # it'll error if these are set to "None" so pop them
                if 'radiusFailoverPolicy' in temp_SSID and \
                        temp_SSID['radiusFailoverPolicy'] is None:
                    temp_SSID.pop('radiusFailoverPolicy')
                    # temp_SSID['radiusFailoverPolicy'] = 'Allow access'
                if 'radiusLoadBalancingPolicy' in temp_SSID and \
                        temp_SSID['radiusLoadBalancingPolicy'] is None:
                    temp_SSID.pop('radiusLoadBalancingPolicy')
                # this is to fix the case where the "target" network has
                # APvlanTags but the source does not. This wipes the target
                # if the source has no tags.
                if not 'apTagsAndVlanIds' in temp_SSID:
                    temp_SSID['apTagsAndVlanIds'] = []

                if 'radiusServers' in temp_SSID:
                    for rs in temp_SSID['radiusServers']:
                        rs['secret'] = appcfg['RAD_KEYS_ALL']

                if 'radiusAccountingServers' in temp_SSID:
                    for ras in temp_SSID['radiusAccountingServers']:
                        ras['secret'] = appcfg['RAD_KEYS_ALL']

                ### END OF THE OVERRIDES/EXCEPTIONS
                if appcfg.WRITE:
                    if 'name' in temp_SSID:
                        for ssid in appcfg.SSID_SKIP_PSK:
                            if self.NetworkWirelessSsid[i][
                                'name'] == ssid:
                                if 'psk' in temp_SSID:
                                    temp_SSID.pop('psk')
                    #               self.NetworkWirelessSsid[temp_SSID['number']] = \
                    await db.wireless.updateNetworkWirelessSsid(net_id,
                                                                **temp_SSID)
                    self.ReSync = True
                    if self.ReSync or not appcfg.CLEAN:
                        await self.Get_NetworkWirelessSsid(db, net_id,appcfg)
                        appcfg.CLEAN = True
                        self.ReSync = False

            else:
                print(
                    f'\t{lib.bc.OKBLUE} {netName} {lib.bc.OKGREEN}-Settings for  {task} Matched Master{lib.bc.ENDC}')

            # Clone the L3 FW rules

    async def Update_NetworkWirelessSsidFirewallL3FirewallRules(self,
                                                                master: object,
                                                                appcfg: object, db: object, net_id: str, task, netName):
        for ssid in self.NetworkWirelessSsid:
            i = ssid['number']
            if 'Unconfigured SSID' in self.NetworkWirelessSsid[i][
                'name'] or 'Unconfigured SSID' in \
                    master.NetworkWirelessSsid[i]['name']:
                pass
            else:
                if not await lib.compare(
                        self.NetworkWirelessSsidFirewallL3FirewallRules[
                            i],
                        master.NetworkWirelessSsidFirewallL3FirewallRules[
                            i]):
                    # print(f'L3 is not the same')
                    print(f'\t\t-{lib.bc.OKBLUE} Copied L3 rules for SSID['
                         f'{self.NetworkWirelessSsid[i]["name"]}] ')
                    lanAccess = True
                    l3rules = copy.deepcopy(
                        master.NetworkWirelessSsidFirewallL3FirewallRules[
                            i])
                    newL3 = {'rules': []}
                    for rule in l3rules['rules']:
                        if rule['destCidr'] == "Local LAN":
                            if rule['policy'] == "deny":
                                lanAccess = False
                            else:
                                lanAccess = True
                            # pull out the allow Lan Access rule, it's boolean
                            l3rules['rules'].remove(rule)
                        # pull out default rule, always the same
                        if rule['comment'] == "Default rule" \
                                or not rule['destCidr'] == "Local LAN":
                            newL3['rules'].append(rule)

                    # print(f'L3 Rules are {newL3}')
                    newL3['allowLanAccess'] = lanAccess
                    if appcfg.WRITE:
                        self.NetworkWirelessSsidFirewallL3FirewallRules[
                            i] \
                            = await db.wireless.updateNetworkWirelessSsidFirewallL3FirewallRules(
                            net_id, i, **newL3)
                        self.ReSync = True
                        if self.ReSync or not appcfg.CLEAN:
                            await self.Get_NetworkWirelessSsidFirewallL3FirewallRules(
                                db, net_id, appcfg)
                            appcfg.CLEAN = True
                            self.ReSync = False
                else:
                    print(
                        f'\t{lib.bc.OKBLUE} {netName} {lib.bc.OKGREEN}-Settings for  {task} Matched Master{lib.bc.ENDC}')

    async def Update_NetworkWirelessSsidFirewallL7FirewallRules(self,
                                                                master: object,
                                                                appcfg: object, db: object, net_id: str, task, netName):
        # Clone the L7 FW rules
        for ssid in self.NetworkWirelessSsid:
            i = ssid['number']
            if 'Unconfigured SSID' in self.NetworkWirelessSsid[i][
                'name'] \
                    or 'Unconfigured SSID' in \
                    master.NetworkWirelessSsid[i]['name']:
                continue
            if not await lib.compare(
                    self.NetworkWirelessSsidFirewallL7FirewallRules[i],
                    master.NetworkWirelessSsidFirewallL7FirewallRules[i]):
                l7rules = \
                    copy.deepcopy(
                        master.NetworkWirelessSsidFirewallL7FirewallRules[
                            i])
                # print(f'L7 not the same ... cloning')
                print(f'\t\t-{lib.bc.OKBLUE} '
                     f'Copied L7 rules for '
                     f'SSID[{self.NetworkWirelessSsid[i]["name"]}] ')

                if appcfg.WRITE:
                    self.NetworkWirelessSsidFirewallL7FirewallRules[i] = \
                        await db.wireless.updateNetworkWirelessSsidFirewallL7FirewallRules(
                            net_id, i, **l7rules)
                    self.ReSync = True
                    if self.ReSync or not appcfg.CLEAN:
                        await self.Get_NetworkWirelessSsidFirewallL7FirewallRules(
                            db, net_id, appcfg)
                        appcfg.CLEAN = True
                        self.ReSync = False
            else:
                print(
                    f'\t{lib.bc.OKBLUE} {netName} {lib.bc.OKGREEN}-Settings for  {task} Matched Master{lib.bc.ENDC}')
        # Clone the TS Rules

    async def Update_NetworkWirelessSsidTrafficShapingRules(self,
                                                            master: object,
                                                            appcfg: object, db: object, net_id: str, task, netName):
        for ssid in self.NetworkWirelessSsid:
            i = ssid['number']
            if 'Unconfigured SSID' in self.NetworkWirelessSsid[i][
                'name'] \
                    or 'Unconfigured SSID' in \
                    master.NetworkWirelessSsid[i]['name']:
                continue
            if not await lib.compare(
                    self.NetworkWirelessSsidTrafficShapingRules[i],
                    master.NetworkWirelessSsidTrafficShapingRules[i]):
                print(f'\t\t-{lib.bc.OKBLUE} Copied Traffic '
                     f'Shaping rules for SSID[{self.NetworkWirelessSsid[i]["name"]}] ')
                try:
                    TSrules = copy.deepcopy(
                        master.NetworkWirelessSsidTrafficShapingRules[
                            i])
                    if appcfg.WRITE:
                        self.NetworkWirelessSsidTrafficShapingRules[i] \
                            = await db.wireless.updateNetworkWirelessSsidTrafficShapingRules(
                            net_id, i, **TSrules)
                        self.ReSync = True

                        await self.Get_NetworkWirelessSsidTrafficShapingRules(
                            db, net_id, appcfg)
                        appcfg.CLEAN = True
                        self.ReSync = False
                except Exception as e:
                    print(
                        f'\t\t-{lib.bc.FAIL}Failed to update TrafficShaping.'
                        f' Make sure all rules are complete{lib.bc.ENDC} '
                        f'Error Code: {str(e)}')
            else:
                print(
                    f'\t{lib.bc.OKBLUE} {netName} {lib.bc.OKGREEN}-Settings for  {task} Matched Master{lib.bc.ENDC}')
        # this also updates ssids_range

    async def Update_aironetie(self, master: object,
                               appcfg: object, db: object, net_id: str,
                               task, netName):
        for i in self.ssids_range:  # and self.hasAironetIE:
            if 'Unconfigured SSID' in self.NetworkWirelessSsid[i][
                'name'] \
                    or 'Unconfigured SSID' in \
                    master.NetworkWirelessSsid[i]['name']:
                continue
            if self.hasAironetIE and not await lib.compare(
                    self.aironetie[i],
                    master.aironetie[i]):
                if appcfg.WRITE:
                    self.ReSync = True
                    self.setaironetie(net_id, i, master.aironetie[i])
                    print(
                        f'{lib.bc.OKBLUE}\t\tConfiguring AironetIE[{lib.bc.WARNING}'
                        f'{master.aironetie[i]}'
                        f'{lib.bc.OKBLUE}] on SSID[{lib.bc.WARNING}'
                        f'{i}{lib.bc.OKBLUE}]{lib.bc.ENDC}')
                    if self.hasAironetIE:
                        await self.Get_aironetie(net_id, appcfg)
            else:
                print(
                    f'\t{lib.bc.OKBLUE} {netName} {lib.bc.OKGREEN}-Settings for  {task} Matched Master{lib.bc.ENDC}')

    async def Update_NetworkWirelessRfProfiles(self,
                                               master: object,
                                               appcfg: object, db: object,
                                               net_id: str, task, netName):
        """
        Compaires Wireless Network RF Profiles with the Master Configuratio
        and Updates The RF Profile If neede
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
        # RFProfiles - (if it exists and not equal, delete/update. If it doesn't exist, create)
        self_RFPS = copy.deepcopy(self.NetworkWirelessRfProfiles)
        master_RFPS = copy.deepcopy(master.NetworkWirelessRfProfiles)
        if not self_RFPS is None:
            for srfp in self_RFPS:
                srfp.pop('id')
                srfp.pop('networkId')
        if not master_RFPS is None:
            for mrfp in master_RFPS:
                mrfp.pop('id')
                mrfp.pop('networkId')

        if not await lib.compare(self_RFPS,
                                 master_RFPS):  # Profiles are NOT the same
            for masterRF in master.NetworkWirelessRfProfiles:
                for selfRF in self.NetworkWirelessRfProfiles:
                    if masterRF['name'] == selfRF['name']:
                        # print(f'RF Profile[{masterRF["name"]}] FOUND')
                        if not await lib.soft_compare(
                                masterRF,
                                selfRF):  # It's in there but might not be the same
                            print(
                                f'\t{lib.bc.OKBLUE}RF Profile[{lib.bc.WARNING}{masterRF["name"]}{lib.bc.OKBLUE}] !!! Updating RF Profile{lib.bc.ENDC}'
                            )
                            newRF = copy.deepcopy(masterRF)
                            newRF.pop('id')
                            newRF.pop('networkId')
                            newRF.pop('name')
                            newRF['fiveGhzSettings'].pop(
                                'validAutoChannels')
                            newRF['fiveGhzSettings'][
                                'validAutoChannels'] = [
                                36, 40, 44, 48, 52, 56, 60, 64, 100,
                                104,
                                108, 112,
                                116, 120, 124, 128, 132, 136, 140, 144,
                                149, 153,
                                157, 161, 165
                            ]
                            newRF = await lib.rfp_pwr(newRF)
                            if appcfg.WRITE:
                                await db.wireless.updateNetworkWirelessRfProfile(
                                    net_id, selfRF['id'], **newRF)
                                self.ReSync = True
                        else:
                            # no more RFProfiles in self, create one
                            print(
                                f'\t{lib.bc.OKBLUE}RF Profile[{lib.bc.WARNING}{masterRF["name"]}{lib.bc.OKBLUE}]!!! New RFP created in network{lib.bc.ENDC}'
                            )
                            newRF = copy.deepcopy(masterRF)
                            newRF.pop('id')
                            newRF.pop('networkId')
                            newRF = await lib.rfp_pwr(newRF)
                            newRF['fiveGhzSettings'].pop(
                                'validAutoChannels')
                            newRF['fiveGhzSettings'][
                                'validAutoChannels'] = [
                                36, 40, 44, 48, 52, 56, 60, 64, 100,
                                104,
                                108, 112, 116,
                                120, 124, 128, 132, 136, 140, 144, 149,
                                153, 157, 161, 165
                            ]
                            if appcfg.WRITE:
                                await db.createNetworkWirelessRfProfile(
                                    net_id, **newRF)
                                self.ReSync = True
        else:
            print(
                f'\t{lib.bc.OKBLUE} {netName} {lib.bc.OKGREEN}-Settings for  {task} Matched Master{lib.bc.ENDC}')

    async def Update_NetworkWirelessSsidIdentityPsks(self,
                                                     master: object,
                                                     appcfg: object,
                                                     db: object,
                                                     net_id: str, task,
                                                     netName):
        """
        Compaires SSID iPSKs with the Master Configuratio
        and Updates The RF Profile If neede
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
        # NetworkWirelessSsidIdentityPsks

        ipsk_tmp = []
        for r in range(0, 15):
            ipsk_tmp.append({})
        for ssid_num in self.ssids_range:
            # if not ssid_num in self.ssids_range: continue
            # ipsk_tmp.append({}) #keep track of master iPSKs so we can remove unused ones from local(self)
            for m_ipsk in master.NetworkWirelessSsidIdentityPsks[ssid_num]:
                if not m_ipsk['name'] in ipsk_tmp[ssid_num]:
                    ipsk_tmp[ssid_num][m_ipsk['name']] = m_ipsk[
                        'passphrase']

                # ipsks are not empty, find the matching group policy
                new_ipsk = copy.deepcopy(m_ipsk)
                # pop off the ID from master, new one will be created "local"
                new_ipsk.pop('id')
                master_GP_tmp = await lib.matchGidByName(
                    master.NetworkGroupPolicies,
                    str(new_ipsk['groupPolicyId']))
                local_GP_tmp = await lib.idFromName(
                    self.NetworkGroupPolicies,
                    str(master_GP_tmp['name']))
                new_ipsk['groupPolicyId'] = local_GP_tmp['groupPolicyId']

                for s_ipsk in self.NetworkWirelessSsidIdentityPsks[
                    ssid_num]:
                    if new_ipsk['name'] == s_ipsk['name']:
                        # if passwords are different, delete the ipsk and re-create
                        if new_ipsk['passphrase'] != s_ipsk['passphrase']:
                            if appcfg.WRITE:
                                self.ReSync = True
                                try:
                                    await db.wireless.deleteNetworkWirelessSsidIdentityPsk(
                                        net_id, ssid_num, s_ipsk['id'])
                                except:
                                    print(
                                        f'ERROR: iPSK Issue, resyncing and trying again')
                                    await self.Get_NetworkWirelessSsidIdentityPsks(
                                        db, net_id, appcfg)
                                    await db.wireless.deleteNetworkWirelessSsidIdentityPsk(
                                        net_id, ssid_num, s_ipsk['id'])

                    else:
                        try:
                            await db.wireless.createNetworkWirelessSsidIdentityPsk(
                                net_id, ssid_num, **new_ipsk)
                            self.ReSync = True
                        except:
                            print(
                                f'{lib.bc.FAIL}{netName} - {task} \t\t{lib.bc.FAIL}iPSK already created or still there{lib.bc.ENDC}')

        if self.ReSync or not appcfg.CLEAN:
            await self.Get_NetworkWirelessSsidIdentityPsks(db, net_id, appcfg)
            appcfg.CLEAN = True
            self.ReSync = False

        # cleanUP local iPSK
        for ssid_num in self.ssids_range:
            for s_ipsk in self.NetworkWirelessSsidIdentityPsks[
                ssid_num]:
                if not s_ipsk['name'] in ipsk_tmp[ssid_num]:
                    if appcfg.WRITE:
                        self.ReSync = True
                        print(
                            f'\t\t{lib.bc.OKBLUE}-Removing Legacy iPSK[{s_ipsk["name"]}]{lib.bc.ENDC}')
                        await db.wireless.deleteNetworkWirelessSsidIdentityPsk(
                            net_id, ssid_num, s_ipsk['id'])
