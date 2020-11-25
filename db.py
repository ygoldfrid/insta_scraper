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
                    n_of_likes INTEGER,
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
                    FOREIGN KEY (hashtag_id) REFERENCES hashtag (hashtag_id)
                    UNIQUE(post_id, hashtag_id));
                    ''')


def add_user(name, username, n_of_followers, n_of_following):
    user_id = add_to_db("INSERT INTO user (name, username, n_of_followers, n_of_following) "
                        "VALUES (?, ?, ?, ?, ?, ?)",
                        [name, username, n_of_followers, n_of_following])
    if user_id:
        return user_id
    else:
        return query_db(f"SELECT id FROM user WHERE username = {username}")


def add_simple_user(username):
    # If exists we return it, otherwise we create it
    user_id = query_db(f"SELECT user_id FROM user WHERE username = '{username}'")

    if user_id:
        print("User already exists - Not creating:", username)
        return user_id[0]
    else:
        print("Created User:", username)
        return add_to_db("INSERT INTO user (username) "
                         "VALUES (?)",
                         [username])


def add_post(user_id, link, n_of_likes):
    # If exists we return it, otherwise we create it
    post_id = query_db(f"SELECT post_id FROM post WHERE link = '{link}'")

    if post_id:
        print("Post already exists - Not creating:", link)
        return post_id[0]
    else:
        print("Created Post:", link)
        return add_to_db("INSERT INTO post (user_id, link, n_of_likes) "
                         "VALUES (?, ?, ?)",
                         [user_id, link, n_of_likes])


def add_hashtag(value):
    # If exists we return it, otherwise we create it
    hash_id = query_db(f"SELECT hashtag_id FROM hashtag WHERE value = '{value}'")

    if hash_id:
        print("Hashtag already exists - Not creating:", value)
        return hash_id[0]
    else:
        print("Created Hashtag:", value)
        return add_to_db("INSERT INTO hashtag (value) "
                         "VALUES (?)",
                         [value])


def add_post_hashtag(post_id, hashtag_id):
    # If exists we return it, otherwise we create it
    ph_id = query_db(f"SELECT id FROM post_hashtag WHERE post_id = '{post_id}' AND hashtag_id = '{hashtag_id}'")

    if ph_id:
        return ph_id[0]
    else:
        return add_to_db("INSERT INTO post_hashtag (post_id, hashtag_id) "
                         "VALUES (?, ?)",
                         [post_id, hashtag_id])


def query_db(command):
    with contextlib.closing(sqlite3.connect(config.DB_FILENAME)) as con:
        with con:
            cur = con.cursor()
            try:
                cur.execute(command)
                return cur.fetchone()
            except sqlite3.IntegrityError as ex:
                print(ex)


def add_to_db(command, values):
    with contextlib.closing(sqlite3.connect(config.DB_FILENAME)) as con:
        with con:
            cur = con.cursor()
            try:
                cur.execute(command, values)
            except sqlite3.IntegrityError as ex:
                print(ex)
            else:
                return cur.lastrowid


