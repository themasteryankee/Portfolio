from PySide6.QtWidgets import QStackedWidget

class AutoResizeQStackedWidget(QStackedWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def resizeEvent(self, event):
        current_widget = self.currentWidget()
        if current_widget:
            new_size = current_widget.sizeHint()
            self.setMinimumSize(new_size)
            self.setMaximumSize(new_size)
        super().resizeEvent(event)