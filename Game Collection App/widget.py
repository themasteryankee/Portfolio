from PySide6.QtWidgets import (QWidget, QListWidget, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout,
                               QPushButton, QMessageBox, QStackedWidget, QCompleter,
                               QCheckBox, QApplication, QDockWidget, QSizePolicy)
from PySide6.QtGui import QColor, QPalette
from PySide6.QtCore import QStringListModel, Qt, QPropertyAnimation, QRect
from style import DarkMessage
from list_widget import GameList, AllGamesList, LoginDisplay, SearchWidget
import bcrypt

class Widget(QStackedWidget):
    def __init__(self, cursor, connection):
        super().__init__()
        self.cursor = cursor
        self.connection = connection
        self.setWindowTitle("Game Collection")
        self.current_user = None
        self.setup_Ui()
        self.collection_page_initialized = False
        self.user_game_list_initialized = False
        self.setMinimumSize(675, 575)
        self.setMaximumSize(675, 575)
        self.setCurrentIndex(0)
        self.page_size = 6
        self.start_row = 0
        self.collection_start_row = 0
        self.collection_page_size = 6

    #Setup and Initialize all pages
    def setup_Ui(self):
        dark_message = DarkMessage()
        print(dark_message.styleSheet())
        self.set_dark_palette()
        self.start_page()
        self.create_account_page()
        self.login_page()
        self.collection_page()
        self.catalog_page()

    def set_dark_palette(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
        dark_palette.setColor(QPalette.Text, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        QApplication.instance().setPalette(dark_palette)

    def check_collection_clicked(self):
        user_id_row = self.cursor.execute("SELECT id FROM LoginInfo WHERE username = ?", (self.current_user,)).fetchone()
        user_id = user_id_row[0] if user_id_row else None
        self.game_list_widget = GameList(self.cursor, self.connection, user_id, start_row=self.collection_start_row,
                                         page_size=self.collection_page_size)
        self.user_game_list_initialized = True
        self.game_list_widget.update_game_list()
        self.collection_start_row = 0
        self.collection_page_size = 6
        game_count = self.cursor.execute("SELECT COUNT(DISTINCT game_id || '-' || console_id) FROM UserGames "
                                    "JOIN LoginInfo ON UserGames.user_id = LoginInfo.id "
                                    "WHERE LoginInfo.id = ?", (user_id,)).fetchone()[0]


        self.collection_next_button = QPushButton("Next Page")

        if game_count > self.collection_start_row + self.collection_page_size:
            self.collection_next_button.show()
        else:
            self.collection_next_button.hide()

        self.update_collection_page()
        self.setCurrentIndex(3)

    #Clears text fields in create page
    def clear_create_fields(self):
        self.create_password_field.clear()
        self.create_confirm_field.clear()
        self.create_user_field.clear()

    #Inserts new account's login info into database
    def insert_login_info(self, username, hashed_password):
        self.cursor.execute("""
        INSERT INTO LoginInfo (username, password_hash) VALUES (?, ?)""", (username, hashed_password))
        self.connection.commit()

    #Returns to start page and clears text fields
    def create_back_clicked(self):
        self.clear_create_fields()
        self.clear_start_fields()
        self.setCurrentIndex(0)

    #Goes to create page
    def start_create_clicked(self):
        self.setCurrentIndex(1)

    #Clears QMessageBoxes
    def clear_message_boxes(self):
        for i in self.findChildren(DarkMessage):
            i.close()

    #Logs out current user, clears text fields and returns to start page
    def login_logout_clicked(self):
        self.current_user = None
        self.clear_start_fields()
        self.setCurrentIndex(0)

    #Checks entered login information and compares with info in database
    def start_login_clicked(self):
        username = self.start_user_field.text()
        password = self.start_password_field.text().encode('utf-8')

        self.cursor.execute("""SELECT username, password_hash FROM LoginInfo WHERE username = ?""", (username,))
        result = self.cursor.fetchone()
        message = DarkMessage()
        if not username or not password:
            message.set_message_type(QMessageBox.Warning)
            message.warning(self, "Missing Information", "Please enter your account's login information.")
        elif result is None:
            self.clear_start_fields()
            message.set_message_type(QMessageBox.Warning)
            message.warning(self, "No User Found", "An account with that username does not exist.")
        else:
            db_username, hashed_password = result
            if bcrypt.checkpw(password, hashed_password):
                self.current_user = db_username
                message.set_message_type(QMessageBox.Information)
                message.information(self, "Logged In", "You have successfully logged in.")

                user_id_row = self.cursor.execute("SELECT id FROM LoginInfo WHERE username = ?",
                                                  (self.current_user,)).fetchone()
                user_id = user_id_row[0] if user_id_row else None

                self.catalog_games_list_widget.set_user_id(user_id)
                self.catalog_games_list_widget.update_game_list(0, 6)

                self.login_welcome_label.setText(f"Welcome, {self.current_user}!")
                self.clear_start_fields()
                self.setCurrentIndex(2)
            else:
                message.set_message_type(QMessageBox.Warning)
                message.warning(self, "Incorrect Password", "The entered password was incorrect.\n"
                                                                "Please try again.")

    #If Create account button on create page is clicked
    def create_create_clicked(self):
        username = self.create_user_field.text()
        password = self.create_password_field.text().encode('utf-8')
        confirm = self.create_confirm_field.text().encode('utf-8')

        if not username or not password or not confirm:
            self.clear_create_fields()
            message = DarkMessage()
            message.set_message_type(QMessageBox.Warning)
            message.warning(self, "Missing Information", "Please enter all of the above information.")
            return
        elif password and confirm and password != confirm:
            self.clear_create_fields()
            message = DarkMessage()
            message.set_message_type(QMessageBox.Warning)
            message.warning(self, "Mismatching Passwords", "The entered passwords do not match.")
            return
        else:
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password, salt)
            self.insert_login_info(username, hashed_password)

            message = DarkMessage()
            message.set_message_type(QMessageBox.Information)
            message.information(self, "Account Created", "Your account has been created succesfully.\n"
                                                             "You may now log in.")
            self.connection.commit()
        self.clear_create_fields()
        self.setCurrentIndex(0)

    #Clears text fields in start page
    def clear_start_fields(self):
        self.start_user_field.clear()
        self.start_password_field.clear()

    def update_collection_page(self):
        if not self.collection_page_initialized:
            game_count = self.cursor.execute("SELECT COUNT(DISTINCT console_id) FROM UserGames "
                                             "JOIN LoginInfo ON UserGames.user_id = LoginInfo.id "
                                             "WHERE LoginInfo.username = ?", (self.current_user,)).fetchone()[0]
            for i in reversed(range(self.collection_layout.count())):
                self.collection_layout.itemAt(i).widget().setParent(None)

            print(game_count)

            collection_pageButton_layout = QHBoxLayout()
            collection_button_layout = QHBoxLayout()
            collection_top_h_layout = QHBoxLayout()

            self.collection_next_button.clicked.connect(self.collection_next_clicked)

            self.collection_prev_button = QPushButton("Previous Page")
            self.collection_prev_button.clicked.connect(self.collection_prev_clicked)
            self.collection_prev_button.hide()

            collection_pageButton_layout.addStretch(1)
            collection_pageButton_layout.addWidget(self.collection_prev_button)
            collection_pageButton_layout.addWidget(self.collection_next_button)

            collection_back_button = QPushButton("Back")
            collection_back_button.clicked.connect(self.collection_back_clicked)

            self.game_list_widget.update_game_list()

            collection_button_layout.addLayout(collection_pageButton_layout)
            collection_button_layout.addWidget(self.collection_addGame_button)

            collection_top_h_layout.addWidget(QLabel(f"{self.current_user}'s Games"))
            collection_top_h_layout.addStretch(1)
            collection_top_h_layout.addWidget(collection_back_button)

            self.collection_layout.addLayout(collection_top_h_layout)
            self.collection_layout.addWidget(self.game_list_widget)
            self.collection_layout.addLayout(collection_button_layout)

            self.collection_page_initialized = True

    def collection_back_clicked(self):
        self.login_display.update_game_list()
        self.setCurrentIndex(2)


    #Lays out create account page
    def create_account_page(self):
        create_account_page = QWidget()
        main_layout = QVBoxLayout()
        layout = QVBoxLayout()
        button_layout = QVBoxLayout()
        h_layout = QHBoxLayout()
        h_layout2 = QHBoxLayout()

        self.create_user_label = QLabel("Username")
        self.create_user_field = QLineEdit()
        self.create_user_field.textChanged.connect(self.clear_message_boxes)

        self.create_password_label = QLabel("Password")
        self.create_password_field = QLineEdit()
        self.create_password_field.setEchoMode(QLineEdit.Password)
        self.create_password_field.textChanged.connect(self.clear_message_boxes)

        self.create_confirm_label = QLabel("Confirm Password")
        self.create_confirm_field = QLineEdit()
        self.create_confirm_field.setEchoMode(QLineEdit.Password)
        self.create_confirm_field.textChanged.connect(self.clear_message_boxes)

        self.create_create_button = QPushButton("Create Account")
        self.create_create_button.clicked.connect(self.create_create_clicked)

        self.create_back_button = QPushButton("Back")
        self.create_back_button.clicked.connect(self.create_back_clicked)

        layout.addStretch(1)
        layout.addWidget(self.create_user_label)
        layout.addWidget(self.create_user_field)
        layout.addWidget(self.create_password_label)
        layout.addWidget(self.create_password_field)
        layout.addWidget(self.create_confirm_label)
        layout.addWidget(self.create_confirm_field)
        layout.addStretch(1)

        h_layout2.addStretch(1)
        h_layout2.addLayout(layout)
        h_layout2.addStretch(1)

        button_layout.addStretch(1)
        button_layout.addWidget(self.create_create_button)
        button_layout.addWidget(self.create_back_button)
        button_layout.addStretch(1)

        h_layout.addStretch(1)
        h_layout.addLayout(button_layout)
        h_layout.addStretch(1)

        main_layout.addLayout(h_layout2)
        main_layout.addLayout(h_layout)

        create_account_page.setLayout(main_layout)
        self.addWidget(create_account_page)

    #Lays out start page
    def start_page(self):
        start_page = QWidget()
        layout = QVBoxLayout()
        h_layout = QHBoxLayout()

        self.start_user_label = QLabel("Username")
        self.start_user_field = QLineEdit()

        self.start_password_label = QLabel("Password")
        self.start_password_field = QLineEdit()
        self.start_password_field.setEchoMode(QLineEdit.Password)

        self.start_login_button = QPushButton("Login")
        self.start_login_button.clicked.connect(self.start_login_clicked)
        self.start_create_button = QPushButton("Create Account")
        self.start_create_button.clicked.connect(self.start_create_clicked)

        layout.addStretch(1)
        layout.addWidget(self.start_user_label)
        layout.addWidget(self.start_user_field)
        layout.addWidget(self.start_password_label)
        layout.addWidget(self.start_password_field)
        layout.addStretch(1)
        layout.addWidget(self.start_login_button)
        layout.addWidget(self.start_create_button)
        layout.addStretch(1)

        h_layout.addStretch(1)
        h_layout.addLayout(layout)
        h_layout.addStretch(1)

        start_page.setLayout(h_layout)

        self.addWidget(start_page)

    #Lays out login page
    def login_page(self):
        login_page = QWidget()
        main_layout = QVBoxLayout()
        h_layout = QHBoxLayout()
        logout_layout = QHBoxLayout()

        self.login_welcome_label = QLabel()

        self.login_checkCollection_button = QPushButton("Check Collection")
        self.login_checkCollection_button.clicked.connect(self.check_collection_clicked)

        browse_button = QPushButton("Browse Games")
        browse_button.clicked.connect(self.addGame_clicked)

        self.login_logout_button = QPushButton("Logout")
        self.login_logout_button.clicked.connect(self.login_logout_clicked)

        self.login_display = LoginDisplay(self.cursor, self.connection)

        h_layout.addWidget(self.login_welcome_label)
        h_layout.addStretch(1)
        h_layout.addWidget(self.login_checkCollection_button)
        h_layout.addWidget(browse_button)

        logout_layout.addStretch(1)
        logout_layout.addWidget(self.login_logout_button)

        main_layout.addLayout(h_layout)
        main_layout.addWidget(self.login_display)
        main_layout.addStretch(1)
        main_layout.addLayout(logout_layout)

        login_page.setLayout(main_layout)
        self.addWidget(login_page)

    def collection_page(self):
        collection_page = QWidget()
        self.collection_layout = QVBoxLayout()

        self.collection_addGame_button = QPushButton("Browse Games")
        self.collection_addGame_button.clicked.connect(self.addGame_clicked)

        collection_page.setLayout(self.collection_layout)
        self.addWidget(collection_page)

    def addGame_clicked(self):
        game_count = self.cursor.execute("SELECT COUNT(*) FROM Games").fetchone()[0]
        self.setCurrentIndex(4)
        self.catalog_prev_button.hide()
        if self.start_row == 0 and game_count > self.start_row + self.page_size:
            self.catalog_next_button.show()
        self.catalog_games_list_widget.update_game_list(self.start_row, self.page_size)

        print(f"{self.start_row}\n"
              f"{self.page_size}\n"
              f"{game_count}")

    def collection_next_clicked(self):
        game_count = self.game_list_widget.get_user_game_count()
        self.collection_start_row += self.collection_page_size
        self.game_list_widget.start_row = self.collection_start_row
        self.game_list_widget.update_game_list()

        self.collection_prev_button.show()

        if self.collection_start_row + self.collection_page_size > game_count:
            self.collection_next_button.hide()
        else:
            self.collection_next_button.show()

        print(f"{self.collection_start_row}\n"
              f"{self.collection_page_size}\n"
              f"{game_count}")

    def collection_prev_clicked(self):
        self.collection_start_row -= self.collection_page_size
        self.game_list_widget.start_row = self.collection_start_row
        game_count = self.game_list_widget.get_user_game_count()
        self.game_list_widget.update_game_list()

        self.collection_next_button.show()

        if self.collection_start_row == 0:
            self.collection_prev_button.hide()
        print(f"{self.collection_start_row}\n"
              f"{self.collection_page_size}\n"
              f"{game_count}")

    def catalog_next_clicked(self):
        self.start_row += self.page_size
        self.catalog_games_list_widget.update_game_list(self.start_row, self.page_size)
        game_count = self.catalog_games_list_widget.get_game_count()
        self.catalog_prev_button.show()

        if (self.start_row + self.page_size) >= game_count:
            self.catalog_next_button.hide()
        else:
            self.catalog_next_button.show()

        print(f"{self.start_row}\n"
              f"{self.page_size}\n"
              f"{game_count}")

    def catalog_prev_clicked(self):
        self.start_row -= self.page_size
        game_count = self.catalog_games_list_widget.get_game_count()
        self.catalog_games_list_widget.update_game_list(self.start_row, self.page_size)

        self.catalog_next_button.show()

        if self.start_row == 0:
            self.catalog_prev_button.hide()

        print(f"{self.start_row}\n"
              f"{self.page_size}\n"
              f"{game_count}")

    def catalog_page(self):
        catalog_page = QWidget()
        user_id_row = self.cursor.execute("SELECT id FROM LoginInfo WHERE username = ?",
                                          (self.current_user,)).fetchone()
        user_id = user_id_row[0] if user_id_row else None

        layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        main_layout = QVBoxLayout()
        main_h_layout = QHBoxLayout()

        catalog_label = QLabel("All Games")

        self.catalog_next_button = QPushButton("Next Page")
        self.catalog_next_button.clicked.connect(self.catalog_next_clicked)

        self.catalog_prev_button = QPushButton("Previous Page")
        self.catalog_prev_button.hide()
        self.catalog_prev_button.clicked.connect(self.catalog_prev_clicked)

        back_button = QPushButton("Back")
        back_button.clicked.connect(self.back_clicked)

        self.catalog_games_list_widget = AllGamesList(self.cursor, self.connection, user_id)
        self.catalog_games_list_widget.get_game_count()

        """self.search_widget = SearchWidget(self.cursor, self.connection)
        self.search_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.search_widget.setFixedWidth(200)

        self.search_widget.search_button.clicked.connect(self.catalog_search_button_clicked)
        self.search_widget.new_search_made.connect(self.on_new_search)
        self.search_widget.searchTextChanged.connect(self.start_row_reset)"""

        top_layout.addWidget(catalog_label)
        top_layout.addStretch(1)
        top_layout.addWidget(back_button)

        layout.addWidget(self.catalog_games_list_widget)

        h_layout = QHBoxLayout()
        h_layout.addStretch(1)
        h_layout.addWidget(self.catalog_prev_button)
        h_layout.addWidget(self.catalog_next_button)

        main_layout.addLayout(top_layout)
        main_layout.addLayout(layout)
        main_layout.addLayout(h_layout)

        """main_h_layout.addWidget(self.search_widget)"""
        main_h_layout.addLayout(main_layout)

        catalog_page.setLayout(main_h_layout)

        self.addWidget(catalog_page)

    def start_row_reset(self):
        self.start_row = 0
        """self.search_widget.perform_search()"""

    """def on_new_search(self, games):
        self.catalog_games_list_widget.games = games
        end_row = self.start_row + self.page_size
        games_to_display = games[self.start_row:end_row]
        self.catalog_games_list_widget.update_search_games_list(games_to_display)"""

    """def catalog_search_button_clicked(self):
        self.start_row = 0
        self.search_widget.perform_search()"""

    def back_clicked(self):
        if not self.user_game_list_initialized:
            self.check_collection_clicked()
        self.start_row = 0
        self.collection_start_row = 0
        self.game_list_widget.start_row = self.collection_start_row
        self.game_list_widget.update_game_list()

        self.collection_prev_button.hide()

        games = self.cursor.execute("SELECT COUNT(*) FROM Games").fetchone()[0]
        if games > self.page_size:
            self.catalog_next_button.show()

        user_games = self.game_list_widget.get_user_game_count()
        if user_games > self.collection_page_size:
            self.collection_next_button.show()

        self.setCurrentIndex(3)
        self.update_catalog_buttons()


    def update_catalog_buttons(self):
        game_count = self.catalog_games_list_widget.get_game_count()

        if game_count > self.start_row + self.page_size:
            self.catalog_next_button.show()
        else:
            self.catalog_next_button.hide()

        if self.start_row == 0:
            self.catalog_prev_button.hide()
        elif self.start_row > 0:
            self.catalog_prev_button.show()