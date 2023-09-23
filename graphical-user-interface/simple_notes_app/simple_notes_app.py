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
    QStatusBar,
    QLabel,
    QDialog,
    QToolBar,
    QListWidget,
    QListWidgetItem,
    QMenu,
    QActionGroup,
)
from PyQt5.QtGui import QTextCursor, QIcon


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

        toolbar = QToolBar("Formatting Toolbar")
        layout.addWidget(toolbar)

        bold_action = self.create_action(
            "Bold", self.toggle_bold, "Ctrl+B", icon="bold.png"
        )
        italic_action = self.create_action(
            "Italic", self.toggle_italic, "Ctrl+I", icon="italic.png"
        )
        underline_action = self.create_action(
            "Underline", self.toggle_underline, "Ctrl+U", icon="underline.png"
        )
        toolbar.addAction(bold_action)
        toolbar.addAction(italic_action)
        toolbar.addAction(underline_action)

        # Add Cut, Copy, Paste, Undo, Redo, Select All actions
        cut_action = self.create_action(
            "Cut", self.text_edit.cut, "Ctrl+X", icon="cut.png"
        )
        copy_action = self.create_action(
            "Copy", self.text_edit.copy, "Ctrl+C", icon="copy.png"
        )
        paste_action = self.create_action(
            "Paste", self.text_edit.paste, "Ctrl+V", icon="paste.png"
        )
        undo_action = self.create_action(
            "Undo", self.text_edit.undo, "Ctrl+Z", icon="undo.png"
        )
        redo_action = self.create_action(
            "Redo", self.text_edit.redo, "Ctrl+Shift+Z", icon="redo.png"
        )
        select_all_action = self.create_action(
            "Select All", self.text_edit.selectAll, "Ctrl+A", icon="select_all.png"
        )
        toolbar.addActions(
            [
                cut_action,
                copy_action,
                paste_action,
                undo_action,
                redo_action,
                select_all_action,
            ]
        )

        self.status_bar = QStatusBar()
        self.word_count_label = QLabel()
        self.status_bar.addWidget(self.word_count_label)
        self.current_note_label = QLabel()
        self.status_bar.addPermanentWidget(self.current_note_label)
        self.setStatusBar(self.status_bar)

        self.setCentralWidget(central_widget)

        # Create a menu bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        file_menu.addAction(
            self.create_action("New", self.new_note, "Ctrl+N", icon="new.png")
        )
        file_menu.addAction(
            self.create_action("Open", self.open_note, "Ctrl+O", icon="open.png")
        )
        file_menu.addAction(
            self.create_action("Save", self.save_note, "Ctrl+S", icon="save.png")
        )
        file_menu.addAction(
            self.create_action(
                "Save As...", self.save_note_as, "Ctrl+Shift+S", icon="save_as.png"
            )
        )
        file_menu.addSeparator()
        file_menu.addAction(
            self.create_action("Exit", qApp.quit, "Ctrl+Q", icon="exit.png")
        )

        self.setWindowTitle("Simple Notes")
        self.setGeometry(100, 100, 800, 600)

    def init_database(self):
        self.connection = sqlite3.connect("notes.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, content TEXT)"
        )
        self.connection.commit()

    def create_action(self, text, slot, shortcut=None, icon=None):
        action = QAction(text, self)
        action.triggered.connect(slot)
        if shortcut:
            action.setShortcut(shortcut)
        if icon:
            action.setIcon(QIcon(icon))
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

    def save_note(self):
        if not self.text_edit.toPlainText():
            return

        if hasattr(self, "current_file"):
            file_name = self.current_file
            with open(file_name, "w") as file:
                file.write(self.text_edit.toPlainText())
                self.update_word_count()
                self.current_note_label.setText(f"Current Note: {file_name}")

        self.save_to_database()

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
                self.current_file = file_name
                self.update_word_count()
                self.current_note_label.setText(f"Current Note: {file_name}")

    def show_notes_list(self):
        notes_list = NotesListDialog(self.connection, self.load_from_database)
        notes_list.exec_()

    def closeEvent(self, event):
        self.connection.close()
        event.accept()


class NotesListDialog(QDialog):
    def __init__(self, connection, load_note_callback):
        super().__init__()

        self.connection = connection
        self.load_note_callback = load_note_callback
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Notes List")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()

        self.notes_list_widget = QListWidget()
        self.populate_notes_list()
        self.notes_list_widget.itemDoubleClicked.connect(self.load_note)

        layout.addWidget(self.notes_list_widget)

        self.setLayout(layout)

    def populate_notes_list(self):
        self.notes_list_widget.clear()
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT id FROM notes")
        notes = self.cursor.fetchall()
        for note in notes:
            item = QListWidgetItem(f"Note ID: {note[0]}")
            self.notes_list_widget.addItem(item)

    def load_note(self, item):
        note_id = int(item.text().split()[-1])
        self.load_note_callback(note_id)
        self.accept()


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
