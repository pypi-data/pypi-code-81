import secrets


s = secrets.Secrets()
s['api_key'] = 'abc'

print(s['api_key'])

