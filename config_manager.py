import os
import configparser

CONFIG_FILE = "ftp-config.cfg"

def load_config():
    config = configparser.ConfigParser()
    if not os.path.exists(CONFIG_FILE):
        config['FTP'] = {
            'username': 'user',
            'password': '123',
            'port': '21',
            'ftp_directory': r'C:\Temp\FTP',
            'run_as_daemon': '0',
            'log_file': 'ftp_log.txt'
        }
        with open(CONFIG_FILE, 'w') as configfile:
            config.write(configfile)
    else:
        config.read(CONFIG_FILE)
    return config
