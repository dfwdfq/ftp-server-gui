import os
import sys
import configparser

CONFIG_FILE = "ftp-config.cfg"

def _mkdir(directory):
    if os.path.isdir(directory): return directory

    try:
        os.mkdir(directory)
        print(f"{directory} is directory for FTP config.")
        return directory
    except Exception as e:
        print(str(e))
        os.exit(-1)
        
def _create_ftp_dir(directory):
    return r'{}'.format(_mkdir(directory))

def get_default_path_based_on_OS():
    OS = sys.platform
    if "linux" == OS or "darwin" == OS:
        return os.path.expanduser("~/FTP")
    if "win32" == OS:
        return "C:\\TEMP\\FTP"

def load_config():
    config = configparser.ConfigParser()
    if not os.path.exists(CONFIG_FILE):
        config['FTP'] = {
            'username': 'user',
            'password': '123',
            'port': '21',
            'ftp_directory': _create_ftp_dir(get_default_path_based_on_OS()),
            'run_as_daemon': '0',
            'log_file': 'ftp_log.txt'
        }
        with open(CONFIG_FILE, 'w') as configfile:
            config.write(configfile)
    else:
        config.read(CONFIG_FILE)
    return config
