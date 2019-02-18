import os
from sys import version_info

if version_info[0] < 3:
    from ConfigParser import ConfigParser
else:
    from configparser import ConfigParser

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETTINGS_PATH = os.path.join(ROOT_DIR, 'settings.ini')


class SettingsValueError(Exception):
    "No value for a certain setting"


class GetFunctionError(Exception):
    "value_type to get function needs to be: str/int/float/boolean"

class SettingsHandler(object):
    def __init__(self, settings_path=SETTINGS_PATH):
        self.path = settings_path
        self.config = ConfigParser()
        self.config.optionxform = str
        self.get_config()

    def get_config(self):
        """
        Returns the config object
        """
        if os.path.exists(self.path):
            self.config.read(self.path)
        else:
            raise FileNotFoundError("Settings.ini Does not exists on the path: {}".format(self.path))

    def get_setting(self, section, setting, value_type='str'):
        """
        Returns the setting in the given section with the requested value type
        :param section:
        :param setting:
        :param value_type:
        :return:
        """
        get_setting_name = "get{v_type}".format(v_type="" if value_type == 'str' else value_type)
        get_setting_func = getattr(self.config, get_setting_name, None)
        if get_setting_func is None:
            raise GetFunctionError("value_type to get function needs to be: str/int/float/boolean")
        value = get_setting_func(section, setting)
        if not value:
            raise SettingsValueError("No value in settings.ini for the option '{}'".format(setting))
        return value
