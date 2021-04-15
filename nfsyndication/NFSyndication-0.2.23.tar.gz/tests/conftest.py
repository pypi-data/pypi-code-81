import os, glob
import pytest
import subprocess
import pytest
from NFSyndication import __main__ as NFS_init
from NFSyndication import parser as PS
# test@
# Change the action associated with your option to action='store'
"""
def test_conf():
    #We use these conditions to check the statement
    subscriptions = [
     'http://feedpress.me/512pixels',
     'http://www.leancrew.com/all-this/feed/',
     'http://ihnatko.com/feed/',
     'http://blog.ashleynh.me/feed']
  
    with open(f'feeds.txt', 'w', encoding='utf8') as f:
     f.write(",".join(subscriptions).replace(',', '\n'))
    return NFS_init.run()
    
def test_entrypoint():
    #Then initialize code
    return test_conf()
    
def pytest_configure():
    pytest.something = test_entrypoint()
"""

@pytest.fixture
def test_client():
    configure_app(flask_app, config_name=Environments.TESTS)
    # I use this a lot for custom Test client classes to inject custom things
    my_project.app.test_client_class = CustomApiTestClient
    client = ''
    yield client