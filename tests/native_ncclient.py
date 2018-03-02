from ncclient import manager

with manager.connect(host="11.1.1.3", port=830, username="vagrant", password="vagrant", hostkey_verify=False) as m:
    c = m.get_config(source='running').data_xml
    print (c)
    with open("%s.xml" % host, 'w') as f:
        f.write(c)
