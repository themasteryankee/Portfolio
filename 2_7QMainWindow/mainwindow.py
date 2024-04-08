from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui_widget import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, app):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Text Editor")
        self.app = app

        self.actionQuit.triggered.connect(self.quit)
        self.actionCut.triggered.connect(self.cut)
        self.actionReo.triggered.connect(self.redo)
        self.actionPaste.triggered.connect(self.paste)
        self.actionUndo.triggered.connect(self.undo)
        self.actionCopy.triggered.connect(self.copy)
        self.actionAbout.triggered.connect(self.about)
        self.actionAbout_Qt.triggered.connect(self.aboutQt)

    def quit(self):
        self.app.quit()

    def copy(self):
        self.textEdit.copy()

    def cut(self):
        self.textEdit.cut()

    def paste(self):
        self.textEdit.paste()

    def redo(self):
        self.textEdit.redo()

    def undo(self):
        self.textEdit.undo()

    def about(self):
        QMessageBox.information(self, "Hello, world!", "My name is Tyler, and I'm teaching myself how to create GUIs\n"
                                                       "using PySide6 and Qt Designer.",
                                QMessageBox.Ok)

    def aboutQt(self):
        QApplication.aboutQt()