# jdbc:hive2://{gateway-host}:{gateway-port}/;ssl=true;sslTrustStore={gateway-trust-store-path};trustStorePassword={gateway-trust-store-password};transportMode=http;httpPath={gateway-path}/{cluster-name}/hive


"""
from IPython.display import display
from ipywidgets import IntProgress

#TODO: clean (not really linked to this context of config?)
#def hive_url(conf:Config)->str:
#    return conf.KNOX_URL.format(**cred)

#TODO: implement
def validate_credential(user,password):
    print(f'Test credential for {user}')
    import time
    f = IntProgress(min=0, max=10) # instantiate the bar
    display(f) # display the bar
    time.sleep(0.5)
    #init stuff
    f.value+=3
    if user == 'fail':
        return False
    #main test
    time.sleep(1)
    f.value+=7
    return True
"""