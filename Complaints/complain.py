from PySide6.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
                               QTableWidget, QDialog, QTableWidgetItem, QHeaderView,
                               QTextEdit, QDateEdit, QMessageBox, QSizePolicy)
from PySide6.QtCore import QDate, Qt
import csv
import os

class Widget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("McFire")
        self.setFixedSize(600, 400)

        self.complaint_label = QLabel("Complaint List")

        self.complaint_table = QTableWidget()
        self.complaint_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.complaint_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.complaint_table.cellClicked.connect(self.cell_clicked)

        self.add_button = QPushButton("Add Complaint")
        self.add_button.clicked.connect(self.complaint_dialog)

        self.label_layout = QHBoxLayout()
        self.list_layout = QHBoxLayout()
        self.button_layout = QHBoxLayout()
        self.main_layout = QVBoxLayout()
        self.main_stretches = QHBoxLayout()

        self.label_layout.addWidget(self.complaint_label)
        self.label_layout.addStretch(1)

        self.list_layout.addWidget(self.complaint_table)

        self.button_layout.addWidget(self.add_button)
        self.button_layout.addStretch(1)

        self.main_layout.addLayout(self.label_layout)
        self.main_layout.addLayout(self.list_layout)
        self.main_layout.addLayout(self.button_layout)
        self.setLayout(self.main_layout)

    def load_complaints(self):
        if os.path.exists("complaints.csv"):
            with open("complaints.csv", "r", newline='') as file:
                reader = csv.reader(file)
                next(reader)
                data = list(reader)

                data.sort(key=lambda row: QDate.fromString(row[0], Qt.ISODate), reverse=True)

                self.headers = ["Date", "Plaintiff", "Complaint"]

                self.complaint_table.setRowCount(len(data))
                self.complaint_table.setColumnCount(len(self.headers))
                self.complaint_table.setHorizontalHeaderLabels(self.headers)

                for row_index, row_data in enumerate(data):
                    for column_index, value in enumerate(row_data):
                        complaint = QTableWidgetItem(value)
                        complaint.setFlags(complaint.flags() & ~Qt.ItemIsEditable)
                        self.complaint_table.setItem(row_index, column_index, complaint)

        else:
            with open("complaints.csv", "w", newline='') as file:
                writer = csv.writer(file)
                headers = ["Date", "Plaintiff", "Complaint"]
                writer.writerow(headers)

    def cell_clicked(self, row, column):
        date = self.complaint_table.item(row, 0).text()
        name = self.complaint_table.item(row, 1).text()
        complaint = self.complaint_table.item(row, 2).text()

        complaint_number = row + 1

        message = QMessageBox.information(self, f"Complaint #{complaint_number}", f"Plaintiff: {name}\n"
                                                                                  f"Date: {date}\n\n"
                                                                                  f"{complaint}")
        return

    def complaint_dialog(self):
        complaint_dialog = QDialog()
        complaint_dialog.setWindowTitle("New Complaint")

        name_label = QLabel("Plaintiff's Name")
        self.name_field = QLineEdit()

        date_label = QLabel("Date of Incident")
        self.date_widget = QDateEdit()
        self.date_widget.setCalendarPopup(True)

        current_date = QDate.currentDate()
        self.date_widget.setDate(current_date)
        self.date_widget.setMaximumDate(current_date)

        complaint_label = QLabel("What is the issue?")
        self.complaint_field = QTextEdit()

        finish_button = QPushButton("Finish")
        finish_button.clicked.connect(lambda: self.add_complaint(complaint_dialog))

        name_label_layout = QHBoxLayout()
        name_field_layout = QHBoxLayout()
        name_layout = QVBoxLayout()
        date_label_layout = QHBoxLayout()
        date_widget_layout = QHBoxLayout()
        date_layout = QVBoxLayout()
        name_date_layout = QHBoxLayout()
        complaint_label_layout = QHBoxLayout()
        complaint_edit_layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        main_layout = QVBoxLayout()

        name_label_layout.addWidget(name_label)
        name_label_layout.addStretch(1)

        name_field_layout.addWidget(self.name_field)
        name_field_layout.addStretch(1)

        name_layout.addStretch(1)
        name_layout.addLayout(name_label_layout)
        name_layout.addLayout(name_field_layout)

        date_label_layout.addWidget(date_label)
        date_label_layout.addStretch(1)

        date_widget_layout.addWidget(self.date_widget)
        date_widget_layout.addStretch(1)

        date_layout.addLayout(date_label_layout)
        date_layout.addLayout(date_widget_layout)

        name_date_layout.addLayout(name_layout)
        name_date_layout.addLayout(date_layout)
        name_date_layout.addStretch(1)

        complaint_label_layout.addWidget(complaint_label)
        complaint_label_layout.addStretch(1)

        complaint_edit_layout.addLayout(complaint_label_layout)
        complaint_edit_layout.addWidget(self.complaint_field)

        button_layout.addWidget(finish_button)
        button_layout.addStretch(1)

        main_layout.addLayout(name_date_layout)
        main_layout.addLayout(complaint_edit_layout)
        main_layout.addLayout(button_layout)

        complaint_dialog.setLayout(main_layout)

        complaint_dialog.exec()

    def add_complaint(self, dialog):
        plaintiff_name = self.name_field.text()
        date = self.date_widget.date().toString(Qt.ISODate)
        complaint = self.complaint_field.toPlainText()

        if not plaintiff_name:
            message = QMessageBox.warning(self, "Invalid Name", "A name is required to submit a complaint.")
            return
        if not date:
            message = QMessageBox.warning(self, "Invalid Date", "A date is required to submit a complaint.")
            return
        if not complaint:
            message = QMessageBox.warning(self, "Invalid Complaint", "A complaint is required to submit a complaint.")
            return

        with open("complaints.csv", "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, plaintiff_name, complaint])

        self.load_complaints()
        dialog.close()













