from ncclient import manager

with manager.connect(host="vsrx02.example.net", port=830,
        username="ansible", password="Ansible", hostkey_verify=False) as m:
    c = m.get_config(source='running').data_xml
    print (c)
    '''
    for cap in m.server_capabilities:
        print (cap)a
    '''
    #with open("%s.xml" % host, 'w') as f:
    #    f.write(c)
