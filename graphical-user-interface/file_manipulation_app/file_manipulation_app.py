import sys
import os
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QFileDialog,
    QTextEdit,
    QSpinBox,
    QAction,
    QMenuBar,
    QStatusBar,
)
from PyQt5.QtGui import QPalette, QColor


class FileManipulationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("FW File Manipulation App")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        status_bar = QStatusBar(self)
        self.setStatusBar(status_bar)

        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Text, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
        self.setPalette(dark_palette)

        prefix_label = QLabel("Prefix:")
        self.prefix_input = QLineEdit()
        suffix_label = QLabel("Suffix:")
        self.suffix_input = QLineEdit()
        extension_label = QLabel("Extension:")
        self.extension_input = QLineEdit()
        num_files_label = QLabel("Number of Files:")
        self.num_files_input = QSpinBox()
        self.num_files_input.setRange(1, 1000)
        content_label = QLabel("File Content:")
        self.content_input = QTextEdit()
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browseDirectory)
        create_button = QPushButton("Create Files")
        create_button.clicked.connect(self.createFiles)
        self.log_text = QTextEdit()

        layout.addWidget(prefix_label)
        layout.addWidget(self.prefix_input)
        layout.addWidget(suffix_label)
        layout.addWidget(self.suffix_input)
        layout.addWidget(extension_label)
        layout.addWidget(self.extension_input)
        layout.addWidget(num_files_label)
        layout.addWidget(self.num_files_input)
        layout.addWidget(content_label)
        layout.addWidget(self.content_input)
        layout.addWidget(browse_button)
        layout.addWidget(create_button)
        layout.addWidget(self.log_text)

    def browseDirectory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.log_text.append(f"Selected directory: {directory}")
            self.selected_directory = directory

    def createFiles(self):
        prefix = self.prefix_input.text()
        suffix = self.suffix_input.text()
        extension = self.extension_input.text()
        num_files = self.num_files_input.value()
        content = self.content_input.toPlainText()

        if not (
            prefix
            and suffix
            and extension
            and num_files > 0
            and content
            and hasattr(self, "selected_directory")
        ):
            self.log_text.append("Please fill in all fields and select a directory.")
            return

        try:
            os.makedirs(self.selected_directory, exist_ok=True)
            for i in range(1, num_files + 1):
                filename = f"{prefix}{i}{suffix}.{extension}"
                file_path = os.path.join(self.selected_directory, filename)
                with open(file_path, "w") as file:
                    file.write(content)
            self.log_text.append(
                f"Created {num_files} files in {self.selected_directory}"
            )
        except Exception as e:
            self.log_text.append(f"Error creating files: {str(e)}")


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = FileManipulationApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
