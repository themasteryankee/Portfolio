from PySide6.QtWidgets import (QWidget, QLineEdit, QLabel, QHBoxLayout, QVBoxLayout, QPushButton,
                               QDialog)
import string
import random

class Widget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Password Generator")

        length_label = QLabel("Password Length")
        self.length_field = QLineEdit()

        gen_button = QPushButton("Generate Password")
        gen_button.clicked.connect(self.gen_password)

        label_layout = QHBoxLayout()
        field_layout = QHBoxLayout()
        button_layout = QHBoxLayout()
        main_layout = QVBoxLayout()

        label_layout.addWidget(length_label)
        label_layout.addStretch(1)

        field_layout.addWidget(self.length_field)
        field_layout.addStretch(1)

        button_layout.addWidget(gen_button)
        button_layout.addStretch(1)

        main_layout.addLayout(label_layout)
        main_layout.addLayout(field_layout)
        main_layout.addStretch(1)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def gen_password(self, length):
        length = self.length_field.text()
        if not length or not length.isdigit():
            return

        self.password = ""

        valid = False

        while not valid:
            for character in range(int(length)):
                letter = random.choice(string.ascii_letters + string.digits + string.punctuation)
                self.password += letter
            if any(char in string.punctuation for char in self.password) and not self.password.isalnum():
                valid = True
            else:
                self.password = ""
                continue

        self.display_password()

    def display_password(self):
        dialog = QDialog()
        dialog.setWindowTitle("New Password")

        label = QLabel("Generated Password:")

        password_label = QLineEdit()
        password_label.setText(f"{self.password}")
        password_label.setReadOnly(True)

        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.close)

        label_layout = QHBoxLayout()
        password_layout = QHBoxLayout()
        button_layout = QHBoxLayout()
        main_layout = QVBoxLayout()

        label_layout.addWidget(label)
        label_layout.addStretch(1)

        password_layout.addWidget(password_label)
        password_layout.addStretch(1)

        button_layout.addWidget(close_button)
        button_layout.addStretch(1)

        main_layout.addLayout(label_layout)
        main_layout.addLayout(password_layout)
        main_layout.addLayout(button_layout)

        dialog.setLayout(main_layout)

        dialog.exec()