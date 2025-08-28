import sys
from PyQt5.QtWidgets import QApplication
from config_manager import load_config
from gui import FTPGuiApp

if __name__ == '__main__':
    config = load_config()
    app = QApplication(sys.argv)
    gui = FTPGuiApp(config)
    
    if not config.getboolean('FTP', 'run_as_daemon'):
        gui.show()

    sys.exit(app.exec_())
