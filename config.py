from configparser import SafeConfigParser

class Config:
    configParser = SafeConfigParser()
    configFilePath = 'config.ini'
    configParser.read(configFilePath)
        
    @classmethod
    def add_new_section(cls, key):
        return cls.configParser.add_section(key)

    @classmethod
    def get_from_section(cls, section, key):
        return cls.configParser.get(section, key)

    @classmethod
    def add_to_section(cls, section, key, val):
        return cls.configParser.set(section, key, val)
    
    @classmethod
    def remove_key(cls, section, key):
        return cls.configParser.remove_option(section, key)

    @classmethod
    def remove_section(cls, section):
        return cls.configParser.remove_section(section)

    @classmethod
    def has_section(cls, section):
        return cls.configParser.has_section(section)

    @classmethod
    def has_val(cls, section, val):
        return cls.configParser.has_option(section, val)
    
    @classmethod
    def write(cls, file):
        return cls.configParser.write(file)

    @classmethod
    def update(cls, section, key, val):
        return cls.configParser.set(section, key, val)