from config import Config

def set_info(instance):
    print("\n---")
    print("The info can also be found in the config.ini file")
    if Config.has_section(instance['ID']):
        for key, val in instance.items():
            print("{0}:{1}".format(key, val))
            val = str(val)
            Config.add_to_section(instance['ID'], key, val)

    else:
        Config.add_new_section(instance['ID'])
        for key, val in instance.items():
            if val == None:
                val = ""
            print(key, val)
            
            Config.add_to_section(instance['ID'], key, val)

    with open('config.ini', 'w') as configfile:
        Config.write(configfile)

def update(identifier, key, val):
    if Config.has_section(identifier):
        Config.update(identifier, key, val)
    
    with open('config.ini', 'w') as configfile:
        Config.write(configfile)

