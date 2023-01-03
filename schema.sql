DROP TABLE IF EXISTS saved_games;

CREATE TABLE saved_games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    password TEXT NOT NULL,
    grid BLOB NOT NULL,
    turns INTEGER NOT NULL,
    coins INTEGER NOT NULL,
    total_score INTEGER NOT NULL
);