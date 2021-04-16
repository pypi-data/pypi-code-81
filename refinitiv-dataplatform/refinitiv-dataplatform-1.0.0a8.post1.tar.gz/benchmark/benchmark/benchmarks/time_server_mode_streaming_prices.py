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
streaming_prices = rdp.StreamingPrices(
    session=session,
    universe=['JPY=', 'EUR='],
    fields=['BID', 'ASK'],
    )

streaming_prices.open()

asyncio.get_event_loop().run_forever()
