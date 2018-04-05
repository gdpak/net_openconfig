from __future__ import (absolute_import, division, print_function)

from schema_transform.base_netconf_transform import SchemaTransformNetconfBase

class JunosSchemaTransformNetconf(SchemaTransformNetconfBase):
    def __init__(self):

    '''
    Function: openconfig_to_netconf
    Input: config in XML format (string)
    Output: Junos specific converted config (string)
    '''
    def openconfig_to_netconf(self, config, xpath_map=None):
        # NO_OP as of now
        # Not able to test openconfig model with Junos
        if xpath_map is not None:
            return self.openconfig_to_xpath_map(config, xpath_map)
        else:
            return (config)

    '''
    Function: nconfig_to_native_junos
    Input: 
        config - config in XML format (string) in openconfig model
        xpath_map - conversion rule (e.g. see template/xpath_map_op_junos )
    Output: 
        return transformed config in xml (string)
    '''
    def openconfig_to_xpath_map(self, config, xpath_map):

