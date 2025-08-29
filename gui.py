import os
from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QVBoxLayout, 
                             QHBoxLayout, QLineEdit, QTextEdit, QFormLayout, 
                             QSpinBox, QFileDialog, QSystemTrayIcon, QMenu, 
                             QAction, QCheckBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from ftp_server import FTPServerThread, get_ip_addresses

class FTPGuiApp(QWidget):
    def __init__(self, config):
        super().__init__()
        self.setWindowTitle("Simple FTP Server")
        self.server_thread = None
        self.ftp_directory = config['FTP']['ftp_directory']
        self.run_as_daemon = config.getboolean('FTP', 'run_as_daemon')
        self.log_file = config['FTP'].get('log_file', 'ftp_log.txt')
        self.username = config['FTP']['username']
        self.password = config['FTP']['password']
        self.port = config.getint('FTP', 'port')

        self.tray_icon = None
        self.init_ui()

        # Start in daemon mode if configured
        if self.run_as_daemon:
            self.start_server()
            self.hide_to_tray()

    def init_ui(self):
        layout = QVBoxLayout()

        # Form for user, password, port, and directory
        form_layout = QFormLayout()

        self.username_input = QLineEdit()
        self.username_input.setText(self.username)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setText(self.password)
        self.port_input = QSpinBox()
        self.port_input.setRange(1, 65535)
        self.port_input.setValue(self.port)

        form_layout.addRow("Username:", self.username_input)
        form_layout.addRow("Password:", self.password_input)
        form_layout.addRow("Port:", self.port_input)

        # FTP directory picker
        self.directory_input = QLineEdit()
        self.directory_input.setText(self.ftp_directory)
        self.directory_button = QPushButton("Browse FTP Folder")
        self.directory_button.clicked.connect(self.select_directory)

        directory_layout = QHBoxLayout()
        directory_layout.addWidget(self.directory_input)
        directory_layout.addWidget(self.directory_button)

        layout.addLayout(form_layout)
        layout.addLayout(directory_layout)

        # Log file path picker
        self.log_file_input = QLineEdit()
        self.log_file_input.setText(self.log_file)
        self.log_file_button = QPushButton("Browse Log File")
        self.log_file_button.clicked.connect(self.select_log_file)

        log_layout = QHBoxLayout()
        log_layout.addWidget(self.log_file_input)
        log_layout.addWidget(self.log_file_button)

        layout.addLayout(log_layout)

        # Daemon mode checkbox
        self.daemon_checkbox = QCheckBox("Run as Daemon (Minimize to Tray)")
        self.daemon_checkbox.setChecked(self.run_as_daemon)
        layout.addWidget(self.daemon_checkbox)

        # Button to start and stop the server
        self.start_button = QPushButton("Start FTP Server")
        self.start_button.clicked.connect(self.start_server)
        self.stop_button = QPushButton("Stop FTP Server")
        self.stop_button.clicked.connect(self.stop_server)
        self.stop_button.setEnabled(False)

        # Layout for buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)

        layout.addLayout(button_layout)

        # Log view to show server activity
        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        layout.addWidget(self.log_view)

        # Label to show listening IP addresses
        self.ip_label = QLabel("Listening on:")
        layout.addWidget(self.ip_label)

        self.setLayout(layout)

        # Set up system tray for daemon mode
        self.setup_tray_icon()

    def setup_tray_icon(self):
        icon_path = os.path.join(os.path.dirname(__file__), 'ftp.png')
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(icon_path))

        tray_menu = QMenu()

        restore_action = QAction("Restore", self)
        restore_action.triggered.connect(self.show)
        tray_menu.addAction(restore_action)

        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.close)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.tray_icon.show()

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.show()

    def hide_to_tray(self):
        self.hide()
        self.tray_icon.showMessage("FTP Server", "Running in background", QSystemTrayIcon.Information, 3000)

    def select_directory(self):
        folder = QFileDialog.getExistingDirectory(self, "Select FTP Folder", self.ftp_directory)
        if folder:
            self.ftp_directory = folder
            self.directory_input.setText(folder)

    def select_log_file(self):
        log_file, _ = QFileDialog.getSaveFileName(self, "Select Log File", self.log_file, "Log Files (*.txt)")
        if log_file:
            self.log_file = log_file
            self.log_file_input.setText(log_file)

    def start_server(self):
        username = self.username_input.text()
        password = self.password_input.text()
        port = self.port_input.value()
        ftp_directory = self.directory_input.text()
        log_file = self.log_file_input.text()

        self.server_thread = FTPServerThread(port, username, password, ftp_directory, log_file)
        self.server_thread.log_signal.connect(self.log_message)
        self.server_thread.start()

        self.update_ip_addresses()
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

        if self.daemon_checkbox.isChecked():
            self.hide_to_tray()

    def stop_server(self):
        if self.server_thread:
            self.server_thread.stop()
            self.server_thread.wait()

        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def log_message(self, message):
        self.log_view.append(message)
        print(message) #whenever you add message, print it, cause it's cool to see what's going on rn

    def update_ip_addresses(self):
        ip_addresses = get_ip_addresses()
        self.ip_label.setText(f"Listening on: {', '.join(ip_addresses)}")

    def closeEvent(self, event):
        if self.daemon_checkbox.isChecked():
            event.ignore()
            self.hide_to_tray()
        else:
            event.accept()
