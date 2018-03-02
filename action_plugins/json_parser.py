# (c) 2017, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
import os
import re
import copy
import json
import collections
import q

from ansible import constants as C
from ansible.plugins.action import ActionBase
from ansible.module_utils.network.common.utils import to_list
from ansible.module_utils.six import iteritems, string_types
from ansible.module_utils._text import to_bytes, to_text
from ansible.errors import AnsibleError, AnsibleUndefinedVariable, AnsibleFileNotFound
from collections import OrderedDict

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()

def warning(msg):
    if C.ACTION_WARNINGS:
        display.warning(msg)

openconfig_xmlns = {
    "<bgp>" : "<bgp xmlns=\"http://openconfig.net/yang/bgp\">",
    "<afi-safi-name>" : "<afi-safi-name xmlns:idx=\"http://openconfig.net/yang/bgp-types\">",
    "ipv4-unicast" : "idx:ipv4-unicast",
    "True"         : "true"
}

class ActionModule(ActionBase):

    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)

        try:
            src = self._task.args.get('src')
            output_file = self._task.args.get('output')
        except KeyError as exc:
            return {'failed': True, 'msg': 'missing required argument: %s' % exc}

        self.facts = {}

        if not os.path.exists(src) and not os.path.isfile(src):
            raise AnsibleError("src is either missing or invalid")
        
        #json_config = self._loader.load_from_file(src)
        with open(src, 'r') as f:
           json_config = f.read()
           j_obj = json.loads(json_config, object_pairs_hook=OrderedDict)
           config_xml = self._json_to_xml(j_obj)
           config_xml_w_xmlns = self._add_openconfig_xmlns_to_config(config_xml,
                   openconfig_xmlns)
           config_xml_final = self._post_openconfig_parsing(config_xml_w_xmlns)

        with open(output_file, 'w') as f:
            f.write(config_xml_final)
        
        #self.ds.update(task_vars)
        result['ansible_facts'] = self.facts
        return result

    def _add_openconfig_xmlns_to_config(self, result_list, xmlns_dict):
        for key in xmlns_dict:
           result_list = result_list.replace(key, xmlns_dict[key])
        
        return (result_list)

    def _post_openconfig_parsing(self, result_list, line_padding=""):
        start_tag = "<config>\n"
        end_tag   = "\n%s</%s>" % (line_padding, "config")
        result_list = start_tag + result_list + end_tag
        return (result_list)
        

    def _json_to_xml(self, json_obj, line_padding=""):
        result_list = []
        
        json_obj_type = type(json_obj)
        
        if json_obj_type is list:
           for sub_elem in json_obj:
               result_list.append(self._json_to_xml(sub_elem, line_padding))
           return "\n".join(result_list)

        #if json_obj_type is dict:
        if json_obj_type is collections.OrderedDict:
           for tag_name in json_obj:
               sub_obj = json_obj[tag_name]
               result_list.append("%s<%s>" % (line_padding, tag_name))
               result_list.append(self._json_to_xml(sub_obj, "\t"+line_padding))
               result_list.append("%s</%s>" % (line_padding, tag_name))
           return "\n".join(result_list)
           
        return "%s%s" % (line_padding, json_obj)


