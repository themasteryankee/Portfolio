from complain import Widget
import sys
from PySide6.QtWidgets import QApplication

def load_style():
    with open("styles.css", "r") as file:
        return file.read()

app = QApplication(sys.argv)
app.setStyle("fusion")

"""style = load_style()
app.setStyleSheet(style)"""

widget = Widget()
widget.show()
widget.load_complaints()

app.exec()