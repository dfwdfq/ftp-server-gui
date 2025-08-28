import os
import logging
import socket
from PyQt5.QtCore import QThread, pyqtSignal
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

class FTPServerThread(QThread):
    log_signal = pyqtSignal(str)

    def __init__(self, port, username, password, ftp_directory, log_file, parent=None):
        super(FTPServerThread, self).__init__(parent)
        self.port = port
        self.username = username
        self.password = password
        self.ftp_directory = ftp_directory
        self.log_file = log_file
        self.server = None
        self.running = False
        self.setup_logger()

    def setup_logger(self):
        """Setup logger to log both to file and emit to GUI."""
        self.logger = logging.getLogger("FTPServer")
        self.logger.setLevel(logging.INFO)

        # Create file handler
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
        self.logger.addHandler(file_handler)

    def run(self):
        if not os.path.exists(self.ftp_directory):
            os.makedirs(self.ftp_directory)

        # Set up authorizer with user authentication
        authorizer = DummyAuthorizer()
        authorizer.add_user(self.username, self.password, self.ftp_directory, perm="elradfmw")

        # Set up FTP handler
        handler = FTPHandler
        handler.authorizer = authorizer

        # Override handler log method to connect to the log signal and file logger
        handler.log = self.log

        # Create FTP server
        self.server = FTPServer(("0.0.0.0", self.port), handler)
        self.running = True
        self.server.serve_forever()

    def log(self, message, logfun=None):
        """Custom log method to emit logs to the GUI and log to the file."""
        self.log_signal.emit(message)
        self.logger.info(message)

    def stop(self):
        if self.server:
            self.server.close_all()
            self.running = False

def get_ip_addresses():
    """Get all non-local IP addresses of the current machine."""
    ip_list = []
    for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
        if not ip.startswith("127."):
            ip_list.append(ip)
    return ip_list
