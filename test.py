from __future__ import unicode_literals

import requests
from requests.exceptions import HTTPError
from urlparse import urlparse
from urllib import quote_plus

from .config import *
from .keystone_client import KeystoneClient
from .azf_client import AzfClient
import json

def _pack_json_permission(resource, name, action, application_id):
    data = json.dumps({'permission' : {
                        'xml' : '', 
                        'resource' : resource,
                        'name' : name,
                        'action' : action,
                        'application_id' : application_id}})
    return json.loads(data)

def _pack_json_role(name, application_id):
    data = json.dumps({'role' : {
                        'name' : name, 
                        'application_id' : application_id}})
    return json.loads(data)


class Test:

    def test_azf_domain():
        keystone_client = KeystoneClient(KEYSTONE_USER, KEYSTONE_PWD, ADMIN_DOMAIN, 'http', 'idm.docker')
        azf_domain = keystone_client.get_azf_domain_by_app_id('c0fc8c23f7044861ad2e941d9774729e')
        
        url = 'http://pep.proxy:7000/v2/entities/room1'
        service = 'TenantRZ1'
        test_url =  url.split('?')[0]
        print test_url
        test_url = service + ':' + test_url
        print test_url

        json_role = _pack_json_role('consumer-role4', 'c0fc8c23f7044861ad2e941d9774729e')
        json_permission = _pack_json_permission('v2', 'Consumer-v4', 'GET', 'c0fc8c23f7044861ad2e941d9774729e')
        print json.dumps(json_role)
        print json.dumps(json_permission)
        if not (keystone_client.get_role_id_by_name('c0fc8c23f7044861ad2e941d9774729e','consumer-role3')):
            role = keystone_client.create_role(json_role)
            role_id = json.loads(role.text)['role']['id']
            permission = keystone_client.create_permission(json_permission)
            permission_id = json.loads(permission.text)['permission']['id']
            print keystone_client.grant_permission_to_role(permission_id, role_id)

            azf_client = AzfClient(azf_domain, 'http', 'pdp.docker', '8081')
            
            policy = {
                'role_id': role_id,
                'permission_name': 'Consumer-v4',
                'permission_id': permission_id,
                'app_id': 'c0fc8c23f7044861ad2e941d9774729e',
                'resource': test_url,
                'action': 'GET',
            }


            print azf_client.update_policy(policy)
        else:
            print "Role: " + 'consumer-role' + ' already exists'

        # print "AZF domain: " + azf_domain
        # azf_client = AzfClient(azf_domain, 'http', 'pdp.docker', '8081')
        # root = azf_client.get_pap_policies()
        # for child in root.iter('*'):
        #     print(child.tag, child.attrib)

    
    
    test_azf_domain()
    #print pack_json_role('v2', 'Consumer-v2', 'GET', 'c0fc8c23f7044861ad2e941d9774729e')

