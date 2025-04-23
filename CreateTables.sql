CREATE TABLE Genres
(
    id   BIGINT PRIMARY KEY ,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE Games
(
    id          BIGINT PRIMARY KEY,
    name        VARCHAR(255) NOT NULL,
    min_players BIGINT,
    max_players BIGINT,
    info        TEXT
);

CREATE TABLE GenresToGames
(
    genre_id BIGINT NOT NULL,
    game_id  BIGINT NOT NULL,
    PRIMARY KEY (genre_id, game_id),
    FOREIGN KEY (genre_id) REFERENCES Genres (id) ON DELETE CASCADE,
    FOREIGN KEY (game_id) REFERENCES Games (id) ON DELETE CASCADE
);

CREATE TABLE Rules_Category
(
    id        BIGINT PRIMARY KEY,
    game_id   BIGINT       NOT NULL,
    parent_id BIGINT,
    name      VARCHAR(255) NOT NULL,
    FOREIGN KEY (game_id) REFERENCES Games (id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES Rules_Category (id) ON DELETE CASCADE
);

CREATE TABLE Rules
(
    id          BIGINT PRIMARY KEY,
    category_id BIGINT NOT NULL,
    content     TEXT,
    FOREIGN KEY (category_id) REFERENCES Rules_Category (id) ON DELETE CASCADE
);
