import sys
import subprocess
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QTextBrowser,
    QListWidget,
    QListWidgetItem,
    QMenu,
    QAction,
    QMenuBar,
    QStatusBar,
    QDialog,
    QColorDialog,
    QFontDialog,
    QComboBox,
)


class PreferencesDialog(QDialog):
    def __init__(self, current_preferences=None):
        super().__init__()

        self.setWindowTitle("Preferences")
        self.setFixedSize(400, 300)

        self.preferences = {
            "text_color": QColor(0, 0, 0),
            "bg_color": QColor(255, 255, 255),
            "font": QFont(),
            "theme": "Dark",
        }

        self.init_ui()
        if current_preferences:
            self.preferences.update(current_preferences)
            self.update_ui_from_preferences()

    def init_ui(self):
        layout = QVBoxLayout()

        self.text_color_label = QLabel("Text Color:")
        self.text_color_button = QPushButton("Choose Color")
        self.text_color_button.clicked.connect(self.choose_text_color)

        self.bg_color_label = QLabel("Background Color:")
        self.bg_color_button = QPushButton("Choose Color")
        self.bg_color_button.clicked.connect(self.choose_bg_color)

        self.font_label = QLabel("Font:")
        self.font_button = QPushButton("Choose Font")
        self.font_button.clicked.connect(self.choose_font)

        self.theme_label = QLabel("Theme:")
        self.theme_combobox = QComboBox()
        self.theme_combobox.addItems(["Dark", "Light"])
        self.theme_combobox.currentIndexChanged.connect(self.change_theme)

        reset_button = QPushButton("Reset to Defaults")
        reset_button.clicked.connect(self.reset_preferences)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_preferences)

        layout.addWidget(self.text_color_label)
        layout.addWidget(self.text_color_button)
        layout.addWidget(self.bg_color_label)
        layout.addWidget(self.bg_color_button)
        layout.addWidget(self.font_label)
        layout.addWidget(self.font_button)
        layout.addWidget(self.theme_label)
        layout.addWidget(self.theme_combobox)
        layout.addWidget(reset_button)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def update_ui_from_preferences(self):
        self.text_color_button.setStyleSheet(
            f"background-color: {self.preferences['text_color'].name()}"
        )
        self.bg_color_button.setStyleSheet(
            f"background-color: {self.preferences['bg_color'].name()}"
        )
        self.font_button.setText(
            f"{self.preferences['font'].family()}, {self.preferences['font'].pointSize()}"
        )
        self.theme_combobox.setCurrentText(self.preferences["theme"])

    def choose_text_color(self):
        color_dialog = QColorDialog(self)
        color_dialog.setOption(QColorDialog.ShowAlphaChannel)
        color = color_dialog.getColor(self.preferences["text_color"])
        if color.isValid():
            self.preferences["text_color"] = color
            self.update_ui_from_preferences()

    def choose_bg_color(self):
        color_dialog = QColorDialog(self)
        color_dialog.setOption(QColorDialog.ShowAlphaChannel)
        color = color_dialog.getColor(self.preferences["bg_color"])
        if color.isValid():
            self.preferences["bg_color"] = color
            self.update_ui_from_preferences()

    def choose_font(self):
        font_dialog = QFontDialog(self)
        font_dialog.setCurrentFont(self.preferences["font"])
        font, ok = font_dialog.getFont()
        if ok:
            self.preferences["font"] = font
            self.update_ui_from_preferences()

    def change_theme(self):
        selected_theme = self.theme_combobox.currentText()
        if selected_theme != self.preferences["theme"]:
            self.preferences["theme"] = selected_theme
            self.update_ui_from_preferences()

    def reset_preferences(self):
        self.preferences = {
            "text_color": QColor(0, 0, 0),
            "bg_color": QColor(255, 255, 255),
            "font": QFont(),
            "theme": "Dark",
        }
        self.update_ui_from_preferences()

    def save_preferences(self):
        text_color = self.preferences["text_color"].name()
        bg_color = self.preferences["bg_color"].name()
        font_str = f"{self.preferences['font'].family()}, {self.preferences['font'].pointSize()}"
        theme = self.preferences["theme"]

        print(f"Text Color: {text_color}")
        print(f"Background Color: {bg_color}")
        print(f"Font: {font_str}")
        print(f"Theme: {theme}")

        self.accept()


class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("About")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()

        label = QLabel("Kali Package Manager by theFest - v0.0.3")
        layout.addWidget(label)

        self.setLayout(layout)


class PackageManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Kali Package Manager")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.set_dark_theme()

        self.create_menu_bar()
        self.create_status_bar()

        self.package_label = QLabel("Package Name:")
        self.package_name_input = QLineEdit()
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_package)
        self.install_button = QPushButton("Install")
        self.install_button.clicked.connect(self.install_package)
        self.remove_button = QPushButton("Remove")
        self.remove_button.clicked.connect(self.remove_package)
        self.list_button = QPushButton("List All Packages")
        self.list_button.clicked.connect(self.list_all_packages)
        self.update_button = QPushButton("Update Package Lists")
        self.update_button.clicked.connect(self.update_package_lists)
        self.updates_button = QPushButton("Available Updates")
        self.updates_button.clicked.connect(self.list_available_updates)
        self.result_text = QTextBrowser()
        self.package_list = QListWidget()

        self.layout.addWidget(self.package_label)
        self.layout.addWidget(self.package_name_input)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.search_button)
        button_layout.addWidget(self.install_button)
        button_layout.addWidget(self.remove_button)
        button_layout.addWidget(self.list_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.updates_button)
        self.layout.addLayout(button_layout)

        self.layout.addWidget(self.result_text)
        self.layout.addWidget(self.package_list)

        self.central_widget.setLayout(self.layout)

        self.package_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.package_list.customContextMenuRequested.connect(self.show_context_menu)

        self.preferences_dialog = PreferencesDialog()
        self.preferences_dialog.accepted.connect(self.apply_preferences)

    def set_dark_theme(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)

        self.setPalette(dark_palette)

    def set_light_theme(self):
        light_palette = QPalette()
        light_palette.setColor(QPalette.Window, QColor(255, 255, 255))
        light_palette.setColor(QPalette.WindowText, Qt.black)
        light_palette.setColor(QPalette.WindowText, Qt.black)
        light_palette.setColor(QPalette.Base, QColor(240, 240, 240))
        light_palette.setColor(QPalette.AlternateBase, QColor(255, 255, 255))
        light_palette.setColor(QPalette.ToolTipBase, Qt.black)
        light_palette.setColor(QPalette.ToolTipText, Qt.black)
        light_palette.setColor(QPalette.Text, Qt.black)
        light_palette.setColor(QPalette.Button, QColor(240, 240, 240))
        light_palette.setColor(QPalette.ButtonText, Qt.black)
        light_palette.setColor(QPalette.BrightText, Qt.red)
        light_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        light_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        light_palette.setColor(QPalette.HighlightedText, Qt.white)

        self.setPalette(light_palette)

    def create_menu_bar(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        file_menu.addAction("Exit", self.close)

        edit_menu = menu_bar.addMenu("Edit")
        edit_menu.addAction("Preferences", self.show_preferences)

        help_menu = menu_bar.addMenu("Help")
        help_menu.addAction("About", self.show_about)

    def create_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def search_package(self):
        package_name = self.package_name_input.text()
        if package_name:
            result = self.run_command(["apt-cache", "show", package_name])
            self.result_text.setPlainText(result)
        else:
            self.result_text.setPlainText("Please enter a package name.")

    def install_package(self):
        package_name = self.package_name_input.text()
        if package_name:
            result = self.run_command(["sudo", "apt", "install", package_name])
            self.result_text.setPlainText(result)
        else:
            self.result_text.setPlainText("Please enter a package name.")

    def remove_package(self):
        package_name = self.package_name_input.text()
        if package_name:
            result = self.run_command(["sudo", "apt", "remove", package_name])
            self.result_text.setPlainText(result)
        else:
            self.result_text.setPlainText("Please enter a package name.")

    def list_all_packages(self):
        result = self.run_command(["apt-cache", "pkgnames"])
        packages = result.splitlines()
        self.package_list.clear()
        for package in packages:
            item = QListWidgetItem(package)
            self.package_list.addItem(item)

    def update_package_lists(self):
        result = self.run_command(["sudo", "apt", "update"])
        self.result_text.setPlainText(result)

    def list_available_updates(self):
        result = self.run_command(["apt", "list", "--upgradable"])
        self.result_text.setPlainText(result)

    def show_context_menu(self, pos):
        menu = QMenu(self)
        item = self.package_list.itemAt(pos)
        if item:
            package_name = item.text()
            info_action = QAction(f"Package Info: {package_name}", self)
            info_action.triggered.connect(lambda: self.show_package_info(package_name))
            menu.addAction(info_action)
        menu.exec_(self.mapToGlobal(pos))

    def show_package_info(self, package_name):
        if package_name:
            result = self.run_command(["apt-cache", "show", package_name])
            self.result_text.setPlainText(result)
        else:
            self.result_text.setPlainText("Please select a package from the list.")

    def show_preferences(self):
        result = self.preferences_dialog.exec_()
        if result == QDialog.Accepted:
            text_color = self.preferences_dialog.preferences["text_color"].name()
            bg_color = self.preferences_dialog.preferences["bg_color"].name()
            font_str = f"{self.preferences_dialog.preferences['font'].family()}, {self.preferences_dialog.preferences['font'].pointSize()}"
            theme = self.preferences_dialog.preferences["theme"]

            if theme == "Light":
                self.set_light_theme()
            else:
                self.set_dark_theme()

            self.result_text.setStyleSheet(
                f"color: {text_color}; background-color: {bg_color};"
            )
            self.result_text.setFont(self.preferences_dialog.preferences["font"])

    def apply_preferences(self):
        text_color = self.preferences_dialog.preferences["text_color"].name()
        bg_color = self.preferences_dialog.preferences["bg_color"].name()
        font = self.preferences_dialog.preferences["font"]
        theme = self.preferences_dialog.preferences["theme"]

        if theme == "Light":
            self.set_light_theme()
        else:
            self.set_dark_theme()

        self.result_text.setStyleSheet(
            f"color: {text_color}; background-color: {bg_color};"
        )
        self.result_text.setFont(font)

    def show_about(self):
        about_dialog = AboutDialog()
        about_dialog.exec_()

    def run_command(self, command):
        try:
            result = subprocess.run(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            if result.returncode == 0:
                return result.stdout
            else:
                return f"Error: {result.stderr}"
        except Exception as e:
            return str(e)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = PackageManagerApp()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
