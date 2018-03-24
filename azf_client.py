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

   