import meraki.aio
import logging
import meraki
import os
import asyncio
class MerakiAsyncApi:
    def __init__(self,appcfg):
        self._appcfg = appcfg
    def __enter__(self):
        self.api = meraki.aio.AsyncDashboardAPI(
            api_key=self._appcfg.MERAKI_DASHBOARD_API_KEY,
            base_url=self._appcfg.meraki_base_url,
            simulate=self._appcfg.simulate,
            wait_on_rate_limit=self._appcfg.wait_on_rate_limit,
            maximum_concurrent_requests =self._appcfg.maximum_concurrent_requests,
            nginx_429_retry_wait_time = self._appcfg.nginx_429_retry_wait_time,
            maximum_retries=int(self._appcfg.maximum_retries),
            log_file_prefix=os.path.basename(__file__)[:-3],
            log_path="Logs/",
            suppress_logging=self._appcfg.suppress_logging,
            print_console=False
            )
        return self.api
    def __exit__(self, type, value, traceback):
        #Exception handling here
        loop=asyncio.get_event_loop()
        loop.create_task(self.api._session.close())
    def __del__(self):
        loop=asyncio.get_event_loop()
        loop.create_task(self.api._session.close())
    async def closesession(self):
         await self.api._session.close()
        
class MerakiApi:
    def __init__(self,appcfg):
        self._appcfg = appcfg
        self.api = meraki.DashboardAPI(
                api_key=self._appcfg.MERAKI_DASHBOARD_API_KEY,
                base_url=self._appcfg.meraki_base_url,
                simulate=self._appcfg.simulate,
                wait_on_rate_limit=self._appcfg.wait_on_rate_limit,
                log_file_prefix=os.path.basename(__file__)[:-3],
                log_path="Logs/",
                suppress_logging=self._appcfg.suppress_logging
            )
        logger = logging.getLogger('meraki')
        logger.setLevel(logging.WARNING)
    def getAPI(self):
        return self.api