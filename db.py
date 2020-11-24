import sqlite3
import os
import contextlib
import config


def initialize():
    if not os.path.exists(config.DB_FILENAME):
        with contextlib.closing(sqlite3.connect(config.DB_FILENAME)) as con:
            with con:
                cur = con.cursor()
                cur.execute('''
                CREATE TABLE user (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(255),    
                    username VARCHAR(255) UNIQUE,
                    n_of_followers INTEGER,
                    n_of_following INTEGER);
                    ''')
                cur.execute('''
                CREATE TABLE post (
                    post_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    link VARCHAR(255) UNIQUE NOT NULL,
                    n_of_likes INTEGER NOT NULL,
                    n_of_comments INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES user (user_id));
                    ''')
                cur.execute('''
                CREATE TABLE hashtag (
                    hashtag_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    value VARCHAR(255) UNIQUE NOT NULL);
                    ''')
                cur.execute('''
                CREATE TABLE post_hashtag (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    post_id INTEGER NOT NULL,
                    hashtag_id INTEGER NOT NULL,
                    FOREIGN KEY (post_id) REFERENCES post (post_id),
                    FOREIGN KEY (hashtag_id) REFERENCES hashtag (hashtag_id));
                    ''')


def add_user(name, username, n_of_followers, n_of_following):
    return execute("INSERT INTO user (name, username, n_of_followers, n_of_following) "
                   "VALUES (?, ?, ?, ?, ?, ?)",
                    [name, username, n_of_followers, n_of_following])


def add_simple_user(username):
    return execute("INSERT INTO user (username) "
                   "VALUES (?)",
                   [username])


def add_post(user_id, link, n_of_likes, n_of_comments):
    return execute("INSERT INTO post (user_id, link, n_of_likes, n_of_comments) "
                   "VALUES (?, ?, ?, ?)",
                   [user_id, link, n_of_likes, n_of_comments])


def add_hashtag(value):
    return execute("INSERT INTO hashtag (value) "
                   "VALUES (?)",
                   [value])


def add_post_hashtag(post_id, hashtag_id):
    return execute("INSERT INTO post_hashtag (post_id, hashtag_id) "
                   "VALUES (?, ?)",
                   [post_id, hashtag_id])


def execute(command, values):
    with contextlib.closing(sqlite3.connect(config.DB_FILENAME)) as con:
        with con:
            cur = con.cursor()
            try:
                cur.execute(command, values)
            except sqlite3.IntegrityError as ex:
                print(ex)
            else:
                return cur.lastrowid
