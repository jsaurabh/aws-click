from config import Config

def set_instance(id, n):
    if Config.has_section('current'):
        Config.add_to_section('current', 'instance-'+str(n), id)

    else:
        Config.add_new_section('current')
        Config.add_to_section('current', 'instance-'+str(n), id)

    with open('config.ini', 'w') as configfile:
        Config.write(configfile)

def set_ip(ip, n):
    if Config.has_section('current'):
        Config.add_to_section('current', 'ip-address-'+str(n), ip)

    else:
        Config.add_new_section('current')
        Config.add_to_section('current', 'ip-address-'+str(n), ip)

    with open('config.ini', 'w') as configfile:
        Config.write(configfile)