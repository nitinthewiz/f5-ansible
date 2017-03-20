#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2017 F5 Networks Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import json

from ansible.compat.tests import unittest
from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes
from library.iworkflow_system_setup import (
    Parameters,
)


fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures')
fixture_data = {}


def set_module_args(args):
    args = json.dumps({'ANSIBLE_MODULE_ARGS': args})
    basic._ANSIBLE_ARGS = to_bytes(args)


def load_fixture(name):
    path = os.path.join(fixture_path, name)

    if path in fixture_data:
        return fixture_data[path]

    with open(path) as f:
        data = f.read()

    try:
        data = json.loads(data)
    except:
        pass

    fixture_data[path] = data
    return data


class TestParameters(unittest.TestCase):

    def test_module_parameters(self):
        args = dict(
            hostname='iworkflow1.local',
            discovery_address='10.2.2.3',
            management_address='10.0.2.15',
            dns_servers=[
                '8.8.8.8'
            ],
            dns_search_domains=[
                'foo.bar.org'
            ],
            ntp_servers=[
                '2.2.2.2'
            ]
        )
        p = Parameters(args)
        assert p.hostname == 'iworkflow1.local'

    def test_api_parameters_variables(self):
        easy_setup = load_fixture('load_easy_setup.json')
        setup = load_fixture('load_setup.json')
        discovered = load_fixture('load_identified_devices_config_discovery.json')

        args = dict()
        args.update(easy_setup)
        args.update(setup),
        args.update(discovered)

        p = Parameters(args)
        assert p.hostname == 'iworkflow1.local'
