CREATE TABLE usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    senha_hash TEXT NOT NULL
);

CREATE TABLE desenvolvedora (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
);

CREATE TABLE distribuidora (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
);

CREATE TABLE jogo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    genero TEXT,
    plataformas TEXT,
    ano INTEGER,
    desenvolvedora_id INTEGER,
    distribuidora_id INTEGER,
    FOREIGN KEY (desenvolvedora_id) REFERENCES desenvolvedora(id),
    FOREIGN KEY (distribuidora_id) REFERENCES distribuidora(id)
);

CREATE TABLE avaliacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    jogo_id INTEGER,
    tempo REAL,
    nota INTEGER,
    comentario TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id),
    FOREIGN KEY (jogo_id) REFERENCES jogo(id)
);
