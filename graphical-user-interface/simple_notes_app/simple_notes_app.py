import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTextEdit,
    QAction,
    qApp,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QMenuBar,
    QMenu,
    QToolBar,
    QListWidget,
    QListWidgetItem,
    QDialog,
    QLineEdit,
    QPushButton,
    QLabel,
)
from PyQt5.QtGui import QTextCursor


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

        self.setWindowTitle("Simple Notes")
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

        new_action = self.create_action("New", self.new_note, "Ctrl+N")
        open_action = self.create_action("Open", self.open_note, "Ctrl+O")
        save_action = self.create_action("Save", self.save_note, "Ctrl+S")
        save_as_action = self.create_action(
            "Save As...", self.save_note_as, "Ctrl+Shift+S"
        )
        exit_action = self.create_action("Exit", qApp.quit, "Ctrl+Q")

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

    def create_toolbar(self):
        toolbar = QToolBar("Formatting Toolbar")
        self.addToolBar(toolbar)

        bold_action = self.create_action("Bold", self.toggle_bold, "Ctrl+B")
        italic_action = self.create_action("Italic", self.toggle_italic, "Ctrl+I")
        underline_action = self.create_action(
            "Underline", self.toggle_underline, "Ctrl+U"
        )

        toolbar.addAction(bold_action)
        toolbar.addAction(italic_action)
        toolbar.addAction(underline_action)

        find_replace_toolbar = QToolBar("Find and Replace")
        self.addToolBar(find_replace_toolbar)

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
        self.text_edit.setFontWeight(QTextCursor.Bold)

    def toggle_italic(self):
        self.text_edit.setFontItalic(not self.text_edit.fontItalic())

    def toggle_underline(self):
        self.text_edit.setFontUnderline(not self.text_edit.fontUnderline())

    def update_word_count(self):
        text = self.text_edit.toPlainText()
        word_count = len(text.split())
        self.word_count_label.setText(f"Word Count: {word_count}")

    def text_changed(self):
        self.update_word_count()

    def new_note(self):
        self.text_edit.clear()
        self.current_file = None
        self.update_word_count()
        self.current_note_label.clear()

    def open_note(self):
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

    def show_find_dialog(self):
        find_dialog = FindDialog(self)
        find_dialog.exec_()

    def show_replace_dialog(self):
        replace_dialog = ReplaceDialog(self)
        replace_dialog.exec_()

    def save_to_database(self):
        content = self.text_edit.toPlainText()
        self.cursor.execute("INSERT INTO notes (content) VALUES (?)", (content,))
        self.connection.commit()
        self.current_note_label.setText("Current Note: Saved to Database")

    def load_from_database(self, note_id):
        self.cursor.execute("SELECT content FROM notes WHERE id = ?", (note_id,))
        note_content = self.cursor.fetchone()
        if note_content:
            self.text_edit.setPlainText(note_content[0])
            self.update_word_count()
            self.current_note_label.setText(f"Current Note: ID {note_id}")

    def show_notes_list(self):
        notes_list = NotesListDialog(self.connection, self.load_from_database)
        notes_list.exec_()

    def closeEvent(self, event):
        self.connection.close()
        event.accept()


class FindDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Find")
        self.setGeometry(300, 300, 300, 100)
        layout = QVBoxLayout()

        self.find_text_edit = QLineEdit()
        find_button = QPushButton("Find")
        find_button.clicked.connect(self.find_text)

        layout.addWidget(self.find_text_edit)
        layout.addWidget(find_button)

        self.setLayout(layout)

    def find_text(self):
        text_to_find = self.find_text_edit.text()
        text = self.parent().text_edit.toPlainText()
        cursor = self.parent().text_edit.textCursor()
        found_cursor = cursor.document().find(text_to_find, cursor)
        if found_cursor.hasSelection():
            self.parent().text_edit.setTextCursor(found_cursor)


class ReplaceDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Replace")
        self.setGeometry(300, 300, 300, 150)
        layout = QVBoxLayout()

        self.find_text_edit = QLineEdit()
        self.replace_text_edit = QLineEdit()
        replace_button = QPushButton("Replace")
        replace_button.clicked.connect(self.replace_text)

        layout.addWidget(self.find_text_edit)
        layout.addWidget(self.replace_text_edit)
        layout.addWidget(replace_button)

        self.setLayout(layout)

    def replace_text(self):
        text_to_find = self.find_text_edit.text()
        text_to_replace = self.replace_text_edit.text()
        text = self.parent().text_edit.toPlainText()
        text = text.replace(text_to_find, text_to_replace)
        self.parent().text_edit.setPlainText(text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dark_theme = """
        QMainWindow { background-color: #2E2E2E; color: white; }
        QTextEdit { background-color: #1E1E1E; color: white; }
        QMenuBar { background-color: #2E2E2E; color: white; }
        QMenu { background-color: #2E2E2E; color: white; }
        QMenu::item:selected { background-color: #3E3E3E; }
        QMenuBar::item:selected { background-color: #3E3E3E; }
    """
    app.setStyleSheet(dark_theme)

    main_win = NoteApp()
    main_win.show()
    sys.exit(app.exec_())
