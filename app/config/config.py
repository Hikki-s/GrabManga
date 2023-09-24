import configparser
import os


config = configparser.ConfigParser()
config_file = 'settings.ini'


def create_conf():
    if not os.path.exists(config_file):
        config.add_section('Settings')
        config.set('Settings', 'save_path', '../../')
        config.set('Settings', 'save_images', 'False')
        config.set('Settings', 'pdf_merge', 'True')
        with open(config_file, 'w') as configfile:
            config.write(configfile)
