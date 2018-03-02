#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2018 Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'network'}


DOCUMENTATION = '''
---
module: json_parser
short_description: Parses JSON openconfig based configs into xml which ansible
can play
description:
     Parses JSON openconfig based configs into xml which ansible can play
version_added: "2.5"
options:
  src:
    source file with openconfig in json
    required: true
  output:
    output xml will be written here
    required: true
author:
  - Ansible Network Team
'''

EXAMPLES = '''
- json_parser:
    src: bgp.json
    output: bgp.xml
'''
