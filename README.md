# Problem Statement

There is a requirement of a ventor agnostic data-model for configuration and operational data for controlling networking devices. All network configurations should be able to modelled in this language and should be communicated to destination device either in chosen native data-model or a tranform function should be provided to convert to defined data-model of vendor device.

# Solution Approach
- openconfig data-model is selected as vendor-neutral data-model to express network configurations
- Few vendors understand openconfig data-model as it is so no transformation is required to control these devices
- For vendors who do not talk in openconfig, a tranformation path is provided

# Example usage
- Define your configs in openconfig model in a file and keep it in valid path as any other ansible template file
- This openconfig template file supports jinja2 directives so you can define variable which can be declared per
  host or group as per requirements
- use new module provided as part of this role 'open_config_parser' to parse the configs in openconfig or native
  vendor model. 
- Conversion schema from openconfig to vendor native format should be provided by argument 'xpath_map' to above role
- use 'netconf_config' module to play configs produced to destination device

# new module

module: open_config_parser                                                                                                                  
description: Parses JSON openconfig based configs into openconfig xml or native OS format                                                                                                                                    
version_added: "2.5"                                                                                                                        
options:                                                                                                                                    
   - src:                                                                                                                                      
       source file with openconfig in json. This file can have vars in jinja2 template                                                         
       required: true                                                                                                                          
   - output:                                                                                                                                   
       output will be file in xml format which can be used using netconf_* modules                                                                                                                                 
       required: true                                                                                                                          
   - xpath_map:                                                                                                                                
       optional mapping of openconfig model to desired model (e.g. device native xml )                                                                                                                           
       required: false                                                                                                                         
                                                                                                                                     
EXAMPLES = '''                                                                                                                              
- open_config_parser:                                                                                                                       
    src: bgp.json                                                                                                                           
    output: bgp.xml                                                                                                                         
    xpath_map: templates/junos_open_to_native_map.yml  
                                                                                              
