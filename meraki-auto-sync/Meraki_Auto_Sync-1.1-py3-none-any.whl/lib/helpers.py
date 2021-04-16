import requests, http3,json
async def _aironetie(net_id: str, _config: object, p_ssid: int,
                        p_apikey: str):
    # looks up org id for a specific org name
    # on failure returns 'null'
    try:
        client = http3.AsyncClient()
        r = await client.get(
            'https://api.meraki.com/api/v1/networks/%s/wireless/ssids/%s/overrides'
            % (net_id, p_ssid),
            headers={
                'X-Cisco-Meraki-API-Key': p_apikey,
                'Content-Type': 'application/json'
            })
    
        if r.status_code != requests.codes.ok:
            return 'null'
    
        rjson = r.json()
        return rjson
    except:
        return "null"

    
async def setAironetIe(net_id: str, cfg: object, _config: object, p_ssid: int,
                        p_data: dict):
    # looks up org id for a specific org name
    # on failure returns 'null'

    r = requests.put(
        'https://api.meraki.com/api/v1/networks/%s/wireless/ssids/%s/overrides'
        % (net_id, p_ssid),
        data=json.dumps(p_data),
        headers={
            'X-Cisco-Meraki-API-Key': cfg.MERAKI_DASHBOARD_API_KEY,
            'Content-Type': 'application/json'
        })

    if r.status_code != requests.codes.ok:
        return 'null'

    rjson = r.json()

    return rjson

async def AironetIe(net_id: str, _config: object, p_ssid: int,
                        p_apikey: str):
    # looks up org id for a specific org name
    # on failure returns 'null'
    client = http3.AsyncClient()
    r = await client.get(
        'https://api.meraki.com/api/v1/networks/%s/wireless/ssids/%s/overrides'
        % (net_id, p_ssid),
        headers={
            'X-Cisco-Meraki-API-Key': p_apikey,
            'Content-Type': 'application/json'
        })

    if r.status_code != requests.codes.ok:
        return 'null'

    rjson = r.json()

    return rjson

async def rfp_pwr(RFP):
    if 'twoFourGhzSettings' in RFP:
        if 'minPower' in RFP['twoFourGhzSettings'] and \
                RFP['twoFourGhzSettings']['minPower'] < 5:
            RFP['twoFourGhzSettings']['minPower'] = 5
        if 'maxPower' in RFP['twoFourGhzSettings'] and \
                RFP['twoFourGhzSettings']['maxPower'] < 5:
            RFP['twoFourGhzSettings']['maxPower'] = 5

    if 'fiveGhzSettings' in RFP:
        if 'minPower' in RFP['fiveGhzSettings'] and \
                RFP['fiveGhzSettings']['minPower'] < 5:
            RFP['fiveGhzSettings']['minPower'] = 8
        if 'maxPower' in RFP['fiveGhzSettings'] and \
                RFP['fiveGhzSettings']['maxPower'] < 5:
            RFP['fiveGhzSettings']['maxPower'] = 8
    return RFP
