from PySide6.QtWidgets import (QListWidget, QListWidgetItem, QHBoxLayout, QVBoxLayout, QWidget,
                               QLabel, QPushButton, QGridLayout, QScrollArea, QSizePolicy, QMessageBox,
                               QStackedWidget, QDialog, QSpacerItem, QSizePolicy, QTextEdit,
                               QDockWidget, QLineEdit, QCheckBox)
from PySide6.QtGui import QIcon, QPixmap, QFont
from PySide6.QtCore import QSize, Qt, Signal
from style import DarkMessage, GameDisplayWidget, ImageLabel
import os

class GameList(QScrollArea):
    def __init__(self, cursor, connection, user_id, start_row, page_size):
        super().__init__()
        self.cursor = cursor
        self.connection = connection
        self.user_id = user_id
        self.start_row = start_row
        self.page_size = page_size
        self.setWidgetResizable(True)
        self.setMinimumSize(200, 200)
        self.adjustSize()
        self.update_game_list()

    def update_game_list(self):
        user_games = self.get_user_games(self.start_row, self.page_size)

        widget = QWidget()
        self.setWidget(widget)
        layout = QGridLayout()

        for i, game in enumerate(user_games):
            name, image_path, release_year, game_id, console_id, console_name, description = game
            game_widget = GameDisplayWidget()
            game_widget.clicked.connect(lambda game_id=game_id, console_id=console_id, name=name,
                                        image_path=image_path, release_year=release_year, console_name=console_name,
                                        description=description:
                                        self.show_game_details(game_id, console_id, name, image_path,
                                                               release_year, console_name, description))
            game_layout = QVBoxLayout()
            h_icon_layout = QHBoxLayout()
            h_name_layout = QHBoxLayout()
            h_console_layout = QHBoxLayout()
            h_year_layout = QHBoxLayout()
            h_layout = QHBoxLayout()
            v_layout = QVBoxLayout()

            game_title = name
            game_name = QLabel(game_title, alignment=Qt.AlignCenter)
            game_name.setWordWrap(True)

            game_icon = ImageLabel()
            game_icon.setPixmap(QPixmap(image_path))
            game_icon.setFixedSize(70, 100)
            game_icon.setScaledContents(True)
            game_year = QLabel(f"Released in: {str(release_year)}")
            game_console = QLabel(console_name)

            remove_button = QPushButton("Remove from\nCollection")
            remove_button.clicked.connect(lambda game_id=game_id, console_id=console_id: self.remove_from_collection(game_id, console_id))

            h_icon_layout.addStretch(1)
            h_icon_layout.addWidget(game_icon)
            h_icon_layout.addStretch(1)

            h_name_layout.addStretch(1)
            h_name_layout.addWidget(game_name)
            h_name_layout.addStretch(1)

            h_console_layout.addStretch(1)
            h_console_layout.addWidget(game_console)
            h_console_layout.addStretch(1)

            h_year_layout.addStretch(1)
            h_year_layout.addWidget(game_year)
            h_year_layout.addStretch(1)

            game_layout.addLayout(h_icon_layout)
            game_layout.addLayout(h_name_layout)
            game_layout.addLayout(h_console_layout)
            game_layout.addLayout(h_year_layout)

            h_layout.addStretch(1)
            h_layout.addLayout(game_layout)
            h_layout.addStretch(1)

            v_layout.addLayout(h_layout)
            v_layout.addWidget(remove_button)

            game_widget.setLayout(v_layout)

            size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            size_policy.setHorizontalStretch(0)
            size_policy.setVerticalStretch(0)
            size_policy.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
            game_widget.setSizePolicy(size_policy)

            row = i // 3
            column = i % 3

            widget.adjustSize()
            self.setMinimumSize(widget.sizeHint())
            layout.addWidget(game_widget, row, column, alignment=Qt.AlignTop)

        widget.setLayout(layout)
        self.update()
        self.updateGeometry()
        self.adjustSize()

    def get_game_count(self):
        result = self.cursor.execute("SELECT COUNT(DISTINCT game_id) FROM UserGames WHERE user_id = ?", (self.user_id,)).fetchone()
        if result is None:
            return 0
        else:
            return result[0]

    def remove_from_collection(self, game_id, console_id):
        self.cursor.execute("DELETE FROM UserGames WHERE user_id = ? AND "
                            "game_id = ? AND console_id = ?", (self.user_id, game_id, console_id))
        self.connection.commit()
        self.update_game_list()

    def get_user_games(self, start_row, page_size):
        self.cursor.execute("SELECT Games.name, GameConsoles.box_art, GameConsoles.release_year, UserGames.game_id, "
                            "UserGames.console_id, Consoles.console_name, GameConsoles.description FROM UserGames "
                            "INNER JOIN Games ON UserGames.game_id = Games.id "
                            "INNER JOIN GameConsoles ON UserGames.game_id = GameConsoles.game_id AND "
                            "UserGames.console_id = GameConsoles.console_id "
                            "INNER JOIN Consoles ON GameConsoles.console_id = Consoles.id "
                            "WHERE UserGames.user_id = ? "
                            "ORDER BY Games.name, Consoles.console_name "
                            "LIMIT ?, ?", (self.user_id, start_row, page_size))
        games = self.cursor.fetchall()
        return games

    def get_user_game_count(self):
        games = self.cursor.execute("SELECT COUNT(DISTINCT game_id || '-' || console_id) FROM UserGames "
                                    "JOIN LoginInfo ON UserGames.user_id = LoginInfo.id "
                                    "WHERE LoginInfo.id = ?", (self.user_id,)).fetchone()

        return games[0] if games else 0

    def show_game_details(self, game_id, console_id, name, image_path, release_year, console_name, description):
        game_name = name
        if ":" in game_name:
            game_title = game_name.replace(': ', ':\n')
            game_title_label = QLabel(game_title)
            game_title_label.setWordWrap(True)
        else:
            game_title_label = QLabel(game_name)

        dialog = QDialog()
        dialog.setWindowTitle(f"About {game_name} for the {console_name}")

        dialog_layout = QHBoxLayout()
        title_console_layout = QVBoxLayout()
        close_layout = QHBoxLayout()
        tc_desc_close_layout = QVBoxLayout()

        tc_spacer = QSpacerItem(10, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        image_tc_spacer = QSpacerItem(10, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        tc_desc_spacer = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        desc_close_spacer = QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Expanding)

        game_desc = QTextEdit(description)
        game_desc.setReadOnly(True)
        game_desc.setMaximumWidth(300)
        game_desc.setStyleSheet("QTextEdit {"
                                "background-color: transparent;"
                                "border: none; }")

        game_icon = ImageLabel()
        game_icon.setPixmap(QPixmap(image_path))
        game_icon.setFixedSize(200, 300)
        game_icon.setScaledContents(True)

        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(22)
        title_label = QLabel(f"{game_title_label.text()}")
        title_label.setFont(title_font)

        console_font = QFont()
        console_font.setBold(True)
        console_font.setPointSize(14)
        console_label = QLabel(f"for the {console_name}")
        console_label.setFont(console_font)

        dialog_close_button = QPushButton("Close")
        dialog_close_button.clicked.connect(dialog.close)

        title_console_layout.addWidget(title_label)
        title_console_layout.addItem(tc_spacer)
        title_console_layout.addWidget(console_label)

        close_layout.addStretch(1)
        close_layout.addWidget(dialog_close_button)

        tc_desc_close_layout.addLayout(title_console_layout)
        tc_desc_close_layout.addItem(tc_desc_spacer)
        tc_desc_close_layout.addWidget(game_desc)
        tc_desc_close_layout.addItem(desc_close_spacer)
        tc_desc_close_layout.addLayout(close_layout)

        dialog_layout.addWidget(game_icon)
        dialog_layout.addItem(image_tc_spacer)
        dialog_layout.addLayout(tc_desc_close_layout)

        dialog.setLayout(dialog_layout)

        dialog.exec()

class AllGamesList(QScrollArea):
    def __init__(self, cursor, connection, user_id):
        super().__init__()
        self.cursor = cursor
        self.connection = connection
        self.user_id = user_id
        self.setWidgetResizable(True)
        self.setMinimumSize(200, 200)
        self.adjustSize()
        self.games = []
        self.update_game_list(start_row=0, page_size=6)

    def update_game_list(self, start_row, page_size):
        self.cursor.execute("SELECT Games.name, Consoles.console_name, GameConsoles.box_art, "
                            "GameConsoles.release_year, GameConsoles.description FROM Games "
                            "INNER JOIN GameConsoles ON Games.id = GameConsoles.game_id "
                            "INNER JOIN Consoles ON GameConsoles.console_id = Consoles.id "
                            "ORDER BY Games.name, Consoles.console_name "
                            "LIMIT ?,?", (start_row, page_size))
        games = self.cursor.fetchall()

        self.main_widget = QWidget()
        self.setWidget(self.main_widget)
        main_layout = QGridLayout()

        for i, game in enumerate(games):
            game_name, console_name, box_art, release_year, description = game
            widget = GameDisplayWidget()
            widget.clicked.connect(lambda game_name=game_name, console_name=console_name, box_art=box_art,
                                   release_year=release_year, description=description:
                                        self.show_game_details(game_name, console_name, box_art,
                                                               release_year, description))
            layout = QVBoxLayout()
            h_layout = QHBoxLayout()
            h_icon_layout = QHBoxLayout()
            h_name_layout = QHBoxLayout()
            h_console_layout = QHBoxLayout()
            h_year_layout = QHBoxLayout()
            h_button_layout = QHBoxLayout()
            v_layout = QVBoxLayout()

            game_title = game[0]
            game_name = QLabel(game_title, alignment=Qt.AlignCenter)
            game_name.setWordWrap(True)

            game_icon = ImageLabel()
            game_icon.setPixmap(QPixmap(game[2]))
            game_icon.setFixedSize(70, 100)
            game_icon.setScaledContents(True)
            game_year = QLabel(f"Released in: {str(game[3])}")
            game_console = QLabel(game[1])

            add_button = QPushButton("Add to Collection")
            add_button.setFixedWidth(100)
            add_button.clicked.connect((lambda game=game: lambda: self.add_to_collection(game))())

            h_icon_layout.addStretch(1)
            h_icon_layout.addWidget(game_icon)
            h_icon_layout.addStretch(1)

            h_name_layout.addStretch(1)
            h_name_layout.addWidget(game_name)
            h_name_layout.addStretch(1)

            h_console_layout.addStretch(1)
            h_console_layout.addWidget(game_console)
            h_console_layout.addStretch(1)

            h_year_layout.addStretch(1)
            h_year_layout.addWidget(game_year)
            h_year_layout.addStretch(1)

            layout.addLayout(h_icon_layout)
            layout.addLayout(h_name_layout)
            layout.addLayout(h_console_layout)
            layout.addLayout(h_year_layout)

            h_button_layout.addStretch(1)
            h_button_layout.addWidget(add_button)
            h_button_layout.addStretch(1)

            v_layout.addLayout(layout)
            v_layout.addLayout(h_button_layout)

            widget.setLayout(v_layout)

            size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            size_policy.setHorizontalStretch(0)
            size_policy.setVerticalStretch(0)
            size_policy.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
            widget.setSizePolicy(size_policy)

            row = i // 3
            column = i % 3

            widget.adjustSize()
            self.setMinimumSize(widget.sizeHint())

            main_layout.addWidget(widget, row, column, alignment=Qt.AlignTop)
        self.main_widget.setLayout(main_layout)
        self.update()
        self.updateGeometry()
        self.adjustSize()

    def clear_all_games(self):
        for i in reversed(range(self.main_layout.count())):
            widget_to_remove = self.main_layout.itemAt(i).widget()
            self.main_layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)


    def update_search_games_list(self, games):
        self.main_widget = QWidget()
        self.setWidget(self.main_widget)
        main_layout = QGridLayout()

        for i, game in enumerate(games):
            game_name, console_name, box_art, release_year, description = game
            widget = GameDisplayWidget()
            widget.clicked.connect(lambda game_name=game_name, console_name=console_name, box_art=box_art,
                                          release_year=release_year, description=description:
                                   self.show_game_details(game_name, console_name, box_art,
                                                          release_year, description))
            layout = QVBoxLayout()
            h_layout = QHBoxLayout()
            h_icon_layout = QHBoxLayout()
            h_name_layout = QHBoxLayout()
            h_console_layout = QHBoxLayout()
            h_year_layout = QHBoxLayout()
            h_button_layout = QHBoxLayout()
            v_layout = QVBoxLayout()

            game_title = game[0]
            game_name = QLabel(game_title, alignment=Qt.AlignCenter)
            game_name.setWordWrap(True)

            game_icon = ImageLabel()
            game_icon.setPixmap(QPixmap(game[2]))
            game_icon.setFixedSize(70, 100)
            game_icon.setScaledContents(True)
            game_year = QLabel(f"Released in: {str(game[3])}")
            game_console = QLabel(game[1])

            add_button = QPushButton("Add to Collection")
            add_button.setFixedWidth(100)
            add_button.clicked.connect((lambda game=game: lambda: self.add_to_collection(game))())

            h_icon_layout.addStretch(1)
            h_icon_layout.addWidget(game_icon)
            h_icon_layout.addStretch(1)

            h_name_layout.addStretch(1)
            h_name_layout.addWidget(game_name)
            h_name_layout.addStretch(1)

            h_console_layout.addStretch(1)
            h_console_layout.addWidget(game_console)
            h_console_layout.addStretch(1)

            h_year_layout.addStretch(1)
            h_year_layout.addWidget(game_year)
            h_year_layout.addStretch(1)

            layout.addLayout(h_icon_layout)
            layout.addLayout(h_name_layout)
            layout.addLayout(h_console_layout)
            layout.addLayout(h_year_layout)

            h_button_layout.addStretch(1)
            h_button_layout.addWidget(add_button)
            h_button_layout.addStretch(1)

            v_layout.addLayout(layout)
            v_layout.addLayout(h_button_layout)

            widget.setLayout(v_layout)

            size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            size_policy.setHorizontalStretch(0)
            size_policy.setVerticalStretch(0)
            size_policy.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
            widget.setSizePolicy(size_policy)

            row = i // 3
            column = i % 3

            widget.adjustSize()
            self.setMinimumSize(widget.sizeHint())

            main_layout.addWidget(widget, row, column, alignment=Qt.AlignTop)
        self.main_widget.setLayout(main_layout)
        self.update()
        self.updateGeometry()
        self.adjustSize()

    def show_game_details(self, game_name, console_name, box_art, release_year, description):
        if ":" in game_name:
            game_title = game_name.replace(': ', ':\n')
            game_title_label = QLabel(game_title)
            game_title_label.setWordWrap(True)
        else:
            game_title_label = QLabel(game_name)

        dialog = QDialog()
        dialog.setWindowTitle(f"About {game_name} for the {console_name}")

        dialog_layout = QHBoxLayout()
        title_console_layout = QVBoxLayout()
        close_layout = QHBoxLayout()
        tc_desc_close_layout = QVBoxLayout()

        tc_spacer = QSpacerItem(10, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        image_tc_spacer = QSpacerItem(10, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        tc_desc_spacer = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        desc_close_spacer = QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Expanding)

        game_desc = QTextEdit(description)
        game_desc.setReadOnly(True)
        game_desc.setMaximumWidth(300)
        game_desc.setStyleSheet("QTextEdit {"
                                "background-color: transparent;"
                                "border: none; }")

        game_icon = ImageLabel()
        game_icon.setPixmap(QPixmap(box_art))
        game_icon.setFixedSize(200, 300)
        game_icon.setScaledContents(True)

        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(22)
        title_label = QLabel(f"{game_title_label.text()}")
        title_label.setFont(title_font)

        console_font = QFont()
        console_font.setBold(True)
        console_font.setPointSize(14)
        console_label = QLabel(f"for the {console_name}")
        console_label.setFont(console_font)

        dialog_close_button = QPushButton("Close")
        dialog_close_button.clicked.connect(dialog.close)

        title_console_layout.addWidget(title_label)
        title_console_layout.addItem(tc_spacer)
        title_console_layout.addWidget(console_label)

        close_layout.addStretch(1)
        close_layout.addWidget(dialog_close_button)

        tc_desc_close_layout.addLayout(title_console_layout)
        tc_desc_close_layout.addItem(tc_desc_spacer)
        tc_desc_close_layout.addWidget(game_desc)
        tc_desc_close_layout.addItem(desc_close_spacer)
        tc_desc_close_layout.addLayout(close_layout)

        dialog_layout.addWidget(game_icon)
        dialog_layout.addItem(image_tc_spacer)
        dialog_layout.addLayout(tc_desc_close_layout)

        dialog.setLayout(dialog_layout)

        dialog.exec()

    def get_game_count(self):
        result = self.cursor.execute("SELECT COUNT(game_id) FROM GameConsoles").fetchone()

        if result is None:
            return 0
        else:
            return result[0]

    def add_to_collection(self, game):
        if not isinstance(game, bool):
            game_name = game[0]
            console_name = game[1]
            self.cursor.execute("SELECT id FROM Games WHERE name = ?", (game_name,))

            result = self.cursor.fetchone()

            if result:
                game_id = result[0]
            else:
                print(f"No PyScape found with name {game_name}")
                return

            self.cursor.execute("SELECT id FROM Consoles WHERE console_name = ?", (console_name,))
            result = self.cursor.fetchone()

            if result:
                console_id = result[0]
            else:
                print(f"No console found with name {console_name}")
                return
            self.cursor.execute("INSERT INTO UserGames (user_id, game_id, console_id) VALUES (?, ?, ?)",
                                (self.user_id, game_id, console_id))
            message = DarkMessage()
            message.set_message_type(QMessageBox.Information)
            message.information(self, "Game Collected", "This PyScape was added to your collection!")
            self.connection.commit()
            print(f"Game added to collection: user_id = {self.user_id}\n"
                  f"game_id = {game_id}, console_id = {console_id}")

    def set_user_id(self, user_id):
        self.user_id = user_id
        self.update_game_list(start_row=0, page_size=6)

class LoginDisplay(QScrollArea):
    def __init__(self, cursor, connection):
        super().__init__()
        self.cursor = cursor
        self.connection = connection
        self.setWidgetResizable(True)
        self.setMinimumSize(200, 200)
        self.adjustSize()
        self.update_game_list()
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

    def update_game_list(self):
        games = self.get_random_games()

        widget = QWidget()
        self.setWidget(widget)
        v_layout = QVBoxLayout()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        for i, game in enumerate(games):
            game_name, game_art, game_release, game_id, game_console_id, game_console_name, game_desc = game
            game_widget = GameDisplayWidget()
            game_widget.clicked.connect(lambda game_name=game_name, game_art=game_art, game_release=game_release, game_console_name=game_console_name,
                                               game_desc=game_desc: self.show_game_details(game_name, game_art, game_release, game_console_name,
                                                                                           game_desc))
            h_layout = QHBoxLayout()

            game_icon = ImageLabel()
            game_icon.setPixmap(QPixmap(game_art))
            game_icon.setFixedSize(120, 160)
            game_icon.setScaledContents(True)

            h_layout.addStretch(1)
            h_layout.addWidget(game_icon)
            h_layout.addStretch(1)

            game_widget.setLayout(h_layout)

            size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            size_policy.setHorizontalStretch(0)
            size_policy.setVerticalStretch(0)
            size_policy.setHeightForWidth(game_widget.sizePolicy().hasHeightForWidth())
            game_widget.setSizePolicy(size_policy)

            game_widget.adjustSize()
            self.setMinimumSize(game_widget.sizeHint())

            layout.addWidget(game_widget, alignment=Qt.AlignTop)

        spacer = QSpacerItem(10, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)

        sugg_font = QFont()
        sugg_font.setPointSize(14)
        sugg_font.setBold(True)

        game_suggestion_label = QLabel("Check these out!")
        game_suggestion_label.setFont(sugg_font)

        v_layout.addWidget(game_suggestion_label)
        v_layout.setAlignment(game_suggestion_label, Qt.AlignTop)
        v_layout.addLayout(layout)

        widget.setLayout(v_layout)
        self.update()
        self.updateGeometry()
        self.adjustSize()

    def get_random_games(self):
        self.cursor.execute("SELECT Games.name, GameConsoles.box_art, GameConsoles.release_year, "
                            "Games.id, GameConsoles.console_id, Consoles.console_name, GameConsoles.description "
                            "FROM Games "
                            "INNER JOIN GameConsoles ON Games.id = GameConsoles.game_id "
                            "INNER JOIN Consoles ON GameConsoles.console_id = Consoles.id "
                            "ORDER BY RANDOM() LIMIT 3")
        games = self.cursor.fetchall()
        return games

    def show_game_details(self, game_name, game_art, game_release, game_console_name, description):
        if ":" in game_name:
            game_title = game_name.replace(": ", ":\n")
            game_title_label = QLabel(game_title)
            game_title_label.setWordWrap(True)
        else:
            game_title_label = QLabel(game_name)

        dialog = QDialog()
        dialog.setWindowTitle(f"About {game_name} for the {game_console_name}")

        dialog_layout = QHBoxLayout()
        title_console_layout = QVBoxLayout()
        close_layout = QHBoxLayout()
        tc_desc_close_layout = QVBoxLayout()

        tc_spacer = QSpacerItem(10, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        image_tc_spacer = QSpacerItem(10, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        tc_desc_spacer = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        desc_close_spacer = QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Expanding)

        game_desc = QTextEdit(description)
        game_desc.setReadOnly(True)
        game_desc.setMaximumWidth(300)
        game_desc.setStyleSheet("QTextEdit {"
                                "background-color: transparent;"
                                "border: none; }")

        game_icon = ImageLabel()
        game_icon.setPixmap(QPixmap(game_art))
        game_icon.setFixedSize(200, 300)
        game_icon.setScaledContents(True)

        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(22)
        title_label = QLabel(f"{game_title_label.text()}")
        title_label.setFont(title_font)

        console_font = QFont()
        console_font.setBold(True)
        console_font.setPointSize(14)
        console_label = QLabel(f"for the {game_console_name}")
        console_label.setFont(console_font)

        dialog_close_button = QPushButton("Close")
        dialog_close_button.clicked.connect(dialog.close)

        title_console_layout.addWidget(title_label)
        title_console_layout.addItem(tc_spacer)
        title_console_layout.addWidget(console_label)

        close_layout.addStretch(1)
        close_layout.addWidget(dialog_close_button)

        tc_desc_close_layout.addLayout(title_console_layout)
        tc_desc_close_layout.addItem(tc_desc_spacer)
        tc_desc_close_layout.addWidget(game_desc)
        tc_desc_close_layout.addItem(desc_close_spacer)
        tc_desc_close_layout.addLayout(close_layout)

        dialog_layout.addWidget(game_icon)
        dialog_layout.addItem(image_tc_spacer)
        dialog_layout.addLayout(tc_desc_close_layout)

        dialog.setLayout(dialog_layout)

        dialog.exec()

class SearchWidget(QDockWidget):
    new_search_made = Signal(list)
    searchTextChanged = Signal()

    def __init__(self, cursor, connection):
        super().__init__()
        self.setWindowTitle("Search Game Titles")
        self.cursor = cursor
        self.connection = connection

        content = QWidget(self)
        layout = QVBoxLayout()
        v_layout = QVBoxLayout()

        console_names = [record[0] for record in self.cursor.execute("SELECT console_name FROM consoles "
                                                                     "ORDER BY console_name")]

        self.search_bar = QLineEdit()
        self.search_bar.textChanged.connect(self.searchTextChanged)

        self.search_button = QPushButton("Search")

        self.checkboxes = [QCheckBox(console_name) for console_name in console_names]

        for i, checkbox in enumerate(self.checkboxes):
            v_layout.addWidget(checkbox, alignment=Qt.AlignTop)

        for checkbox in self.checkboxes:
            checkbox.stateChanged.connect(self.perform_search)

        layout.addWidget(self.search_bar)
        layout.addWidget(self.search_button)
        layout.addLayout(v_layout)
        layout.setAlignment(Qt.AlignTop)

        content.setLayout(layout)

        self.setWidget(content)

        self.update()
        self.updateGeometry()
        self.adjustSize()

    def perform_search(self):
        search_text = self.search_bar.text().strip()
        #any_box_checked = any(checkbox.isChecked() for checkbox in self.checkboxes)
        checked_consoles = [checkbox.text() for checkbox in self.checkboxes if checkbox.isChecked()]

        results = []

        if search_text or checked_consoles:
            query = ("SELECT Games.name, Consoles.console_name, GameConsoles.box_art, "
                     "GameConsoles.release_year, GameConsoles.description FROM Games "
                     "INNER JOIN GameConsoles ON Games.id = GameConsoles.game_id "
                     "INNER JOIN Consoles ON GameConsoles.console_id = Consoles.id ")

            if checked_consoles:
                query += "WHERE Games.name = ? AND Consoles.console_name IN ({}) ".format(', '.join(['?'] * len(checked_consoles)))
                for console_name in checked_consoles:
                    self.cursor.execute(query, (search_text, console_name))
                    results.extend(self.cursor.fetchall())
            else:
                query += "WHERE Games.name = ? "
                self.cursor.execute(query, (search_text,))
                results = self.cursor.fetchall()
            results = list(filter(lambda result: result[0] == search_text, results))
            self.new_search_made.emit(results)
        else:
            self.cursor.execute("SELECT Games.name, Consoles.console_name, GameConsoles.box_art, "
                     "GameConsoles.release_year, GameConsoles.description FROM Games "
                     "INNER JOIN GameConsoles ON Games.id = GameConsoles.game_id "
                     "INNER JOIN Consoles ON GameConsoles.console_id = Consoles.id "
                     "WHERE Games.name like ? AND Consoles.console_name = ? "
                     "ORDER BY Games.name, Consoles.console_name")
            result = self.cursor.fetchall()
            self.new_search_made.emit(result)
