import asyncio

import refinitiv.dataplatform as rdp
from refinitiv.dataplatform import configure

configure.config["auto-reconnect"] = True

rdp.open_platform_session(
    "8e5a3ec37ebc4177ba51bd9345776656221b031c",
    grant=rdp.GrantPassword(
        username="GE-A-01103867-3-1857",
        password="edppassword@123"
        )
    )

rdp.StreamingPrices(universe=["GBP="]).open()

asyncio.get_event_loop().run_forever()
