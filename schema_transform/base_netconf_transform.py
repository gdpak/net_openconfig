from __future__ import (absolute_import, division, print_function)

import json
from collections import OrderedDict

class SchemaTransformNetconfBase(object):

    '''
    Base Class for all common conversion for supported connection type
    All platform independent code should reside in base class
    '''

    '''
    Converts openconfig to XML which netconf can understand
    config should be passed as raw string (python 3 ?)
    '''
    def openconfig_to_netconf(self, config):
        json_py_obj = json.loads(config, object_pairs_hook=OrderedDict)
        config_xml = self._json_to_xml(json_py_obj)
        config_xml_final = self._post_openconfig_parsing(config_xml)

        return (config_xml_final)

    def _json_to_xml(self, json_obj, line_padding=""):
        result_list = []

        json_obj_type = type(json_obj)

        if json_obj_type is list:
            for sub_elem in json_obj:
                result_list.append(self._json_to_xml(sub_elem, line_padding))
            return "\n".join(result_list)

        # if json_obj_type is dict:
        if (json_obj_type is OrderedDict) or (json_obj_type is dict):
            for tag_name in json_obj:
                sub_obj = json_obj[tag_name]
                result_list.append("%s<%s>" % (line_padding, tag_name))
                result_list.append(self._json_to_xml(sub_obj, "\t" + line_padding))
                result_list.append("%s</%s>" % (line_padding, tag_name))
            return "\n".join(result_list)

        return "%s%s" % (line_padding, json_obj)

    def _post_openconfig_parsing(self, result_list, line_padding=""):
        start_tag = "<config>\n"
        end_tag   = "\n%s</%s>" % (line_padding, "config")
        result_list = start_tag + result_list + end_tag
        return (result_list)

