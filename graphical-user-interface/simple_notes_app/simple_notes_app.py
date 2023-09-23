import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMenuBar,
    QMenu,
    QToolBar,
    QAction,
    QTextEdit,
    QVBoxLayout,
    QLabel,
    QMessageBox,
    QFontDialog,
    QColorDialog,
    QPlainTextEdit,
    QWidget,
    QFileDialog,
    QDialog,
    QListWidget,
    QListWidgetItem,
    QLineEdit,
    QPushButton,
    QInputDialog,
)
from PyQt5.QtGui import QTextCharFormat, QTextImageFormat, QTextCursor
from PyQt5.QtCore import Qt


class NoteApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.init_database()

    def init_ui(self):
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)

        self.text_edit = QTextEdit()
        self.text_edit.textChanged.connect(self.text_changed)
        layout.addWidget(self.text_edit)

        self.create_menu()
        self.create_toolbar()

        self.status_bar = self.statusBar()
        self.word_count_label = QLabel()
        self.status_bar.addWidget(self.word_count_label)
        self.current_note_label = QLabel()
        self.status_bar.addPermanentWidget(self.current_note_label)

        self.setCentralWidget(central_widget)

        self.setWindowTitle("Simple FW Notes")
        self.setGeometry(100, 100, 800, 600)

        self.current_file = None

    def init_database(self):
        self.connection = sqlite3.connect("notes.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, content TEXT)"
        )
        self.connection.commit()

    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        edit_menu = menubar.addMenu("Edit")
        view_menu = menubar.addMenu("View")
        help_menu = menubar.addMenu("Help")

        new_action = self.create_action("New", self.new_note, "Ctrl+N")
        open_action = self.create_action("Open", self.open_note, "Ctrl+O")
        save_action = self.create_action("Save", self.save_note, "Ctrl+S")
        save_as_action = self.create_action(
            "Save As...", self.save_note_as, "Ctrl+Shift+S"
        )
        exit_action = self.create_action("Exit", QApplication.quit, "Ctrl+Q")

        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        undo_action = self.create_action("Undo", self.text_edit.undo, "Ctrl+Z")
        redo_action = self.create_action("Redo", self.text_edit.redo, "Ctrl+Shift+Z")
        cut_action = self.create_action("Cut", self.text_edit.cut, "Ctrl+X")
        copy_action = self.create_action("Copy", self.text_edit.copy, "Ctrl+C")
        paste_action = self.create_action("Paste", self.text_edit.paste, "Ctrl+V")
        select_all_action = self.create_action(
            "Select All", self.text_edit.selectAll, "Ctrl+A"
        )
        find_action = self.create_action("Find", self.show_find_dialog, "Ctrl+F")
        replace_action = self.create_action(
            "Replace", self.show_replace_dialog, "Ctrl+H"
        )
        spell_check_action = self.create_action(
            "Spell Check", self.toggle_spell_check, "Ctrl+G"
        )
        view_html_action = self.create_action(
            "View HTML Source", self.view_html_source, "Ctrl+U"
        )
        insert_image_action = self.create_action(
            "Insert Image", self.insert_image, "Ctrl+I"
        )
        insert_table_action = self.create_action(
            "Insert Table", self.insert_table, "Ctrl+T"
        )

        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)
        edit_menu.addSeparator()
        edit_menu.addAction(cut_action)
        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)
        edit_menu.addSeparator()
        edit_menu.addAction(select_all_action)
        edit_menu.addSeparator()
        edit_menu.addAction(find_action)
        edit_menu.addAction(replace_action)
        edit_menu.addSeparator()
        edit_menu.addAction(spell_check_action)

        view_menu.addAction(view_html_action)
        view_menu.addAction(insert_image_action)
        view_menu.addAction(insert_table_action)

        dark_theme_action = self.create_action(
            "Dark Theme", self.toggle_dark_theme, "Ctrl+D"
        )
        view_menu.addAction(dark_theme_action)

        font_action = self.create_action("Font", self.choose_font)
        font_color_action = self.create_action("Font Color", self.choose_font_color)
        view_menu.addAction(font_action)
        view_menu.addAction(font_color_action)

        help_action = self.create_action("Help", self.show_help_dialog, "F1")
        help_menu.addAction(help_action)

    def create_toolbar(self):
        formatting_toolbar = QToolBar("Formatting Toolbar")
        self.addToolBar(Qt.BottomToolBarArea, formatting_toolbar)

        bold_action = self.create_action("Bold", self.toggle_bold, "Ctrl+B")
        italic_action = self.create_action("Italic", self.toggle_italic, "Ctrl+I")
        underline_action = self.create_action(
            "Underline", self.toggle_underline, "Ctrl+U"
        )
        font_size_action = self.create_action("Font Size", self.choose_font_size)
        font_color_action = self.create_action("Font Color", self.choose_font_color)

        formatting_toolbar.addAction(bold_action)
        formatting_toolbar.addAction(italic_action)
        formatting_toolbar.addAction(underline_action)
        formatting_toolbar.addAction(font_size_action)
        formatting_toolbar.addAction(font_color_action)

        find_replace_toolbar = QToolBar("Find and Replace")
        self.addToolBar(Qt.BottomToolBarArea, find_replace_toolbar)

        find_action = self.create_action("Find", self.show_find_dialog, "Ctrl+F")
        replace_action = self.create_action(
            "Replace", self.show_replace_dialog, "Ctrl+H"
        )

        find_replace_toolbar.addAction(find_action)
        find_replace_toolbar.addAction(replace_action)

    def create_action(self, text, slot, shortcut=None):
        action = QAction(text, self)
        action.triggered.connect(slot)
        if shortcut:
            action.setShortcut(shortcut)
        return action

    def toggle_bold(self):
        char_format = QTextCharFormat()
        char_format.setFontWeight(
            QFont.Bold if self.text_edit.fontWeight() != QFont.Bold else QFont.Normal
        )
        self.text_edit.mergeCurrentCharFormat(char_format)

    def toggle_italic(self):
        char_format = QTextCharFormat()
        char_format.setFontItalic(not self.text_edit.fontItalic())
        self.text_edit.mergeCurrentCharFormat(char_format)

    def toggle_underline(self):
        char_format = QTextCharFormat()
        char_format.setFontUnderline(not self.text_edit.fontUnderline())
        self.text_edit.mergeCurrentCharFormat(char_format)

    def toggle_spell_check(self):
        self.text_edit.setAcceptRichText(not self.text_edit.acceptRichText())

    def choose_font(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.text_edit.setCurrentFont(font)

    def choose_font_size(self):
        size, ok = QInputDialog.getInt(
            self,
            "Font Size",
            "Enter font size:",
            self.text_edit.fontPointSize(),
            1,
            100,
        )
        if ok:
            char_format = QTextCharFormat()
            char_format.setFontPointSize(size)
            self.text_edit.mergeCurrentCharFormat(char_format)

    def choose_font_color(self):
        color = QColorDialog.getColor(self.text_edit.textColor(), self)
        if color.isValid():
            char_format = QTextCharFormat()
            char_format.setForeground(color)
            self.text_edit.mergeCurrentCharFormat(char_format)

    def update_word_count(self):
        text = self.text_edit.toPlainText()
        word_count = len(text.split())
        self.word_count_label.setText(f"Word Count: {word_count}")

    def text_changed(self):
        self.update_word_count()

    def new_note(self):
        if self.text_edit.toPlainText() and not self.ask_to_save():
            return

        self.text_edit.clear()
        self.current_file = None
        self.update_word_count()
        self.current_note_label.clear()

    def open_note(self):
        if self.text_edit.toPlainText() and not self.ask_to_save():
            return

        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Note", "", "Text Files (*.txt);;All Files (*)", options=options
        )
        if file_name:
            with open(file_name, "r") as file:
                self.text_edit.setPlainText(file.read())
                self.update_word_count()
                self.current_note_label.setText(f"Current Note: {file_name}")
                self.current_file = file_name

    def save_note(self):
        if not self.text_edit.toPlainText():
            return

        if self.current_file:
            file_name = self.current_file
            with open(file_name, "w") as file:
                file.write(self.text_edit.toPlainText())
                self.update_word_count()
                self.current_note_label.setText(f"Current Note: {file_name}")
        else:
            self.save_note_as()

    def save_note_as(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save Note As",
            "",
            "Text Files (*.txt);;All Files (*)",
            options=options,
        )

        if file_name:
            with open(file_name, "w") as file:
                file.write(self.text_edit.toPlainText())
                self.update_word_count()
                self.current_note_label.setText(f"Current Note: {file_name}")
                self.current_file = file_name

    def ask_to_save(self):
        reply = QMessageBox.question(
            self,
            "Save Changes?",
            "Do you want to save changes to the current note?",
            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
            QMessageBox.Save,
        )

        if reply == QMessageBox.Save:
            self.save_note()
            return True
        elif reply == QMessageBox.Discard:
            return True
        elif reply == QMessageBox.Cancel:
            return False
        return True

    def show_find_dialog(self):
        find_dialog = FindDialog(self)
        find_dialog.exec_()

    def show_replace_dialog(self):
        replace_dialog = ReplaceDialog(self)
        replace_dialog.exec_()

    def view_html_source(self):
        html_source = self.text_edit.toHtml()
        source_dialog = QDialog(self)
        source_dialog.setWindowTitle("HTML Source")
        source_dialog.setGeometry(100, 100, 800, 600)

        source_layout = QVBoxLayout(source_dialog)
        source_text_edit = QPlainTextEdit(source_dialog)
        source_text_edit.setPlainText(html_source)

        source_layout.addWidget(source_text_edit)
        source_dialog.setLayout(source_layout)

        source_dialog.exec_()

    def insert_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Insert Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.gif *.bmp)",
            options=options,
        )
        if file_name:
            cursor = self.text_edit.textCursor()
            image_format = QTextImageFormat()
            image_format.setName(file_name)
            image_format.setWidth(300)
            image_format.setHeight(200)
            cursor.insertImage(image_format)

    def insert_table(self):
        table_dialog = TableDialog(self)
        if table_dialog.exec_():
            rows = table_dialog.get_rows()
            cols = table_dialog.get_columns()
            cursor = self.text_edit.textCursor()
            table_format = QTextTableFormat()
            table_format.setCellPadding(4)
            table_format.setCellSpacing(0)
            table_format.setAlignment(Qt.AlignLeft)
            cursor.insertTable(rows, cols, table_format)

    def toggle_dark_theme(self):
        app_style = """
            QMainWindow {
                background-color: #1e1e1e;
                color: #f0f0f0;
            }
            QMenuBar {
                background-color: #1e1e1e;
                color: #f0f0f0;
            }
            QMenuBar::item {
                background-color: #1e1e1e;
                color: #f0f0f0;
                padding: 4px 8px;
                border-radius: 4px;
            }
            QMenuBar::item:selected {
                background-color: #474747;
            }
            QMenu {
                background-color: #1e1e1e;
                color: #f0f0f0;
                border: 1px solid #474747;
            }
            QMenu::item {
                background-color: transparent;
                padding: 6px 20px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #474747;
            }
            QToolBar {
                background-color: #1e1e1e;
                border: none;
                spacing: 10px;
            }
            QPushButton {
                background-color: #474747;
                color: #f0f0f0;
                border: 1px solid #474747;
                padding: 6px 20px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #333333;
            }
            QLineEdit {
                background-color: #333333;
                color: #f0f0f0;
                padding: 6px 10px;
                border: 1px solid #474747;
                border-radius: 4px;
            }
            QTextEdit {
                background-color: #333333;
                color: #f0f0f0;
                border: 1px solid #474747;
                border-radius: 4px;
                padding: 6px;
            }
        """
        self.setStyleSheet(app_style)

    def show_help_dialog(self):
        help_text = """
        Simple FW Notes
        
        This is a simple note-taking application with basic formatting options.

        File Menu:
        - New (Ctrl+N): Create a new note.
        - Open (Ctrl+O): Open an existing note.
        - Save (Ctrl+S): Save the current note.
        - Save As... (Ctrl+Shift+S): Save the current note with a new name.
        - Exit (Ctrl+Q): Exit the application.

        Edit Menu:
        - Undo (Ctrl+Z): Undo the last action.
        - Redo (Ctrl+Shift+Z): Redo the last undone action.
        - Cut (Ctrl+X): Cut the selected text.
        - Copy (Ctrl+C): Copy the selected text.
        - Paste (Ctrl+V): Paste the copied or cut text.
        - Select All (Ctrl+A): Select all the text in the note.
        - Find (Ctrl+F): Find text in the note.
        - Replace (Ctrl+H): Replace text in the note.
        - Spell Check (Ctrl+G): Toggle spell check.
        
        View Menu:
        - View HTML Source (Ctrl+U): View the HTML source of the note.
        - Insert Image (Ctrl+I): Insert an image into the note.
        - Insert Table (Ctrl+T): Insert a table into the note.
        - Dark Theme (Ctrl+D): Toggle dark theme for the application.
        - Font: Change the font for the text.
        - Font Color: Change the font color for the text.

        Formatting Toolbar (Bottom):
        - Bold (Ctrl+B): Toggle bold text.
        - Italic (Ctrl+I): Toggle italic text.
        - Underline (Ctrl+U): Toggle underline text.
        - Font Size: Change the font size.
        - Font Color: Change the font color.

        Find and Replace Toolbar (Bottom):
        - Find (Ctrl+F): Find text in the note.
        - Replace (Ctrl+H): Replace text in the note.

        Help Menu:
        - Help (F1): Show this help message.
        """
        QMessageBox.information(self, "Help", help_text)


class FindDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Find")
        self.setGeometry(100, 100, 400, 100)

        layout = QVBoxLayout()

        self.find_input = QLineEdit()
        self.find_input.setPlaceholderText("Find text...")
        layout.addWidget(self.find_input)

        find_button = QPushButton("Find")
        find_button.clicked.connect(self.find_text)
        layout.addWidget(find_button)

        self.results_list = QListWidget()
        self.results_list.itemDoubleClicked.connect(self.go_to_result)
        layout.addWidget(self.results_list)

        self.setLayout(layout)

    def find_text(self):
        text = self.find_input.text()
        if text:
            self.results_list.clear()
            cursor = self.parent().text_edit.document().find(text)
            while cursor.hasSelection():
                item = QListWidgetItem(cursor.selectedText())
                self.results_list.addItem(item)
                cursor = self.parent().text_edit.document().find(text, cursor)

    def go_to_result(self, item):
        text_widget = self.parent().text_edit
        cursor = text_widget.textCursor()
        cursor.setPosition(text_widget.document().find(item.text()).position())
        text_widget.setTextCursor(cursor)
        self.accept()


class ReplaceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Replace")
        self.setGeometry(100, 100, 400, 150)

        layout = QVBoxLayout()

        self.find_input = QLineEdit()
        self.find_input.setPlaceholderText("Find text...")
        layout.addWidget(self.find_input)

        self.replace_input = QLineEdit()
        self.replace_input.setPlaceholderText("Replace with...")
        layout.addWidget(self.replace_input)

        find_button = QPushButton("Find")
        find_button.clicked.connect(self.find_text)
        layout.addWidget(find_button)

        replace_button = QPushButton("Replace")
        replace_button.clicked.connect(self.replace_text)
        layout.addWidget(replace_button)

        self.results_list = QListWidget()
        self.results_list.itemDoubleClicked.connect(self.go_to_result)
        layout.addWidget(self.results_list)

        self.setLayout(layout)

    def find_text(self):
        text = self.find_input.text()
        if text:
            self.results_list.clear()
            cursor = self.parent().text_edit.document().find(text)
            while cursor.hasSelection():
                item = QListWidgetItem(cursor.selectedText())
                self.results_list.addItem(item)
                cursor = self.parent().text_edit.document().find(text, cursor)

    def replace_text(self):
        text_widget = self.parent().text_edit
        cursor = text_widget.textCursor()
        text = text_widget.toPlainText()

        find_text = self.find_input.text()
        replace_text = self.replace_input.text()

        new_text = text.replace(find_text, replace_text)

        cursor.beginEditBlock()
        cursor.select(QTextCursor.Document)
        cursor.removeSelectedText()
        cursor.insertText(new_text)
        cursor.endEditBlock()

        self.find_text()

    def go_to_result(self, item):
        text_widget = self.parent().text_edit
        cursor = text_widget.textCursor()
        cursor.setPosition(text_widget.document().find(item.text()).position())
        text_widget.setTextCursor(cursor)
        self.accept()


class TableDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Insert Table")
        self.setGeometry(100, 100, 300, 100)

        layout = QVBoxLayout()

        self.rows_input = QLineEdit()
        self.rows_input.setPlaceholderText("Rows")
        layout.addWidget(self.rows_input)

        self.columns_input = QLineEdit()
        self.columns_input.setPlaceholderText("Columns")
        layout.addWidget(self.columns_input)

        insert_button = QPushButton("Insert")
        insert_button.clicked.connect(self.accept)
        layout.addWidget(insert_button)

        self.setLayout(layout)

    def get_rows(self):
        return int(self.rows_input.text())

    def get_columns(self):
        return int(self.columns_input.text())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = NoteApp()
    window.show()
    sys.exit(app.exec_())
