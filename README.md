# net_openconfig

Ansible role for defining configuration in JSON template with openconfig yang schema. 
Configuration can be defined in ansible template format and will support jinja2 directives.

Configuration will be communicated to target networking device with netconf protocol.

#new module

json_parser - parses json configs to native device config in xml based on ansible_network_os
ex:
- hosts: rtr1
  tasks:
    - name: Parse BGP configurations                                                    
      json_parser:                                                                                                         
          src: 'templates/bgp_edit_config.json'
          output: 'templates/bgp_edit_config_exp.xml'
      register: result                                                                                                       
                                           
o/p can be used to communicate with target device using netconf_config
Example:
- hosts: rtr1
  tasks:
    - name: Enable bgp iosxr                                                     
      netconf_config:                                                                                                         
          src: bgp_edit_config_exp.xml
      register: result                                                                                                        
