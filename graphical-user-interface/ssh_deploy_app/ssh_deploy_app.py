import csv
import paramiko
import sys
import os
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QPlainTextEdit,
    QCheckBox,
    QHBoxLayout,
    QProgressBar,
    QSpinBox,
    QToolTip,
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

dark_theme_style = """
QMainWindow {
    background-color: #202020;
    color: #FFFFFF;
}
QLabel, QLineEdit, QPlainTextEdit, QPushButton, QCheckBox, QProgressBar, QSpinBox {
    background-color: #404040;
    color: #FFFFFF;
    border: 1px solid #FFFFFF;
    padding: 5px;
}
QPlainTextEdit {
    font-family: Consolas, Courier, monospace;
}
QPushButton:hover {
    background-color: #606060;
}
QToolTip {
    color: #FFFFFF;
    background-color: #303030;
    border: 1px solid #FFFFFF;
}
"""


class SSHConnectionThread(QThread):
    log_updated = pyqtSignal(str)

    def __init__(
        self, host, port, username, password, ssh_key, deployment_commands, timeout
    ):
        super().__init__()
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.ssh_key = ssh_key
        self.deployment_commands = deployment_commands
        self.timeout = timeout

    def run(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(
                self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                key_filename=self.ssh_key,
                timeout=self.timeout,
            )

            self.log_updated.emit(f"Successfully connected to {self.host}")

            for index, command in enumerate(self.deployment_commands, 1):
                stdin, stdout, stderr = ssh.exec_command(command)
                self.log_updated.emit(
                    f"[{index}/{len(self.deployment_commands)}] Deployment command output for {self.host}:"
                )
                self.log_updated.emit(stdout.read().decode())

        except paramiko.ssh_exception.AuthenticationException as e:
            self.log_updated.emit(f"Authentication failed for {self.host}: {e}")
        except paramiko.ssh_exception.SSHException as e:
            self.log_updated.emit(f"SSH error occurred for {self.host}: {e}")
        except paramiko.BadHostKeyException as e:
            self.log_updated.emit(f"Bad host key for {self.host}: {e}")
        except paramiko.AuthenticationException as e:
            self.log_updated.emit(f"Authentication failed for {self.host}: {e}")
        except paramiko.SSHException as e:
            self.log_updated.emit(f"SSH error occurred for {self.host}: {e}")
        except paramiko.BadHostKeyException as e:
            self.log_updated.emit(f"Bad host key for {self.host}: {e}")
        except paramiko.ssh_exception.NoValidConnectionsError as e:
            self.log_updated.emit(f"Connection error for {self.host}: {e}")
        except Exception as e:
            self.log_updated.emit(f"Error connecting to {self.host}: {e}")
        finally:
            ssh.close()


class SSHDeployApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SSH Deploy App")
        self.setGeometry(100, 100, 800, 600)

        self.hosts_file_path = ""
        self.ssh_key = ""
        self.deployment_script = ""
        self.log_text = ""
        self.deployment_threads = []

        layout = QVBoxLayout()

        self.file_label = QLabel("Select CSV File:")
        layout.addWidget(self.file_label)

        self.file_line_edit = QLineEdit()
        self.file_line_edit.setPlaceholderText("No file selected.")
        layout.addWidget(self.file_line_edit)

        self.select_file_button = QPushButton("Select File")
        self.select_file_button.clicked.connect(self.select_file)
        layout.addWidget(self.select_file_button)

        ssh_key_layout = QHBoxLayout()
        self.ssh_key_checkbox = QCheckBox("Use SSH Key")
        self.ssh_key_checkbox.stateChanged.connect(self.toggle_ssh_key)
        ssh_key_layout.addWidget(self.ssh_key_checkbox)

        self.ssh_key_label = QLabel("SSH Key File:")
        self.ssh_key_label.hide()
        ssh_key_layout.addWidget(self.ssh_key_label)

        self.ssh_key_line_edit = QLineEdit()
        self.ssh_key_line_edit.setPlaceholderText("No SSH Key selected.")
        self.ssh_key_line_edit.hide()
        ssh_key_layout.addWidget(self.ssh_key_line_edit)

        self.select_ssh_key_button = QPushButton("Select SSH Key")
        self.select_ssh_key_button.clicked.connect(self.select_ssh_key)
        self.select_ssh_key_button.hide()
        ssh_key_layout.addWidget(self.select_ssh_key_button)

        layout.addLayout(ssh_key_layout)

        self.deployment_label = QLabel(
            "Custom Deployment Commands (Separate with semicolon ';'):"
        )
        layout.addWidget(self.deployment_label)

        self.deployment_text_area = QPlainTextEdit()
        layout.addWidget(self.deployment_text_area)

        options_layout = QHBoxLayout()

        port_label = QLabel("Port:")
        options_layout.addWidget(port_label)

        self.port_spin_box = QSpinBox()
        self.port_spin_box.setRange(1, 65535)
        self.port_spin_box.setValue(22)
        options_layout.addWidget(self.port_spin_box)

        timeout_label = QLabel("Timeout (s):")
        options_layout.addWidget(timeout_label)

        self.timeout_spin_box = QSpinBox()
        self.timeout_spin_box.setRange(1, 600)
        self.timeout_spin_box.setValue(30)
        options_layout.addWidget(self.timeout_spin_box)

        self.save_settings_button = QPushButton("Save Settings")
        self.save_settings_button.clicked.connect(self.save_settings)
        options_layout.addWidget(self.save_settings_button)

        self.load_settings_button = QPushButton("Load Settings")
        self.load_settings_button.clicked.connect(self.load_settings)
        options_layout.addWidget(self.load_settings_button)

        layout.addLayout(options_layout)

        self.log_label = QLabel("Deployment Log:")
        layout.addWidget(self.log_label)

        self.log_text_area = QPlainTextEdit()
        self.log_text_area.setReadOnly(True)
        layout.addWidget(self.log_text_area)

        progress_layout = QHBoxLayout()
        self.progress_bar = QProgressBar()
        progress_layout.addWidget(self.progress_bar)

        self.deploy_button = QPushButton("Deploy")
        self.deploy_button.clicked.connect(self.deploy_hosts)
        progress_layout.addWidget(self.deploy_button)

        self.save_log_button = QPushButton("Save Log")
        self.save_log_button.clicked.connect(self.save_log_to_file)
        progress_layout.addWidget(self.save_log_button)

        layout.addLayout(progress_layout)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def toggle_ssh_key(self):
        is_checked = self.ssh_key_checkbox.isChecked()
        self.ssh_key_label.setVisible(is_checked)
        self.ssh_key_line_edit.setVisible(is_checked)
        self.select_ssh_key_button.setVisible(is_checked)

    def select_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv);;All Files (*)",
            options=options,
        )

        if file_path:
            self.hosts_file_path = file_path
            self.file_line_edit.setText(file_path)

    def select_ssh_key(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select SSH Key File", "", "All Files (*)", options=options
        )

        if file_path:
            self.ssh_key = file_path
            self.ssh_key_line_edit.setText(file_path)

    def deploy_hosts(self):
        if not self.hosts_file_path:
            self.add_log("Please select a CSV file.")
            return

        if not self.deployment_text_area.toPlainText().strip():
            self.add_log("Please enter deployment commands.")
            return

        self.progress_bar.reset()
        self.log_text_area.clear()
        self.deployment_threads.clear()

        try:
            with open(self.hosts_file_path, "r") as f:
                reader = csv.reader(f)
                # Skip the header row
                next(reader)

                total_hosts = sum(1 for _ in reader)
                f.seek(
                    0
                )  # Reset the file reader to the beginning after counting total_hosts
                next(reader)  # Skip the header row again

                for row in reader:
                    host, username, password = row
                    ssh_key = (
                        self.ssh_key if self.ssh_key_checkbox.isChecked() else None
                    )
                    deployment_commands = (
                        self.deployment_text_area.toPlainText().strip().split(";")
                    )

                    if not (host and username and (password or ssh_key)):
                        self.add_log(f"Invalid entry for host: {host}. Skipping.")
                        total_hosts -= 1
                        continue

                    if ssh_key and not os.path.isfile(ssh_key):
                        self.add_log(f"SSH key file not found: {ssh_key}. Skipping.")
                        total_hosts -= 1
                        continue

                    port = self.port_spin_box.value()
                    timeout = self.timeout_spin_box.value()

                    thread = SSHConnectionThread(
                        host,
                        port,
                        username,
                        password,
                        ssh_key,
                        deployment_commands,
                        timeout,
                    )
                    thread.log_updated.connect(self.add_log)
                    thread.finished.connect(self.update_progress)
                    self.deployment_threads.append(thread)
                    thread.start()

        except FileNotFoundError as e:
            self.add_log(f"Error opening file: {e}")
        except Exception as e:
            self.add_log(f"Error reading file: {e}")

    def add_log(self, message):
        self.log_text_area.appendPlainText(message)

    def update_progress(self):
        completed_threads = sum(
            thread.isFinished() for thread in self.deployment_threads
        )
        total_threads = len(self.deployment_threads)
        progress = (completed_threads / total_threads) * 100
        self.progress_bar.setValue(progress)

    def save_log_to_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Log to File",
            "",
            "Text Files (*.txt);;All Files (*)",
            options=options,
        )
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.log_text_area.toPlainText())

    def save_settings(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Settings to File",
            "",
            "INI Files (*.ini);;All Files (*)",
            options=options,
        )
        if file_path:
            settings = {
                "port": self.port_spin_box.value(),
                "timeout": self.timeout_spin_box.value(),
                "ssh_key": self.ssh_key_line_edit.text(),
                "deployment_commands": self.deployment_text_area.toPlainText(),
            }
            with open(file_path, "w") as file:
                for key, value in settings.items():
                    file.write(f"{key}={value}\n")

    def load_settings(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Settings from File",
            "",
            "INI Files (*.ini);;All Files (*)",
            options=options,
        )
        if file_path:
            with open(file_path, "r") as file:
                settings = {}
                for line in file:
                    key, value = line.strip().split("=")
                    settings[key] = value

                if "port" in settings:
                    self.port_spin_box.setValue(int(settings["port"]))

                if "timeout" in settings:
                    self.timeout_spin_box.setValue(int(settings["timeout"]))

                if "ssh_key" in settings:
                    self.ssh_key_line_edit.setText(settings["ssh_key"])

                if "deployment_commands" in settings:
                    self.deployment_text_area.setPlainText(
                        settings["deployment_commands"]
                    )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(dark_theme_style)
    QToolTip.setFont(app.font())
    window = SSHDeployApp()
    window.show()
    sys.exit(app.exec_())
