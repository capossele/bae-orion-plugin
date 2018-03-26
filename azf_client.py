# -*- coding: utf-8 -*-

# Copyright (c) 2018, Digital Catapult

# This file belongs to the orion context broker plugin
# of the Business API Ecosystem.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Author: Angelo Capossele

from __future__ import unicode_literals

import requests
import xml.etree.ElementTree as ET
import uuid


class AzfClient:

    _server = None
    _domain = None


    def __init__(self, domain, protocol, host, port):
        self._domain = domain
        self._server = protocol + '://' + host + ':' + unicode(port)

       

    def _make_get_request(self, url):
        resp = requests.get(url)
        resp.raise_for_status()
        #tree = ET.parse(resp.text)
        #root = tree.getroot()
        root = ET.fromstring(resp.content)
        return root

    def get_pap_policies(self):
        return self._make_get_request(self._server + '/authzforce-ce/domains/' + self._domain + '/pap/policies')

    def update_policy(self, policy):

        context = {
            'role_id': policy['role_id'],
            'permission_name': policy['permission_name'],
            'permission_id': policy['permission_id'],
            'app_id': policy['app_id'],
            'resource': policy['resource'],
            'action': policy['action'],
            'policy_id': str(uuid.uuid4())
        }
        
        xmlTemplate = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
            <PolicySet xmlns="urn:oasis:names:tc:xacml:3.0:core:schema:wd-17" PolicySetId="%(policy_id)s" Version="1.0"  PolicyCombiningAlgId="urn:oasis:names:tc:xacml:3.0:policy-combining-algorithm:deny-unless-permit">
            <Description>Policy Set for application %(app_id)s</Description>
            <Target />
            <Policy PolicyId="%(role_id)s" Version="1.0" RuleCombiningAlgId="urn:oasis:names:tc:xacml:3.0:rule-combining-algorithm:deny-unless-permit">
            <Description>Role %(role_id)s from application %(app_id)s</Description>
            <Target>
                <AnyOf>
                <AllOf>
                    <Match MatchId="urn:oasis:names:tc:xacml:1.0:function:string-equal">
                    <AttributeValue DataType="http://www.w3.org/2001/XMLSchema#string">%(app_id)s</AttributeValue>
                    <AttributeDesignator Category="urn:oasis:names:tc:xacml:3.0:attribute-category:resource"
                        AttributeId="urn:oasis:names:tc:xacml:1.0:resource:resource-id" DataType="http://www.w3.org/2001/XMLSchema#string"
                        MustBePresent="true" />
                    </Match>
                </AllOf>
                </AnyOf>
            </Target>

            <Rule RuleId="%(permission_id)s" Effect="Permit">
            <Description>%(permission_name)s</Description>
            <Target>
                <AnyOf>
                <AllOf>
                    <Match MatchId="urn:oasis:names:tc:xacml:3.0:function:string-equal">
                    <AttributeValue DataType="http://www.w3.org/2001/XMLSchema#string">%(resource)s</AttributeValue>
                    <AttributeDesignator Category="urn:oasis:names:tc:xacml:3.0:attribute-category:resource"
                        AttributeId="urn:thales:xacml:2.0:resource:sub-resource-id" DataType="http://www.w3.org/2001/XMLSchema#string"
                        MustBePresent="true" />
                    </Match>
                </AllOf>
                </AnyOf>
                <AnyOf>
                <AllOf>
                    <Match MatchId="urn:oasis:names:tc:xacml:3.0:function:string-equal">
                    <AttributeValue DataType="http://www.w3.org/2001/XMLSchema#string">%(action)s</AttributeValue>
                    <AttributeDesignator Category="urn:oasis:names:tc:xacml:3.0:attribute-category:action"
                        AttributeId="urn:oasis:names:tc:xacml:1.0:action:action-id" DataType="http://www.w3.org/2001/XMLSchema#string"
                        MustBePresent="true" />
                    </Match>
                </AllOf>
                </AnyOf>
            </Target>
            <Condition>
                <Apply FunctionId="urn:oasis:names:tc:xacml:3.0:function:any-of">
                <Function FunctionId="urn:oasis:names:tc:xacml:1.0:function:string-equal" />
                <AttributeValue DataType="http://www.w3.org/2001/XMLSchema#string">%(role_id)s</AttributeValue>
                <AttributeDesignator AttributeId="urn:oasis:names:tc:xacml:2.0:subject:role"
                    DataType="http://www.w3.org/2001/XMLSchema#string" MustBePresent="false"
                    Category="urn:oasis:names:tc:xacml:1.0:subject-category:access-subject" />
                </Apply>
            </Condition>
            </Rule>
            </Policy>
            </PolicySet>"""
        
        
        xml = xmlTemplate%context
        # LOG.debug('XACML: %s', xml)

        headers = {
            'content-type': 'application/xml'
            #'X-Auth-Token': settings.ACCESS_CONTROL_MAGIC_KEY
        }

        url = self._server + '/authzforce-ce/domains/' + self._domain + '/pap/policies'

        #LOG.debug('Sending request to : %s', url)

        response = requests.post(
            url,
            data=xml,
            headers=headers,
            verify=False)

        print response.text
        
        #LOG.debug('Response code from the AC GE: %s', response.status_code)

        xmlTemplate = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><pdpPropertiesUpdate xmlns="http://authzforce.github.io/rest-api-model/xmlns/authz/5"><rootPolicyRefExpression>%(policy_id)s</rootPolicyRefExpression></pdpPropertiesUpdate>"""

        xml = xmlTemplate%context
        url = self._server + '/authzforce-ce/domains/' + self._domain + '/pap/pdp.properties'
        
        # #LOG.debug('Activating policy %s', policy_id)
        # #LOG.debug('Sending request to : %s', url)

        response = requests.put(
            url,
            data=xml,
            headers=headers,
            verify=False)

        print response.text
        return response

   