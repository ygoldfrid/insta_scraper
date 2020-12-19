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
            cur.execute(f"CREATE DATABASE IF NOT EXISTS {config.DB_NAME}")
            cur.execute(f"USE {config.DB_NAME}")
            cur.execute('''CREATE TABLE IF NOT EXISTS user (
                           user_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                           username VARCHAR(255) UNIQUE,
                           full_name VARCHAR(255),
                           followers INTEGER,
                           following INTEGER,
                           posts INTEGER,
                           igtv_posts INTEGER,
                           bio VARCHAR(255),
                           external_url VARCHAR(255),
                           is_private BOOLEAN,
                           is_verified BOOLEAN,
                           is_business_account BOOLEAN,
                           business_category_name VARCHAR(255),
                           is_joined_recently BOOLEAN);
                           ''')
            cur.execute('''CREATE TABLE IF NOT EXISTS post (
                           post_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                           user_id INTEGER NOT NULL,
                           link VARCHAR(255) UNIQUE NOT NULL,
                           caption VARCHAR(255),
                           likes INTEGER,
                           comments INTEGER,
                           is_video BOOLEAN,
                           views INTEGER,
                           temperature INTEGER,
                           weather VARCHAR(255),
                           timestamp INTEGER,
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
                           name VARCHAR(255) NOT NULL,
                           slug VARCHAR(255) UNIQUE,
                           country VARCHAR(255),
                           city VARCHAR(255),
                           latitude INT,
                           longitude INT);
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
    user_id = query_db("SELECT user_id FROM user WHERE username = '{}'".format(user["username"]))

    if user_id:
        logger.log(logging.INFO, msg="User already exists - Not creating: {}".format(user["username"]))
        return user_id[0]
    else:
        logger.log(logging.INFO, msg="Created User: {}".format(user["username"]))
        return add_to_db("INSERT INTO user ("
                         "username, "
                         "full_name, "
                         "followers, "
                         "following, "
                         "posts, "
                         "igtv_posts, "
                         "bio, "
                         "external_url, "
                         "is_private, "
                         "is_verified, "
                         "is_business_account, "
                         "business_category_name, "
                         "is_joined_recently) "
                         "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                         [user["username"],
                          user["full_name"],
                          user["followers"],
                          user["following"],
                          user["posts"],
                          user["igtv_posts"],
                          user["bio"],
                          user["external_url"],
                          user["is_private"],
                          user["is_verified"],
                          user["is_business_account"],
                          user["business_category_name"],
                          user["is_joined_recently"]])


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


def add_post(user_id, post):
    # If exists we return it, otherwise we create it
    post_id = query_db("SELECT post_id FROM post WHERE link = '{}'".format(post["link"]))

    if post_id:
        logger.log(logging.INFO, msg="Post already exists - Not creating: {}".format(post["link"]))
        return post_id[0]
    else:
        logger.log(logging.INFO, msg="Created Post: {}".format(post["link"]))
        return add_to_db("INSERT INTO post ("
                         "user_id, "
                         "link, "
                         "caption, "
                         "likes, "
                         "comments, "
                         "is_video, "
                         "views, "
                         "temperature, "
                         "weather, "
                         "timestamp) "
                         "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                         [user_id,
                          post["link"],
                          post["caption"],
                          post["likes"],
                          post["comments"],
                          post["is_video"],
                          post["views"],
                          post["temperature"],
                          post["weather"],
                          post["timestamp"]])


def add_simple_post(user_id, link, likes):
    # If exists we return it, otherwise we create it
    post_id = query_db(f"SELECT post_id FROM post WHERE link = '{link}'")

    if post_id:
        logger.log(logging.INFO, msg=f"Post already exists - Not creating: {link}")
        return post_id[0]
    else:
        logger.log(logging.INFO, msg=f"Created Simple Post: {link}")
        return add_to_db("INSERT INTO post (user_id, link, likes) "
                         "VALUES (%s, %s, %s)",
                         [user_id, link, likes])


def add_hashtag(value):
    # If exists we return it, otherwise we create it
    hash_id = query_db(f"SELECT hashtag_id FROM hashtag WHERE value = '{value}'")

    if hash_id:
        logger.log(logging.INFO, msg=f"Hashtag already exists - Not creating: {value}")
        return hash_id[0]
    else:
        logger.log(logging.INFO, msg=f"Created Hashtag: {value}")
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


def add_location(location):
    # If exists we return it, otherwise we create it
    hash_id = query_db("SELECT location_id FROM location WHERE name = '{}'".format(location["name"]))

    if hash_id:
        logger.log(logging.INFO, msg="Location already exists - Not creating: {}".format(location["name"]))
        return hash_id[0]
    else:
        logger.log(logging.INFO, msg="Created Location: {}".format(location["slug"]))
        return add_to_db("INSERT INTO location ("
                         "name, "
                         "slug, "
                         "country, "
                         "city, "
                         "latitude, "
                         "longitude) "
                         "VALUES (%s, %s, %s, %s, %s, %s)",
                         [location["name"],
                          location["slug"],
                          location["country"],
                          location["city"],
                          location["latitude"],
                          location["longitude"]])


def add_simple_location(name):
    # If exists we return it, otherwise we create it
    hash_id = query_db(f"SELECT location_id FROM location WHERE name = '{name}'")

    if hash_id:
        logger.log(logging.INFO, msg=f"Location already exists - Not creating: {name}")
        return hash_id[0]
    else:
        logger.log(logging.INFO, msg=f"Created Simple Location: {name}")
        return add_to_db("INSERT INTO location (name) "
                         "VALUES (%s)",
                         [name])


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

    conn = mysql.connector.connect(host=host, user=user, password=password, database=f"{config.DB_NAME}")
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

    conn = mysql.connector.connect(host=host, user=user, password=password, database=f"{config.DB_NAME}")
    cur = conn.cursor(buffered=True)
    try:
        cur.execute(command, values)
        conn.commit()
        return cur.lastrowid
    except Exception as ex:
        print(ex)



