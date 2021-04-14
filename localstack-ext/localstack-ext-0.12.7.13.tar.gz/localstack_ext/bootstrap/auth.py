import sys
GSiaT=object
GSiaN=staticmethod
GSiay=False
GSiaV=Exception
GSiaB=None
GSiaC=input
GSiaQ=list
import json
import logging
import getpass
from localstack.config import CONFIG_FILE_PATH,load_config_file
from localstack.constants import API_ENDPOINT
from localstack.utils.common import to_str,safe_requests,save_file,load_file
LOG=logging.getLogger(__name__)
class AuthProvider(GSiaT):
 @GSiaN
 def name():
  raise
 def get_or_create_token(self,username,password,headers):
  pass
 def get_user_for_token(self,token):
  pass
 @GSiaN
 def providers():
  return{c.name():c for c in AuthProvider.__subclasses__()}
 @GSiaN
 def get(provider,raise_error=GSiay):
  provider_class=AuthProvider.providers().get(provider)
  if not provider_class:
   msg='Unable to find auth provider class "%s"'%provider
   LOG.warning(msg)
   if raise_error:
    raise GSiaV(msg)
   return GSiaB
  return provider_class()
class AuthProviderInternal(AuthProvider):
 @GSiaN
 def name():
  return 'internal'
 def get_or_create_token(self,username,password,headers):
  data={'username':username,'password':password}
  response=safe_requests.post('%s/user/signin'%API_ENDPOINT,json.dumps(data),headers=headers)
  if response.status_code>=400:
   return
  try:
   result=json.loads(to_str(response.content or '{}'))
   return result['token']
  except GSiaV:
   pass
 def read_credentials(self,username):
  print('Please provide your login credentials below')
  if not username:
   sys.stdout.write('Username: ')
   sys.stdout.flush()
   username=GSiaC()
  password=getpass.getpass()
  return username,password,{}
 def get_user_for_token(self,token):
  raise GSiaV('Not implemented')
def login(provider,username=GSiaB):
 auth_provider=AuthProvider.get(provider)
 if not auth_provider:
  providers=GSiaQ(AuthProvider.providers().keys())
  raise GSiaV('Unknown provider "%s", should be one of %s'%(provider,providers))
 username,password,headers=auth_provider.read_credentials(username)
 print('Verifying credentials ... (this may take a few moments)')
 token=auth_provider.get_or_create_token(username,password,headers)
 if not token:
  raise GSiaV('Unable to verify login credentials - please try again')
 configs=load_config_file()
 configs['login']={'provider':provider,'username':username,'token':token}
 save_file(CONFIG_FILE_PATH,json.dumps(configs))
def logout():
 configs=json_loads(load_file(CONFIG_FILE_PATH,default='{}'))
 configs['login']={}
 save_file(CONFIG_FILE_PATH,json.dumps(configs))
def json_loads(s):
 return json.loads(to_str(s))
# Created by pyminifier (https://github.com/liftoff/pyminifier)
