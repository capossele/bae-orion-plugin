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
        
        url = 'http://pep.proxy:7000/v2/entities/room1/attrs/temperature'
        parsed_url = urlparse(url) 
        service = 'TenantRZ1'
        #test_url =  url.split('?')[0]
        #print test_url
        #test_url = service + ':' + test_url
        print url
        s = parsed_url.path
        print s
        #print s.find("/v2",0,3)
        if (s.find('/v2') == 0) and (s.find('/v2/entities') == -1):
            resource = s.split('/')[1]
        elif s.find('/v2/entities/') == 0:
            resource = s.split('/')[3]
        else:
            print "URL not valid"
        role_name = service + ':' + resource
        print role_name

        print keystone_client.get_role_id_by_name('c0fc8c23f7044861ad2e941d9774729e', role_name)
        # json_role = _pack_json_role('consumer-role3', 'c0fc8c23f7044861ad2e941d9774729e')
        # print json.dumps(json_role)
        # if not (keystone_client.get_role_id_by_name('c0fc8c23f7044861ad2e941d9774729e','consumer-role3')):
        #     role = keystone_client.create_role(json_role)
        #     role_id = json.loads(role.text)['role']['id']    
        # else:
        #     print "Role: " + 'consumer-role' + ' already exists'

    #print pack_json_role('v2', 'Consumer-v2', 'GET', 'c0fc8c23f7044861ad2e941d9774729e')

    test_rbac()