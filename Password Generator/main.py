from PySide6.QtWidgets import QApplication
import sys
from practice import Widget

app = QApplication(sys.argv)

widget = Widget()
widget.show()

app.exec()