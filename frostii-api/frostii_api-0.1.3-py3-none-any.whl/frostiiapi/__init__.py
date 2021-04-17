try:
    import aiohttp, asyncio
except ImportError:
    raise RuntimeError("Cannot run the program, aiohttp and asyncio are not installed.")
    
__version__ = "0.1.3"    
    
class Route:
    API = "https://frostii-api.herokuapp.com/"

class Client:
     __slots__ = ('token','__init','__session',)
     def __init__(self, token : str):
         self.token = token
         
     async def alwayshasbeen(self, text):
         """
         Always has been endpoint.
         """
         try:
             try_to_catch_error = self.__init
         except AttributeError:
             raise RuntimeError("Please run the init function.")
         else:
             async with self.__session.get(Route.API+"ahb", params={"token": self.token, "text": text}) as resp:
                 return await resp.read()
     
     async def init(self):
         """
         Initialize the modules the client needs.
         """
         self.__session = aiohttp.ClientSession()
         self.__init = True