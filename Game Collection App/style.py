from PySide6.QtWidgets import QMessageBox, QStyle, QWidget, QLabel
from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import (QColor, QPainter, QTextCursor, QLinearGradient, QTextCharFormat, QBrush)

class DarkMessage(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
                    QMessageBox {
                        background-color: rgb(53, 53, 53);
                        color: rgb(255, 255, 255);
                        border: 2px solid rgb(53, 53, 53);
                    }
                    QMessageBox QLabel {
                        color: rgb(255, 255, 255);
                    }
                    QPushButton {
                        background-color: rgb(53, 53, 53);
                        color: white;
                    }
                    """)

    def set_message_type(self, message_type):
        icon_map = {
            QMessageBox.Information: QStyle.SP_MessageBoxInformation,
            QMessageBox.Warning: QStyle.SP_MessageBoxWarning,
            QMessageBox.Critical: QStyle.SP_MessageBoxCritical,
            QMessageBox.Question: QStyle.SP_MessageBoxQuestion
        }
        icon = self.style().standardIcon(icon_map[message_type])
        pixmap = icon.pixmap(icon.actualSize(QSize(64, 64)))
        self.setIconPixmap(pixmap)

    @staticmethod
    def information(parent, title, message):
        dark_message = DarkMessage()
        dark_message.set_message_type(QMessageBox.Information)
        dark_message.setWindowTitle(title)
        dark_message.setText(message)
        dark_message.exec()

    @staticmethod
    def warning(parent, title, message):
        dark_message = DarkMessage()
        dark_message.set_message_type(QMessageBox.Warning)
        dark_message.setWindowTitle(title)
        dark_message.setText(message)
        dark_message.exec()

    @staticmethod
    def critical(parent, title, message):
        dark_message = DarkMessage()
        dark_message.set_message_type(QMessageBox.Critical)
        dark_message.setWindowTitle(title)
        dark_message.setText(message)

    @staticmethod
    def question(parent, title, message):
        dark_message = DarkMessage()
        dark_message.set_message_type(QMessageBox.Question)
        dark_message.setWindowTitle(title)
        dark_message.setText(message)

class GameDisplayWidget(QWidget):
    clicked = Signal()

    def __init__(self, parent=None):
        super(GameDisplayWidget, self).__init__(parent)
        self.setAutoFillBackground(True)
        self.default_palette = self.palette()

    def enterEvent(self, event):
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(70, 70, 70))
        self.setPalette(palette)

    def leaveEvent(self, event):
        self.setPalette(self.default_palette)

    def mousePressEvent(self, event):
        self.clicked.emit()

class ImageLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._border_color = QColor(225, 255, 255)
        self._border_width = 10

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(self._border_color)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(0, 0, self.width() - 1,
                         self.height() - 1)
