import mysql.connector
import config
import logging
import logger


def initialize():
    with open(config.AUTH_DB_FILE, "r") as file:
        host = file.readline().strip()
        user = file.readline().strip()
        password = file.readline().strip()

    with mysql.connector.connect(host=host, user=user, password=password) as conn:
        with conn:
            cur = conn.cursor()
            cur.execute("CREATE DATABASE IF NOT EXISTS insta")
            cur.execute("USE insta")
            cur.execute('''CREATE TABLE IF NOT EXISTS user (
                           user_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                           username VARCHAR(255) UNIQUE,
                           full_name VARCHAR(255),
                           followers INTEGER,
                           following INTEGER);
                           ''')
            cur.execute('''CREATE TABLE IF NOT EXISTS post (
                           post_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                           user_id INTEGER NOT NULL,
                           link VARCHAR(255) UNIQUE NOT NULL,
                           likes INTEGER,
                           FOREIGN KEY (user_id) REFERENCES user (user_id));
                           ''')
            cur.execute('''CREATE TABLE IF NOT EXISTS hashtag (
                           hashtag_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                           value VARCHAR(255) UNIQUE NOT NULL);
                           ''')
            cur.execute('''CREATE TABLE IF NOT EXISTS post_hashtag (
                           post_hashtag_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                           post_id INTEGER NOT NULL,
                           hashtag_id INTEGER NOT NULL,
                           FOREIGN KEY (post_id) REFERENCES post (post_id),
                           FOREIGN KEY (hashtag_id) REFERENCES hashtag (hashtag_id),
                           UNIQUE KEY (post_id, hashtag_id));
                           ''')
            cur.execute('''CREATE TABLE IF NOT EXISTS location (
                           location_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                           value VARCHAR(255) UNIQUE NOT NULL);
                           ''')
            cur.execute('''CREATE TABLE IF NOT EXISTS post_location (
                           post_location_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                           post_id INTEGER NOT NULL,
                           location_id INTEGER NOT NULL,
                           FOREIGN KEY (post_id) REFERENCES post (post_id),
                           FOREIGN KEY (location_id) REFERENCES location (location_id),
                           UNIQUE KEY (post_id, location_id));
                           ''')


def add_user(user):
    # If exists we return it, otherwise we create it
    username = user["username"]
    user_id = query_db(f"SELECT user_id FROM user WHERE username = '{username}'")

    if user_id:
        logger.log(logging.INFO, msg=f"User already exists - Not creating: {username}")
        return user_id[0]
    else:
        logger.log(logging.INFO, msg=f"Created User: {username}")
        return add_to_db("INSERT INTO user (username, full_name, followers, following) "
                         "VALUES (%s, %s, %s, %s)",
                         [username,
                          user["full_name"],
                          user["followers"],
                          user["following"]])


def add_simple_user(username):
    # If exists we return it, otherwise we create it
    user_id = query_db(f"SELECT user_id FROM user WHERE username = '{username}'")

    if user_id:
        logger.log(logging.INFO, msg=f"User already exists - Not creating: {username}")
        return user_id[0]
    else:
        logger.log(logging.INFO, msg=f"Created Simple User: {username}")
        return add_to_db("INSERT INTO user (username) "
                         "VALUES (%s)",
                         [username])


def add_post(user_id, link, likes):
    # If exists we return it, otherwise we create it
    post_id = query_db(f"SELECT post_id FROM post WHERE link = '{link}'")

    if post_id:
        logger.log(logging.INFO, msg=f"Post already exists - Not creating:{link}")
        return post_id[0]
    else:
        logger.log(logging.INFO, msg=f"Created Post: {link}")
        return add_to_db("INSERT INTO post (user_id, link, likes) "
                         "VALUES (%s, %s, %s)",
                         [user_id, link, likes])


def add_hashtag(value):
    # If exists we return it, otherwise we create it
    hash_id = query_db(f"SELECT hashtag_id FROM hashtag WHERE value = '{value}'")

    if hash_id:
        logger.log(logging.INFO, msg=f"Hashtag already exists - Not creating:{value}")
        return hash_id[0]
    else:
        logger.log(logging.INFO, msg=f"Created Hashtag:{value}")
        return add_to_db("INSERT INTO hashtag (value) "
                         "VALUES (%s)",
                         [value])


def add_post_hashtag(post_id, hashtag_id):
    # If exists we return it, otherwise we create it
    ph_id = query_db(f"SELECT post_hashtag_id FROM post_hashtag "
                     f"WHERE post_id = '{post_id}' AND hashtag_id = '{hashtag_id}'")

    if ph_id:
        return ph_id[0]
    else:
        return add_to_db("INSERT INTO post_hashtag (post_id, hashtag_id) "
                         "VALUES (%s, %s)",
                         [post_id, hashtag_id])


def add_location(value):
    # If exists we return it, otherwise we create it
    hash_id = query_db(f"SELECT location_id FROM location WHERE value = '{value}'")

    if hash_id:
        logger.log(logging.INFO, msg=f"Location already exists - Not creating:{value}")
        return hash_id[0]
    else:
        logger.log(logging.INFO, msg=f"Created location:{value}")
        return add_to_db("INSERT INTO location (value) "
                         "VALUES (%s)",
                         [value])


def add_post_location(post_id, location_id):
    # If exists we return it, otherwise we create it
    ph_id = query_db(f"SELECT post_location_id FROM post_location "
                     f"WHERE post_id = '{post_id}' AND location_id = '{location_id}'")

    if ph_id:
        return ph_id[0]
    else:
        return add_to_db("INSERT INTO post_location (post_id, location_id) "
                         "VALUES (%s, %s)",
                         [post_id, location_id])


def query_db(command):
    with open(config.AUTH_DB_FILE, "r") as file:
        host = file.readline().strip()
        user = file.readline().strip()
        password = file.readline().strip()

    conn = mysql.connector.connect(host=host, user=user, password=password, database="insta")
    cur = conn.cursor(buffered=True)
    try:
        cur.execute(command)
        conn.commit()
        return cur.fetchone()
    except Exception as ex:
        print(ex)


def add_to_db(command, values):
    with open(config.AUTH_DB_FILE, "r") as file:
        host = file.readline().strip()
        user = file.readline().strip()
        password = file.readline().strip()

    conn = mysql.connector.connect(host=host, user=user, password=password, database="insta")
    cur = conn.cursor(buffered=True)
    try:
        cur.execute(command, values)
        conn.commit()
        return cur.lastrowid
    except Exception as ex:
        print(ex)



