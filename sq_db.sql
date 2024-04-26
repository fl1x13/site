CREATE TABLE IF NOT EXISTS mainmenu (
id integer PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
url text NOT NULL
);

CREATE TABLE IF NOT EXISTS vechicle (
id INTEGER PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
description text NOT NULL,
price integer NOT NULL
);


CREATE TABLE IF NOT EXISTS  users (id integer PRIMARY KEY AUTOINCREMENT,
name text NOT NULL,
email text NOT NULL,
password text NOT NULL,
avatar BLOB DEFAULT NULL
);