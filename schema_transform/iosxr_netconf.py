from __future__ import (absolute_import, division, print_function)

from schema_transform.base_netconf_transform import SchemaTransformNetconfBase

class IosxrSchemaTransformNetconf(SchemaTransformNetconfBase):
    def __init__(self):
        self.openconfig_iosxr_xmlns = {
            "<bgp>": "<bgp xmlns=\"http://openconfig.net/yang/bgp\">",
            "<afi-safi-name>": "<afi-safi-name xmlns:idx=\"http://openconfig.net/yang/bgp-types\">",
            "ipv4-unicast": "idx:ipv4-unicast",
            "True": "true"
        }

    def openconfig_to_netconf(self, config):
        config_xml = super(IosxrSchemaTransformNetconf, self).openconfig_to_netconf(config)
        config_xml_wt_ns = self._add_openconfig_xmlns_to_config(config_xml, self.openconfig_iosxr_xmlns)
        return (config_xml_wt_ns)

    def _add_openconfig_xmlns_to_config(self, result_list, xmlns_dict):
        for key in xmlns_dict:
            result_list = result_list.replace(key, xmlns_dict[key])

        return (result_list)