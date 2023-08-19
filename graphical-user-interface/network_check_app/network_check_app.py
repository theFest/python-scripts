import socket
import sys
import subprocess
import ctypes
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QSystemTrayIcon, QMenu, QAction, QStyleFactory, QMessageBox, QTextEdit, QVBoxLayout, QHBoxLayout, QFileDialog, QSlider, QFormLayout, QGroupBox, QCheckBox
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QIcon, QColor, QPalette, QPixmap
import ping3
import psutil
from ipwhois import IPWhois
import requests
from fontawesome import icons

class NetworkCheckApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Network Check Application")
        self.setGeometry(100, 100, 600, 300)
        
        self.init_ui()
        
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("icon.png"))
        self.tray_icon.setVisible(True)
        
        self.tray_menu = QMenu()
        self.show_action = QAction("Show", self)
        self.exit_action = QAction("Exit", self)
        self.tray_menu.addAction(self.show_action)
        self.tray_menu.addAction(self.exit_action)
        
        self.show_action.triggered.connect(self.show_window)
        self.exit_action.triggered.connect(self.exit_app)
        
        self.tray_icon.setContextMenu(self.tray_menu)
        
        self.output_text = ""
        
    def init_ui(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        
        self.create_layout()
        
    def create_layout(self):
        layout = QVBoxLayout()
        
        self.output_window = QTextEdit(self.central_widget)
        self.output_window.setReadOnly(True)
        layout.addWidget(self.output_window)
        
        settings_group = QGroupBox("Settings", self.central_widget)
        settings_layout = QFormLayout(settings_group)
        
        self.host_input = QLineEdit(self.central_widget)
        self.host_input.setPlaceholderText("Host (IP or Domain)")
        
        self.interval_input = QLineEdit(self.central_widget)
        self.interval_input.setPlaceholderText("Ping Interval (seconds)")
        
        self.timeout_slider = QSlider(Qt.Horizontal, self.central_widget)
        self.timeout_slider.setRange(1, 5000)
        self.timeout_slider.setValue(1000)
        self.timeout_slider.valueChanged.connect(self.update_timeout_label)
        self.timeout_value_label = QLabel("1000", self.central_widget)
        
        self.continuous_ping_checkbox = QCheckBox("Continuous Ping", self.central_widget)
        
        self.traceroute_button = QPushButton("Traceroute", self.central_widget)
        self.traceroute_button.clicked.connect(self.start_traceroute)
        
        self.geolocation_button = QPushButton("Geolocation Lookup", self.central_widget)
        self.geolocation_button.clicked.connect(self.start_geolocation_lookup)
        
        settings_layout.addRow("Host:", self.host_input)
        settings_layout.addRow("Interval:", self.interval_input)
        settings_layout.addRow("Timeout (ms):", self.timeout_slider)
        settings_layout.addRow("", self.timeout_value_label)
        settings_layout.addRow("", self.continuous_ping_checkbox)
        settings_layout.addRow("", self.traceroute_button)
        settings_layout.addRow("", self.geolocation_button)
        
        settings_group.setLayout(settings_layout)
        
        control_layout = QHBoxLayout()
        
        self.ping_button = QPushButton("Ping Test", self.central_widget)
        ping_icon = QPixmap(icons['network-wired']).scaledToHeight(20)
        self.ping_button.setIcon(QIcon(ping_icon))
        self.ping_button.clicked.connect(self.start_ping)

        self.clear_button = QPushButton("Clear Output", self.central_widget)
        self.clear_button.clicked.connect(self.clear_output)
        
        self.save_button = QPushButton("Save Log", self.central_widget)
        self.save_button.clicked.connect(self.save_log)
        
        self.minimize_button = QPushButton("Minimize to Tray", self.central_widget)
        self.minimize_button.clicked.connect(self.minimize_to_tray)
        
        control_layout.addWidget(self.ping_button)
        control_layout.addWidget(self.clear_button)
        control_layout.addWidget(self.save_button)
        control_layout.addWidget(self.minimize_button)
        
        layout.addWidget(settings_group)
        layout.addLayout(control_layout)
        self.central_widget.setLayout(layout)
        
    def update_timeout_label(self):
        self.timeout_value_label.setText(str(self.timeout_slider.value()))
        
    def start_ping(self):
        if hasattr(self, 'timer') and self.timer.isActive():
            self.stop_ping()
        else:
            host = self.host_input.text()
            interval = self.interval_input.text()
            timeout = self.timeout_slider.value() / 1000.0

            if not host or not interval.isdigit():
                QMessageBox.critical(self, "Error", "Invalid input. Please enter a valid host and interval.")
                return

            self.timer = QTimer(self)
            self.timer.timeout.connect(self.ping)
            self.timer.start(int(interval) * 1000)
            self.ping_button.setText("Stop Ping")
            self.continuous_ping_checkbox.setEnabled(False)
            self.timeout_slider.setEnabled(False)
        
    def stop_ping(self):
        if hasattr(self, 'timer') and self.timer.isActive():
            self.timer.stop()
            self.ping_button.setText("Ping Test")
            self.continuous_ping_checkbox.setEnabled(True)
            self.timeout_slider.setEnabled(True)
        
    def ping(self):
        host = self.host_input.text()
        timeout = self.timeout_slider.value() / 1000.0
        
        response_time = ping3.ping(host, timeout=timeout, unit="ms")
        
        if response_time is not None:
            self.append_to_output(f"Ping response from {host}: {response_time:.2f} ms", "green")
        else:
            self.append_to_output(f"Request timed out for {host}", "red")
        
    def start_traceroute(self):
        host = self.host_input.text()
        
        if not host:
            QMessageBox.critical(self, "Error", "Invalid input. Please enter a valid host.")
            return
        
        try:
            command = ["tracert", host]
            result = subprocess.run(command, stdout=subprocess.PIPE, text=True)
            self.append_to_output(result.stdout, "white")
        except subprocess.CalledProcessError:
            self.append_to_output("Traceroute failed.", "red")
        
    def start_geolocation_lookup(self):
        host = self.host_input.text()
        
        if not host:
            QMessageBox.critical(self, "Error", "Invalid input. Please enter a valid host.")
            return
        
        try:
            ip = socket.gethostbyname(host)
            ipwhois = IPWhois(ip)
            results = ipwhois.lookup_rdap()
            country = results.get('asn_country_code', 'Unknown')
            self.append_to_output(f"Geolocation for {host}: Country - {country}", "green")
        except:
            self.append_to_output("Geolocation lookup failed.", "red")
        
    def append_to_output(self, text, color):
        self.output_text += f'<span style="color: {color}">{text}</span><br>'
        self.output_window.setHtml(self.output_text)
        self.output_window.verticalScrollBar().setValue(self.output_window.verticalScrollBar().maximum())
        
    def show_window(self):
        self.show()
        
    def exit_app(self):
        self.tray_icon.hide()
        self.close()
        
    def clear_output(self):
        self.output_text = ""
        self.output_window.clear()
        
    def save_log(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Log", "", "Text Files (*.txt);;All Files (*)", options=options)
        
        if file_name:
            with open(file_name, "w") as file:
                file.write(self.output_text)
                
    def minimize_to_tray(self):
        self.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    app.setStyle(QStyleFactory.create("Fusion"))
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

    fw_app_id = u'fw.network.checkapp.1'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(fw_app_id)
    
    window = NetworkCheckApp()
    window.show()
    sys.exit(app.exec_())
