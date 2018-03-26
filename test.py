from __future__ import unicode_literals

import requests
from requests.exceptions import HTTPError
from urlparse import urlparse
from urllib import quote_plus

from .config import *
from .keystone_client import KeystoneClient
import json

def _pack_json_role(name, application_id):
    data = json.dumps({'role' : {
                        'name' : name, 
                        'application_id' : application_id}})
    return json.loads(data)


class Test:

    def test_rbac():
        keystone_client = KeystoneClient(KEYSTONE_USER, KEYSTONE_PWD, ADMIN_DOMAIN, 'http', 'idm.docker')
        
        url = 'http://pep.proxy:7000/v2/entities/room1'
        service = 'TenantRZ1'
        test_url =  url.split('?')[0]
        print test_url
        test_url = service + ':' + test_url
        print test_url

        json_role = _pack_json_role('consumer-role4', 'c0fc8c23f7044861ad2e941d9774729e')
        print json.dumps(json_role)
        if not (keystone_client.get_role_id_by_name('c0fc8c23f7044861ad2e941d9774729e','consumer-role3')):
            role = keystone_client.create_role(json_role)
            role_id = json.loads(role.text)['role']['id']    
        else:
            print "Role: " + 'consumer-role' + ' already exists'

    #print pack_json_role('v2', 'Consumer-v2', 'GET', 'c0fc8c23f7044861ad2e941d9774729e')

