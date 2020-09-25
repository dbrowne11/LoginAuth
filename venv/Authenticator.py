import hashlib
import os
import sqlite3



def connectDB():
    """
    creates a connection object to Users.db
    :return: connection object to Users.db database
    """
    # get absolute path to db
    BASEDIR = os.path.dirname(os.path.abspath(__file__))
    dbPath = os.path.join(BASEDIR, 'Users.db')
    # connect to SQLDatabase
    conn = sqlite3.connect(dbPath)
    return conn

def createCursor(connection):
    """
    creates cursor object for specified db connection
    :param connection: connection object to a database
    :return: cursor object for the connection
    """
    return connection.cursor()


def hash(password, salt=None):
    """
    :param password: User entered password
    :param salt: salt, can be None for randomly generated salt
    :return: tuple containing (salt, hash)
    """
    if salt == None:
        salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000
    )
    return salt, key

def verify(username, pswd):
    """
    Verifies a Username/Password combination
    :param username: user entered username
    :param pswd: user entered password
    :return: True if user/password combo is in the database, False otherwise
    """
    db.execute("SELECT salt, hash FROM users WHERE username = ?;", (username,))
    try:
        dbSalt, dbHash = db.fetchone()
        salt, attemptHash = hash(pswd, dbSalt)
    except TypeError:
        return False
    if attemptHash != dbHash:
        return False
    else:
        return True


def add_user(user = None, pswd = None):
    """
    Add user to DB, when called without parameters, it prompts the user for a username and password
    :param user: Username to create account with OR None
    :param pswd: Password to create account with OR None
    :return: None
    """
    if user == None:
        while True:
            user = input("Choose a Username: ")
            if valUsername(user):
                break
    if pswd == None:
        while True:
            pswd = input("Choose a Password: ")     # prompt user for username and password
            if valPassword(pswd):
                break
    salt, key = hash(pswd)                  # hash pswd to get user-specific salt and hash
    values = user, salt, key
    db.execute("INSERT INTO users VALUES (?, ?, ?)", (user, salt, key))
    conn.commit()
    return

def valUsername(username):
    """
    Validates that a username is not present in database
    :param username: User entered username
    :return: True if username is available, False otherwise
    """
    db.execute("SELECT username from users")
    currentUsers = db.fetchall()
    for taken in currentUsers:
        if username == taken[0]:
            return False
    return True

def valPassword(password):
    """
    Ensures password meets criteria
    :param password: User's password
    :return: True if password meets the criteria, Flase otherwise
    """
    if len(password) < 8:
        return False
    if password.islower() or password.isupper():
        return False
    return True

conn = connectDB()
db = createCursor(conn)

