import sys
import concurrent.futures
import pyclamd
import winrm
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QLabel,
    QLineEdit,
    QCheckBox,
    QFileDialog,
    QComboBox,
)
from qdarkstyle import load_stylesheet_pyqt5


class ClamAVScan(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("ClamAV Remote Computer Scanner")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet(load_stylesheet_pyqt5())  # Apply dark theme

        # Create the main layout
        layout = QVBoxLayout()

        # Create the computer name input
        computer_label = QLabel("Computer Name:")
        self.computer_input = QLineEdit(self)
        layout.addWidget(computer_label)
        layout.addWidget(self.computer_input)

        # Create the username input
        username_label = QLabel("Username:")
        self.username_input = QLineEdit(self)
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)

        # Create the password input
        password_label = QLabel("Password:")
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)

        # Create the output window
        self.output_window = QTextEdit(self)
        layout.addWidget(self.output_window)

        # Create the authentication method selection
        auth_label = QLabel("Authentication Method:")
        self.auth_combo = QComboBox(self)
        self.auth_combo.addItems(["NTLM", "Basic"])
        layout.addWidget(auth_label)
        layout.addWidget(self.auth_combo)

        # Create the install and scan buttons
        install_button = QPushButton("Install ClamAV", self)
        install_button.clicked.connect(self.install_clamav)
        layout.addWidget(install_button)

        scan_button = QPushButton("Scan Remote Computer", self)
        scan_button.clicked.connect(self.scan_remote_computer)
        layout.addWidget(scan_button)

        # Create the main widget and set the layout
        main_widget = QWidget(self)
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def update_output(self, message):
        # Append the message to the output window
        self.output_window.append(message)

    def run_powershell_script(self, script, session):
        # Run a custom PowerShell script on the remote computer using winrm
        encoded_ps = f"[{script.encode('utf_16_le').hex()}]"
        ps_script = (
            f"$command = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String('{encoded_ps}'));"
            f"Invoke-Expression $command"
        )
        result = session.run_ps(ps_script)
        return result.std_out.decode()

    def install_clamav(self):
        computer_name = self.computer_input.text()
        username = self.username_input.text()
        password = self.password_input.text()

        # Sample PowerShell script to install Chocolatey and ClamAV using Chocolatey
        install_script = """
        # Set execution policy to allow script execution
        Set-ExecutionPolicy Bypass -Scope Process -Force;

        # Install Chocolatey and ClamAV using Chocolatey
        iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'));
        choco install clamav -y
        """

        try:
            # Initialize WinRM session
            session = winrm.Session(
                computer_name, auth=(username, password), transport="ntlm"
            )

            # Run the installation script on the remote computer
            self.update_output(
                "Installing Chocolatey and ClamAV on the remote computer..."
            )
            install_output = self.run_powershell_script(install_script, session)
            self.update_output(install_output)
            self.update_output("Installation completed.")

        except Exception as e:
            self.update_output(f"Error during installation: {e}")

    def install_chocolatey(self, session):
        # PowerShell script to install Chocolatey
        install_chocolatey_script = """
        # Set execution policy to allow script execution
        Set-ExecutionPolicy Bypass -Scope Process -Force;

        # Install Chocolatey
        iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
        """

        # Run the installation script on the remote computer with PowerShell version 5.0
        self.update_output("Installing Chocolatey on the remote computer...")
        install_output = session.run_ps(
            install_chocolatey_script, shell="pwsh", codepage=65001
        )
        self.update_output(install_output.std_out.decode())
        self.update_output("Chocolatey installation completed.")

    def scan_remote_computer(self):
        computer_name = self.computer_input.text()
        username = self.username_input.text()
        password = self.password_input.text()
        enable_archive_scan = self.archive_scan_checkbox.isChecked()
        scan_specific_files = self.scan_files_checkbox.isChecked()
        file_path = self.file_path_input.text()

        try:
            # Initialize WinRM session
            session = winrm.Session(
                computer_name, auth=(username, password), transport="ntlm"
            )

            # Asynchronous scanning using concurrent.futures.ThreadPoolExecutor
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(
                    self.do_scan,
                    computer_name,
                    enable_archive_scan,
                    scan_specific_files,
                    file_path,
                    session,
                )

                # Periodically check the progress and update the GUI
                while not future.done():
                    self.scan_progress(future.result() * 100)
                    # You can adjust the sleep interval based on your requirements
                    # For frequent updates, use a smaller value like 0.1 seconds
                    # For less frequent updates, use a larger value like 1 second
                    concurrent.futures.wait([future], timeout=1)

            # The scanning is completed, display the final result
            scan_result = future.result()
            self.update_output(f"Scanning result for {computer_name}:")
            self.update_output(scan_result)

        except Exception as e:
            self.update_output(f"Error: {e}")

    def do_scan(
        self,
        computer_name,
        enable_archive_scan,
        scan_specific_files,
        file_path,
        session,
    ):
        try:
            # Connect to ClamAV daemon on the remote computer using pyclamd
            cd = pyclamd.ClamdNetworkSocket(
                computer_name, 3310
            )  # Assuming the pyclamd server is listening on port 3310
            cd.ping()  # Test the connection

            # Get the scanning target (file/directory) based on the options selected
            if scan_specific_files:
                scanning_target = file_path
            else:
                scanning_target = (
                    "C:/"  # Default to scan the entire C drive, change as needed
                )

            # Perform the scan and get the result
            scan_result = cd.scan_file(scanning_target, multiscan=enable_archive_scan)

            return scan_result

        except pyclamd.ConnectionError as e:
            raise Exception(
                f"Could not reach ClamAV daemon using network on {computer_name}: {e}"
            )
        except pyclamd.ScanError as e:
            raise Exception(f"ClamAV scan error on {computer_name}: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet_pyqt5())
    main_window = ClamAVScan()
    main_window.show()
    sys.exit(app.exec_())
