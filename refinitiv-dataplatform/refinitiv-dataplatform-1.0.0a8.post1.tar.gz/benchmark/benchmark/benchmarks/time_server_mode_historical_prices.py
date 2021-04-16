import helper

cfg = {
    'logs': {
        'level': 'debug'
        },
    'sessions': {
        'platform': {
            'default-session': {
                'auto-reconnect': True,
                }
            },
        }
    }
helper.write_json_file('rdplibconfig.prod.json', cfg)

import asyncio

import refinitiv.dataplatform as rdp

session = helper.create_platform_session(rdp)
session.open()

events = rdp.HistoricalPricing.get_events(universe='VOD.L', session=session)
print(f"Is successful : {events.is_success}")
print(f"Dataframe: {events.data.df}")
print(f"Raw: {events.data.raw}")
print(f"Status: {events.status}")
print(f"Error code: {events.error_code}")
print(f"Error message: {events.error_message}")
print("#####################")

asyncio.get_event_loop().run_forever()
