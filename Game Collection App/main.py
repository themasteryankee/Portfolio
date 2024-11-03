from PySide6.QtWidgets import QApplication
import sys
from widget import Widget
from db_init import create_tables
import sqlite3

app = QApplication(sys.argv)
app.setStyle("fusion")

connection = sqlite3.connect("userdata.db")
cursor = connection.cursor()
create_tables(cursor)   

widget = Widget(cursor, connection)
widget.adjustSize()
widget.show()
app.exec()