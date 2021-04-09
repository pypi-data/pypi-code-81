import requests
import json
class ProBotDB:
    def __init__(self,authToken,serverId,embedName = 'probot.db'):
        if type(authToken) != str or type(serverId) !=str or type(embedName) != str:
            raise TypeError("authToken, serverId, embedName must be a string")
        self.authToken = authToken
        self.serverId = serverId
        self.embedName = embedName
        self.headers={
                'Authorization': self.authToken,
                'Content-Type': 'application/json',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0',
            }
        self.cache = None
    def _fetchEmbed(self):
        response = requests.get(f'https://api.probot.io/{self.serverId}/embeds',headers=self.headers).json()

        embeds = list(filter(lambda a : a['name'] == self.embedName,response))
        if len(embeds) == 0:
            raise Exception(f"There's more than one embed with the name \"{self.embedName}\"")
        embed = embeds[0]

        if not embed:
            data= {
                'access': self.authToken,
                'guild_id': self.serverId,
                'method': 'ADD_EMBED',
            }
            response = requests.put('https://api.probot.io/',headers=self.headers,data=json.dumps(data).encode('utf-8')).json()

            embed = response[len(response) - 1]
        if not embed['content'] or len(embed['content']) == 0:
            data = {
                    'access': self.authToken,
                    'embed': {
                        '_id': embed['_id'],
                        'content': '{}',
                        'embed': {},
                        'guild': self.serverId,
                        'name': self.embedName,
                    },
                    'guild_id': self.serverId,
                    'method': 'UPDATE_EMBED',
                   }
            requests.put('https://api.probot.io/',headers=self.headers,data=json.dumps(data).encode('utf-8'))
            embed['content'] = '{}'
        return embed

    def _write(self,data):
        embed = self._fetchEmbed()
        data_ = {
            'access': self.authToken,
            'embed': {
                '_id': embed['_id'],
                'content': str(json.dumps(data)),
                'embed': {},
                'guild': self.serverId,
                'name': self.embedName,
            },
            'guild_id': self.serverId,
            'method': 'UPDATE_EMBED',
        }
        requests.put('https://api.probot.io/',headers=self.headers,data=json.dumps(data_).encode('utf-8'))
        self.cache = data
        return True
    def _read(self):
        x = self._fetchEmbed()['content']
        return self.cache or json.loads(x)

    def clear(self):
        return self._write({})

    def delete(self,key):
        if type(key) != str:
            raise TypeError('Provided key must be a string')
        data = self._read()
        del data[key]
        return self._write(data)
    def push(self,key, element):
        if type(key) != str:
            raise TypeError('Provided key must be a string')
        arr = self.get(key) or []
        if type(arr) != list:
            raise TypeError(f'{key}" is not an array!')
        arr.append(element)
        return self.set(key, arr)
    def set(self,key, value):
        if type(key) != str:
            raise TypeError('Provided key must be a string')
        data = self._read()
        data[key] = value
        return self._write(data)
    def get(self,key):
        if type(key) != str:
            raise TypeError('Provided key must be a string')
        return self._read()[key]

