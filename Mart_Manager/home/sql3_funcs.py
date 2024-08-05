import sqlite3
import os
import cryptography
import cryptography.fernet

def nameDB(name):
    current_dir = os.path.join(os.path.abspath(__file__))
    db_dir = os.path.join(current_dir, '..', '..', 'db_files')
    db_actual = (os.path.normpath(os.path.join(db_dir, name)))
    return db_actual

def connect(dbName):
    con = sqlite3.connect(dbName)
    cur = con.cursor()
    return con, cur

def encrypt_user(name, passwd):
    key = cryptography.fernet.Fernet.generate_key()
    cyp = cryptography.fernet.Fernet(key)
    retName = cyp.encrypt(name.encode())
    retpasswd = cyp.encrypt(passwd.encode())
    return retName, retpasswd, key

def decrypt_user(name, passwd, key):
    cyp = cryptography.fernet.Fernet(key)
    retName = cyp.decrypt(name).decode()
    retpasswd = cyp.decrypt(passwd).decode()
    return retName, retpasswd

def retrieveUserLogin(uname, passwd):
    pass

def insertUser(uname, passwd):
    pass

#con, cur = connect(nameDB('userLogins.db'))
#query = """CREATE TABLE IF NOT EXISTS user(
#            id INTEGER PRIMARY KEY AUTOINCREMENT,
#            uname TEXT UNIQUE NOT NULL,
#            passwd TEXT NOT NULL
#            );"""
#cur.execute(query)
#con.commit()



