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

def retLastID(tablename):
    try:
        con, cur = connect(nameDB('userLogins.db'))
        cur.execute(f"SELECT MAX(id) FROM {tablename};")
        lastID = cur.fetchone()[0]
        if lastID is None:
            lastID = 1
            con.close()
            return lastID
        else:
            lastID = lastID + 1
            con.close()
            return lastID
    except sqlite3.Error as e:
        print('ERROR OCCURED:in function retLastID():->',e)
        return False
    except Exception as e:
        print('EXCEPTION OCCURED:in function retLastID():->',e)
        return False

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

def retrieveUserLogin(uname, upasswd):
    try:
        flag = 0
        con, cur = connect(nameDB('userLogins.db'))
        queryRet = """SELECT u.id, u.uname, u.passwd, k.key
                      FROM user u
                      JOIN key k ON u.id = k.id"""
        cur.execute(queryRet)
        values = cur.fetchall()
        con.close()
        for value in values:
            dname, dpasswd = decrypt_user(value[1], value[2], value[3])
            if dname == uname and dpasswd == upasswd:
                print(dname, dpasswd)
                flag = 1
                break
            else:
                pass
        if flag == 1:
            print("NOTE : in function retrieveUserLogin():-> User Retrieval Successful")
            err = None
            return True, err
        else:
            print("NOTE : in function retrieveUserLogin():-> User Retrieval Unsuccessful, REASON::USER NOT FOUND")
            err =  "User Not Found"
            return False, err
    except sqlite3.Error as e:
        print("ERROR OCCURED in function retrieveUserLogin():->", e)
        err = "ERROR IN Database"
        return False, err
    except Exception as e:
        print("EXCEPTION OCCURED in function retrieveUserLogin():->", e)
        err = "EXCEPTION OCCURED"
        return False, err

def insertUser(uname, upasswd):
    try:
        name, passwd, key = encrypt_user(uname, upasswd)
        con, cur = connect(nameDB('userLogins.db'))
        lastID = retLastID('user')
        if lastID is False:
            print('EXCEPTION OCCURED in function insertUser() While Calling retLastID()')
            return False
        else:
            values1 = (lastID, name, passwd,)
            query1 = cur.execute("INSERT INTO user VALUES(?,?,?);", values1)
            values2 = (lastID, key)
            query2 = cur.execute("INSERT INTO key VALUES(?,?)", values2)
            con.commit()
            con.close()
            return True
    except sqlite3.Error as e:
        print('ERROR OCCURED:in function insertUser():->',e)
        return False
    except Exception as e:
        print('EXCEPTION OCCURED:in function insertUser():->',e)
        return False

#con, cur = connect(nameDB('userLogins.db'))
#query = """CREATE TABLE IF NOT EXISTS user(
#            id INTEGER PRIMARY KEY AUTOINCREMENT,
#            uname TEXT UNIQUE NOT NULL,
#            passwd TEXT NOT NULL
#            );"""
#cur.execute(query)
#con.commit()

#table 'user' stores user deatils
#table 'key' stores encryption keys

#s = cur.execute("select name from sqlite_master where type='table';")

"""
con, cur = connect(nameDB('userLogins.db'))
s = cur.execute("select * from user;")
v = s.fetchall()
print(v)
"""


#con, cur = connect(nameDB('userLogins.db'))
#query = """CREATE TABLE IF NOT EXISTS key(
#            id INTEGER,
#            key TEXT NOT NULL,
#            FOREIGN KEY (id) REFERENCES user(id)
#            );"""
#cur.execute(query)
#con.commit()

retrieveUserLogin("GLEN1010", "2001")
