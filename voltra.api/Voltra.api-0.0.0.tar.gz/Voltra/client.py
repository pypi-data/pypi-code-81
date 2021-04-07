import aiohttp, requests

class VoltraClient:
    def __init__(self, token: str):
        self.token = token
        self.ws = 'ws://voltra.tk'
        
        
        
    async def change_username(self, username: str):
        "Change username"
        async with aiohttp.ClientSession() as session:
            async with session.post(f'http://voltra.xyz/bot/api/username?sid={self.token}&username={username}', headers={'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}) as req:
                req = await req.json()
                
        return req

    async def change_avatar(self, avatar):
        async with aiohttp.ClientSession() as session:
            async with session.post(f'http://voltra.xyz/bot/api/avatar?sid={self.token}&body={avatar}') as req:
                req = await req.json()
                
        return req
    
    def get_channel(self, _id):
        "Gets a channel from a id"
        req = requests.get(f'http://voltra.xyz/api/gc?id={_id}')
        if (req.status_code != 200):
            return req.status_code
        else:
            return req.json().get('json')

    def get_user(self, uid):
        "Gets a user from a id"
        req = requests.get(
            f'http://voltra.xyz/api/u?id={uid}&sid={self.token}')
        if (req.status_code != 200):
            return req
        else:
            return req.json().get('json')
    
    async def join_guild(self, guildid):
        async with aiohttp.ClientSession() as session:
            async with session.post(f'http://voltra.xyz/g/api/join?sid={self.token}&g={guildid}') as req:
                req = await req.json()

        return req
