import string

from PySide6.QtWidgets import (QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QPushButton,
                               QLabel, QFileDialog, QTextEdit, QMessageBox, QApplication,
                               QColorDialog, QMainWindow, QFontComboBox, QSpinBox,
                               QFrame, QSizePolicy, QInputDialog, QFontDialog)
import sys
from PySide6.QtCore import QFile, QTextStream, QIODevice, QSettings, Qt
from PySide6.QtGui import QIcon, QAction, QFont, QPalette, QColor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("T-Pad")
        app_icon = QIcon("images/app_icon.png")
        self.setWindowIcon(app_icon)
        self.settings = QSettings("Settings", "T-Pad")
        self.defaultPalette = QApplication.palette()
        self.darkModeEnabled = False

        #Mainwindow central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        #Layouts
        main_layout = QGridLayout(central_widget)
        main_button_layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        bottom_button_layout = QHBoxLayout()

        #Icon declarations
        save_icon = QIcon("images/save_icon.png")
        open_icon = QIcon("images/open_icon.png")
        quit_icon = QIcon("images/quit_icon.png")
        settings_icon = QIcon("images/settings_icon.png")
        pref_icon = QIcon("images/pref_icon.png")
        dark_mode_icon = QIcon("images/dark_mode_icon.png")
        about_app_icon = QIcon("images/about_icon.png")
        about_qt_icon = QIcon("images/about_qt_icon.png")
        copy_icon = QIcon("images/copy_icon.png")
        cut_icon = QIcon("images/cut_icon.png")
        paste_icon = QIcon("images/paste_icon.png")
        undo_icon = QIcon("images/undo_icon.png")
        redo_icon = QIcon("images/redo_icon.png")
        clear_icon = QIcon("images/clear_icon.png")
        quit_icon = QIcon("images/quit_icon.png")
        bold_icon = QIcon("images/bold_icon.png")
        underline_icon = QIcon("images/underline_icon.png")
        italic_icon = QIcon("images/italic_icon.png")
        color_icon = QIcon("images/font_color_icon.png")
        find_replace_icon = QIcon("images/replace_icon.png")

        #Menubar menus
        menu_bar = self.menuBar()
        self.file_menu = menu_bar.addMenu("File")
        self.edit_menu = menu_bar.addMenu("Edit")
        self.help_menu = menu_bar.addMenu("Help")

        #File menu actions
        save_action = QAction("Save File", self)
        save_action.setIcon(save_icon)
        save_action.triggered.connect(self.save_clicked)
        open_action = QAction("Open File", self)
        open_action.setIcon(open_icon)
        open_action.triggered.connect(self.open_clicked)
        quit_action = QAction("Exit", self)
        quit_action.setIcon(quit_icon)
        quit_action.triggered.connect(self.quit_app)
        self.file_menu.addAction(save_action)
        self.file_menu.addAction(open_action)
        self.file_menu.addSeparator()

        #Settings menu
        self.settings_menu = self.file_menu.addMenu("Settings")
        self.settings_menu.setIcon(settings_icon)

        #Settings menu actions
        change_pref_action = QAction("Font Preset", self)
        change_pref_action.setIcon(pref_icon)
        change_pref_action.triggered.connect(self.change_pref)
        self.dark_mode_action = QAction("Dark Mode", self)
        self.dark_mode_action.setIcon(dark_mode_icon)
        self.dark_mode_action.triggered.connect(self.toggle_dark_mode)
        self.settings_menu.addAction(change_pref_action)
        self.settings_menu.addAction(self.dark_mode_action)
        self.file_menu.addSeparator()

        #Help menu actions
        about_app = QAction("About Application", self)
        about_app.setIcon(about_app_icon)
        about_app.triggered.connect(self.about_app)
        about_qt = QAction("About Qt", self)
        about_qt.setIcon(about_qt_icon)
        about_qt.triggered.connect(self.about_qt)
        self.help_menu.addAction(about_app)
        self.help_menu.addAction(about_qt)

        #Edit menu replace action
        find_replace_action = QAction("Find and Replace", self)
        find_replace_action.setIcon(find_replace_icon)
        find_replace_action.triggered.connect(self.find_replace)
        self.edit_menu.addSeparator()
        self.edit_menu.addAction(find_replace_action)

        #Initializing text edit widget
        self.text_edit = QTextEdit()
        self.text_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.text_edit.textChanged.connect(self.update_char_count)
        self.text_edit.textChanged.connect(self.update_word_count)
        self.text_edit.textChanged.connect(self.update_line_count)

        #Text edit buttons and edit menu actions
        copy_button = QPushButton()
        copy_button.setIcon(copy_icon)
        copy_button.clicked.connect(self.text_edit.copy)
        copy_button.setToolTip("Copy the selected text.")

        copy_action = QAction("Copy", self)
        copy_action.setIcon(copy_icon)
        copy_action.triggered.connect(self.text_edit.copy)
        self.edit_menu.addAction(copy_action)

        cut_button = QPushButton()
        cut_button.setIcon(cut_icon)
        cut_button.setToolTip("Cut the selected text.")
        cut_button.clicked.connect(self.text_edit.cut)

        cut_action = QAction("Cut", self)
        cut_action.setIcon(cut_icon)
        cut_action.triggered.connect(self.text_edit.cut)
        self.edit_menu.addAction(cut_action)

        paste_button = QPushButton()
        paste_button.setIcon(paste_icon)
        paste_button.setToolTip("Paste previously copied text.")
        paste_button.clicked.connect(self.text_edit.paste)

        paste_action = QAction("Paste", self)
        paste_action.setIcon(paste_icon)
        paste_action.triggered.connect(self.text_edit.paste)
        self.edit_menu.addAction(paste_action)

        undo_button = QPushButton()
        undo_button.setIcon(undo_icon)
        undo_button.setToolTip("Undo the last change made.")
        undo_button.clicked.connect(self.text_edit.undo)

        undo_action = QAction("Undo", self)
        undo_action.setIcon(undo_icon)
        undo_action.triggered.connect(self.text_edit.undo)
        self.edit_menu.addAction(undo_action)

        redo_button = QPushButton()
        redo_button.setIcon(redo_icon)
        redo_button.setToolTip("Redo the last change.")
        redo_button.clicked.connect(self.text_edit.redo)

        redo_action = QAction("Redo", self)
        redo_action.setIcon(redo_icon)
        redo_action.triggered.connect(self.text_edit.redo)
        self.edit_menu.addAction(redo_action)

        clear_button = QPushButton()
        clear_button.setIcon(clear_icon)
        clear_button.setToolTip("Clear the current file.")
        clear_button.clicked.connect(self.text_edit.clear)

        #File menu clear action
        clear_action = QAction("Clear", self)
        clear_action.setIcon(clear_icon)
        clear_action.triggered.connect(self.text_edit.clear)
        self.file_menu.addAction(clear_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(quit_action)

        #Text editing buttons
        bold_button = QPushButton()
        bold_button.setIcon(bold_icon)
        bold_button.setToolTip("Set the current text to bold.")
        bold_button.clicked.connect(self.bold_clicked)

        underline_button = QPushButton()
        underline_button.setIcon(underline_icon)
        underline_button.setToolTip("Underline the current text.")
        underline_button.clicked.connect(self.underline_clicked)

        italic_button = QPushButton()
        italic_button.setIcon(italic_icon)
        italic_button.setToolTip("Set the current text to italics.")
        italic_button.clicked.connect(self.italic_clicked)

        color_button = QPushButton()
        color_button.setIcon(color_icon)
        color_button.setToolTip("Change the selected font's color.")
        color_button.clicked.connect(self.change_color_clicked)

        #Separator
        button_separator = QFrame()
        button_separator.setFrameShape(QFrame.VLine)
        button_separator.setFrameShadow(QFrame.Sunken)

        #Button layout
        button_layout.addWidget(copy_button)
        button_layout.addWidget(cut_button)
        button_layout.addWidget(paste_button)
        button_layout.addWidget(undo_button)
        button_layout.addWidget(redo_button)
        button_layout.addWidget(clear_button)
        button_layout.addWidget(button_separator)
        button_layout.addWidget(color_button)
        button_layout.addWidget(bold_button)
        button_layout.addWidget(underline_button)
        button_layout.addWidget(italic_button)
        button_layout.addStretch(1)

        #Font combo box
        self.font_box = QFontComboBox()
        self.font_box.setToolTip("Change the current font.")
        self.font_box.setMaxVisibleItems(5)
        self.font_box.currentFontChanged.connect(self.font_changed)

        #Font size spin box
        self.size_box = QSpinBox()
        self.size_box.setToolTip("Change the font's current size.")
        self.size_box.setRange(1, 72)
        self.size_box.setValue(12)
        self.size_box.valueChanged.connect(self.change_size)

        #Font preset
        fontstr = self.settings.value('font')
        if fontstr:
            font = QFont()
            font.fromString(fontstr)
            self.text_edit.setCurrentFont(font)
            self.text_edit.setFont(font)
            self.text_edit.setFontPointSize(font.pointSize())
            self.font_box.setCurrentText(font.family())
            self.size_box.setValue(font.pointSize())

        #Bottom button layout
        bottom_button_layout.addWidget(self.font_box)
        bottom_button_layout.addWidget(self.size_box)
        bottom_button_layout.addStretch(1)

        #Main layout
        main_button_layout.addLayout(button_layout)
        main_button_layout.addLayout(bottom_button_layout)

        #Status bar with count labels
        status_bar = self.statusBar()
        self.char_count_label = QLabel("Character Count: 0")
        self.word_count_label = QLabel("Word Count: 0")
        self.line_count_label = QLabel("Line Count: 1")
        count_separator = QFrame()
        count_separator.setFrameShape(QFrame.VLine)
        count_separator.setFrameShadow(QFrame.Sunken)
        count_separator2 = QFrame()
        count_separator2.setFrameShape(QFrame.VLine)
        count_separator2.setFrameShadow(QFrame.Sunken)
        status_bar.addWidget(self.char_count_label)
        status_bar.addWidget(count_separator)
        status_bar.addWidget(self.word_count_label)
        status_bar.addWidget(count_separator2)
        status_bar.addWidget(self.line_count_label)
        self.setStatusBar(status_bar)

        main_layout.addLayout(button_layout, 0, 0)
        main_layout.addLayout(main_button_layout, 1, 0)
        main_layout.addWidget(self.text_edit, 2, 0)

    def enable_dark_mode(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        QApplication.instance().setPalette(dark_palette)

    def toggle_dark_mode(self):
        app = QApplication.instance()
        if self.darkModeEnabled:
            app.setPalette(self.defaultPalette)
            self.darkModeEnabled = False
        else:
            self.enable_dark_mode()
            self.darkModeEnabled = True

    def change_pref(self):
        ok, font = QFontDialog.getFont()
        if ok:
            fontStr = font.toString()
            self.settings.setValue('font', fontStr)
            self.text_edit.setCurrentFont(font)
            self.font_box.setCurrentText(font.family())
            self.size_box.setValue(font.pointSize())

    def find_replace(self):
        text, ok = QInputDialog.getText(self, "Find and Replace",
                                        "Find:")
        if ok and text:
            replace_text, ok2 = QInputDialog.getText(self, "Find and Replace",
                                                     "Replace " + text + " with:")
        if ok and ok2 and text and replace_text:
            replaced = self.text_edit.toPlainText().replace(text, replace_text)
            self.text_edit.setPlainText(replaced)

    def about_app(self):
        QMessageBox.about(self, "Application Details", "This application is essentially a notepad with\n"
                                                       "features such as font selection, color selection, and\n"
                                                       "other text editing functionality.\n"
                                                       "\nTyler Hummel created this app using PySide6 in the\n"
                                                       "PyCharm IDE.")

    def about_qt(self):
        QApplication.aboutQt()

    def quit_app(self):
        QApplication.instance().exit()

    def update_line_count(self):
        line_count = 1
        for i in self.text_edit.toPlainText():
            if i == "\n":
                line_count += 1
        self.line_count_label.setText(f"Line Count: {line_count}")

    def update_word_count(self):
        text = self.text_edit.toPlainText().strip()
        table = str.maketrans('', '', string.punctuation)
        clean_words = text.translate(table)
        words = clean_words.split()
        word_count = len(words)
        self.word_count_label.setText(f"Word Count: {word_count}")

    def update_char_count(self):
        self.char_count_label.setText(f"Character Count: {str(len(self.text_edit.toPlainText().strip()))}")

    def italic_clicked(self):
        font = self.text_edit.currentFont()
        font.setItalic(not font.italic())
        self.text_edit.setCurrentFont(font)

    def bold_clicked(self):
        font = self.text_edit.currentFont()
        font.setBold(not font.bold())
        self.text_edit.setCurrentFont(font)

    def underline_clicked(self):
        font = self.text_edit.currentFont()
        font.setUnderline(not font.underline())
        self.text_edit.setCurrentFont(font)

    def font_changed(self):
        font = self.font_box.currentFont()
        self.text_edit.setCurrentFont(font)
        self.text_edit.setFont(font)

    def change_size(self, value):
        font = self.text_edit.currentFont()
        font.setPointSize(value)
        self.text_edit.setCurrentFont(font)
        self.text_edit.setFontPointSize(value)
        self.text_edit.setFont(font)

    def change_color_clicked(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.text_edit.setTextColor(color)

    def save_clicked(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "/home/",
                                                   "Text(*.txt);; All Files (*.txt)")

        if file_name == "":
            return
        file = QFile(file_name)
        if not file.open(QIODevice.WriteOnly | QIODevice.Text):
            return
        out = QTextStream(file)
        out << self.text_edit.toPlainText() << "\n"
        file.close()
        QMessageBox.information(self, "File Saved", "File saved successfully.")

    def open_clicked(self):
        file_content = ""
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "/home/",
                                                   "Text(*.txt);; All Files (*.*)")
        if file_name == "":
            return
        file = QFile(file_name)
        if not file.open(QIODevice.ReadOnly | QIODevice.Text):
            return
        in_stream = QTextStream(file)
        while not in_stream.atEnd():
            line = in_stream.readLine()
            file_content += line
            file_content += "\n"
        file.close()
        self.text_edit.clear()
        self.text_edit.setText(file_content)

app = QApplication(sys.argv)
app.setStyle("fusion")
mainwindow = MainWindow()
mainwindow.show()
app.exec()