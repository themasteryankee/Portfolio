def create_tables(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS LoginInfo (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    password_hash TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Games (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Consoles (
    id INTEGER PRIMARY KEY,
    console_name TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS GameConsoles (
    game_id INTEGER,
    console_id INTEGER,
    box_art TEXT,
    release_year INTEGER,
    description TEXT,
    PRIMARY KEY(game_id, console_id),
    FOREIGN KEY(game_id) REFERENCES Games(id),
    FOREIGN KEY(console_id) REFERENCES Consoles(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS UserGames (
    user_id INTEGER,
    game_id INTEGER,
    console_id INTEGER,
    PRIMARY KEY(user_id, game_id, console_id),
    FOREIGN KEY(user_id) REFERENCES LoginInfo(id),
    FOREIGN KEY(game_id, console_id) REFERENCES GameConsoles(game_id, console_id))
    """)