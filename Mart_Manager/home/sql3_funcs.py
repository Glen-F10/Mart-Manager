print("SQL3_FUNCS Loading...")
import sqlite3
import os
import cryptography
import cryptography.fernet 
import re
import logfuncs
#from . import logfuncs
from datetime import date

sqlite3.register_adapter(date, lambda d: d.isoformat())#to convert date to iso format (SQL3 compatible)

def cleanData(value:str|int, option:int=0) -> bool:
    try:
        if option == 1:
            include = r'[0-9a-zA-Z_]'
            returnValue = re.sub(include, '', value)
            if len(returnValue) > 0:
                #---Log start---
                message = "CLEAN DATA UNSUCCESSFUL in function sql3_funcs.cleanData()"
                program = "home app"
                error = f"Invalid Data {value} given"
                logfuncs.insertlog("NA", "NA", program, message, error, None)
                #---Log end---
                return False
            else:
                #---Log start---
                message = "CLEAN DATA SUCCESSFUL in function sql3_funcs.cleanData()"
                program = "home app"
                logfuncs.insertlog("NA", "NA", program, message, None, None)
                #---Log end---
                return True
        else:
            #---Log start---
            message = "CLEAN DATA UNSUCCESSFUL in function sql3_funcs.cleanData()"
            program = "home app"
            error = f"Invalid option value {option}"
            logfuncs.insertlog("NA", "NA", program, message, None, None)
            #---Log end---
            return False
    except Exception as e:
        #---Log start---
        message = "EXCEPTION OCCURED in function sql3_funcs.cleanData()"
        program = "home app"
        logfuncs.insertlog("NA", "NA", program, message, None, e)
        #---Log end---
        return False

def nameDB(name: str):
    """
    Will return a path of the sqlite3 db which is stored outside the app folder but is stored in main folder.

    Parameters:
    name (str): name of the db file example given below

    Returns:
    string: returns a path to the db folder in the current system

    Example:
    >>> nameDB('sqlfile.db')
    path/in/current/directory/to/sqlfile.db
    """
    current_dir = os.path.join(os.path.abspath(__file__))   
    db_dir = os.path.join(current_dir, '..', '..', 'db_files')
    db_actual = (os.path.normpath(os.path.join(db_dir, name)))
    return db_actual

def connect(dbName: str):
    """
    Will create a db or return a existing db's (sqlite3) connection and curser.

    Parameters:
    name (str): name of the db for, for current program combine this with nameDB() function, example given below

    Returns:
    Tuple[Connection, Cursor]: returns connection and cursor for the given db

    Example:
    >>> con, cur =connect(nameDB('dbFileName.db'))
    """
    try:
        con = sqlite3.connect(dbName)
        cur = con.cursor()
        #---Log start---
        message = "DB CONNECTION SUCCESSFUL in function sql3_funcs.connect()"
        program = "home app"
        logfuncs.insertlog("NA", "NA", program, message, None, None)
        #---Log end---
        return con, cur
    except sqlite3.Error as e:
        #---Log start---
        message = "ERROR OCCURED in function sql3_funcs.connect()"
        program = f"home app/DB connection {dbName}"
        logfuncs.insertlog("NA", "NA", program, message, e, None)
        #---Log end---
        return False
    except Exception as e:
        #---Log start---
        message = "EXCEPTION OCCURED in function sql3_funcs.connect()"
        program = "home app"
        logfuncs.insertlog("NA", "NA", program, message, None, e)
        #---Log end---
        return False

def retLastID(tablename: str)-> (int|bool):
    """
    Will Return the last id in the db, used with inserUser() function

    Parameters:
    tablename (str): tablename from which the last id is to be retrieved

    Returns:
    LastID (int or Boolean): May return id else will return False

    Example:
    >>> retLastID('user')
    22
    """
    try:
        con, cur = connect(nameDB('userLogins.db'))
        cur.execute(f"SELECT MAX(id) FROM {tablename};")
        lastID = cur.fetchone()[0]
        if lastID is None:
            lastID = 1
            con.close()
            #---Log start---
            message = "LAST ID RETRIEVED SUCCESSFULLY in function sql3_funcs.retLastID()"
            program = "home app"
            logfuncs.insertlog("NA", "NA", program, message, None, None)
            #---Log end---
            return lastID
        else:
            lastID = lastID + 1
            con.close()
            #---Log start---
            message = "LAST ID RETRIEVED SUCCESSFULLY in function sql3_funcs.retLastID()"
            program = "home app"
            logfuncs.insertlog("NA", "NA", program, message, None, None)
            #---Log end---
            return lastID
    except sqlite3.Error as e:
        #---Log start---
        message = "ERROR OCCURED in function sql3_funcs.retLastID()"
        program = "home app"
        logfuncs.insertlog("NA", "NA", program, message, e, None)
        #---Log end---
        return False
    except Exception as e:
        #---Log start---
        message = "EXCEPTION OCCURED in function sql3_funcs.retLastID()"
        program = "home app"
        logfuncs.insertlog("NA", "NA", program, message, None, e)
        #---Log end---
        return False
    


def encrypt_user(name: str, passwd: str):
    """
    retruns a encrypted username, password and key for given details.

    Parameters:
    name (str): Username to Encrypt
    passwd (str): Password to Encrypt

    Example:
    >>> encrypt_user('username','password')
    """
    try:
        key = cryptography.fernet.Fernet.generate_key()
        cyp = cryptography.fernet.Fernet(key)
        retName = cyp.encrypt(name.encode())
        retpasswd = cyp.encrypt(passwd.encode())
        return retName, retpasswd, key
    except Exception as e:
        #---Log start---
        message = "EXCEPTION OCCURED in function sql3_funcs.encrypt_user()"
        program = "home app"
        logfuncs.insertlog("NA", "NA", program, message, None, e)
        #---Log end---
        return False

def decrypt_user(name, passwd, key):
    try:
        cyp = cryptography.fernet.Fernet(key)
        retName = cyp.decrypt(name).decode()
        retpasswd = cyp.decrypt(passwd).decode()
        return retName, retpasswd
    except Exception as e:
        #---Log start---
        message = "EXCEPTION OCCURED in function sql3_funcs.decrypt_user()"
        program = "home app"
        logfuncs.insertlog("NA", "NA", program, message, None, e)
        #---Log end---
        return False

def retrieveUserLogin(uname: str, upasswd: str):
    try:
        if cleanData(uname, 1) is True and cleanData(upasswd, 1) is True:
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
                    flag = 1
                    break
                else:
                    pass
            if flag == 1:
                #---Log start---
                message = "USER LOGIN Retrieved SUCCESSFULLY in function sql3_funcs.retrieveUserLogin()"
                program = "home app"
                logfuncs.insertlog("NA", "NA", program, message, None, None)
                #---Log end---
                err = None
                return True
            else:
                #---Log start---
                message = "USER LOGIN NOT Retrieved SUCCESSFULLY in function sql3_funcs.retrieveUserLogin()"    
                program = "home app"
                Error = f"User Not Found {uname} {upasswd}"
                logfuncs.insertlog("NA", "NA", program, message, Error, None)
                #---Log end---
                return False
        else:
            #---Log start---
            message = "USER LOGIN NOT Retrieved SUCCESSFULLY in function sql3_funcs.retrieveUserLogin()"
            program = "home app"
            Error = f"Invalid Data {uname} {upasswd}, Did not pass validation in sql3_funcs.cleanData()"
            logfuncs.insertlog("NA", "NA", program, message, Error, None)
            #---Log end---
            return False
    except sqlite3.Error as e:
        #---Log start---
        message = "ERROR OCCURED in function sql3_funcs.retrieveUserLogin()"
        program = "home app"
        logfuncs.insertlog("NA", "NA", program, message, e, None)
        #---Log end---
        return False
    except Exception as e:
        #---Log start---
        message = "EXCEPTION OCCURED in function sql3_funcs.retrieveUserLogin()"
        program = "home app"
        logfuncs.insertlog("NA", "NA", program, message, e, None)
        #---Log end---
        return False

def insertUser(uname, upasswd):
    try:
        name, passwd, key = encrypt_user(uname, upasswd)
        con, cur = connect(nameDB('userLogins.db'))
        lastID = retLastID('user')
        if lastID is False:
            #---Log start---
            message = "LAST ID NOT RETRIEVED SUCCESSFULLY in function sql3_funcs.insertUser()"
            program = "home app"
            error = "LAST ID NOT RETRIEVED SUCCESSFULLY FROM sql3_funcs.retLastID()"
            logfuncs.insertlog("NA", "NA", program, message, error, None)
            #---Log end---
            return False
        else:
            values1 = (lastID, name, passwd,)
            query1 = cur.execute("INSERT INTO user VALUES(?,?,?);", values1)
            values2 = (lastID, key)
            query2 = cur.execute("INSERT INTO key VALUES(?,?)", values2)
            con.commit()
            con.close()
            #---Log start---
            message = "USER INSERTED SUCCESSFULLY in function sql3_funcs.insertUser()"
            program = "home app"
            logfuncs.insertlog("NA", "NA", program, message, None, None)
            #---Log end---
            return True
    except sqlite3.Error as e:
        #---Log start---
        message = "ERROR OCCURED in function sql3_funcs.insertUser()"
        program = "home app"
        logfuncs.insertlog("NA", "NA", program, message, e, None)
        #---Log end---
        return False
    except Exception as e:
        #---Log start---
        message = "EXCEPTION OCCURED in function sql3_funcs.insertUser()"
        program = "home app"
        logfuncs.insertlog("NA", "NA", program, message, None, e)
        #---Log end---
        return False

def deleteUser(uname: str):
    try:
        flag = 0
        to_delete_user_id = None

        #Selecting all values in user and their respective keys
        con, cur = connect(nameDB('userLogins.db'))
        query1 = ("""SELECT u.id, u.uname, u.passwd, k.key
                    FROM user u
                    Join key k ON u.id=k.id""")
        cur.execute(query1)
        values = cur.fetchall()

        #checking for username in DB and retrieving userID
        for value in values:
            dname, dpasswd =decrypt_user(value[1], value[2], value[3])
            del dpasswd #not needed
            if dname == uname:#because username is unique
                flag = 1
                to_delete_user_id = value[0]
                break
            else:
                pass
        if flag == 0:
            #---Log start---
            message = "USER NOT FOUND in function sql3_funcs.deleteUser()"
            program = "home app"
            error = f"User Not Found {uname}"
            logfuncs.insertlog("NA", "NA", program, message, error, None)
            #---Log end---
            return False
        else:
            #if User Found
            query2, query3 = "DELETE FROM user WHERE id=?;", "DELETE FROM key WHERE id=?;"
            value = to_delete_user_id
            cur.execute(query2, (value,))
            con.commit()
            cur.execute(query3,(value,))
            con.commit()
            con.close()
            #---Log start---
            message = "USER DELETED SUCCESSFULLY in function sql3_funcs.deleteUser()"
            program = "home app"
            logfuncs.insertlog("NA", "NA", program, message, None, None)
            #---Log end---
            return True
    except sqlite3.Error as e:
        #---Log start---
        message = "ERROR OCCURED in function sql3_funcs.deleteUser()"
        program = "home app"
        logfuncs.insertlog("NA", "NA", program, message, e, None)
        #---Log end---
        return False
    except Exception as e:
        #---Log start---
        message = "EXCEPTION OCCURED in function sql3_funcs.deleteUser()"
        program = "home app"
        logfuncs.insertlog("NA", "NA", program, message, None, e)
        #---Log end---
        return False

def userDetailsOps(uname:str, option:int=0)->str|list:#Finish this function implementation
    try:
        if option == 1:
            flag = 0
            returnUserDetails = []
            query = """SELECT k.key, u.id, u.uname, u.passwd, d.UserType, d.UserFName, d.UserMName, d.UserLName, d.UserEmail, d.UserPhone,  d.UserMessageID, d.UserEmailID, d.LastPageURL
                       FROM user u
                       Join userDetails d ON u.id = d.id
                       JOIN key k ON u.id = k.id;"""
            con, cur = connect(nameDB('userLogins.db'))
            cur.execute(query)
            rows = cur.fetchall()
            con.close()
            for row in rows:
                tocheck, toignore = decrypt_user(row[2], row[3], row[0])
                del toignore
                if tocheck == uname:
                    flag = 1
                    returnUserDetails.append(row[1])
                    returnUserDetails.append(tocheck)
                    for i in range(4,len(row)):
                        returnUserDetails.append(row[i])
                    break
                else:
                    pass
            if flag == 1:
                #---Log start---
                message = "USER DETAILS RETRIEVED SUCCESSFULLY in function sql3_funcs.userDetailsOps()"
                program = "home app"
                logfuncs.insertlog("NA", "NA", program, message, None, None)
                #---Log end---
                return returnUserDetails
            else:
                #---Log start---
                message = "USER NOT FOUND in function sql3_funcs.userDetailsOps()"
                program = "home app"
                error = f"User Not Found {uname}"
                logfuncs.insertlog("NA", "NA", program, message, error, None)
                #---Log end---
                return False
    except Exception as e:
        #---Log start---
        message = "EXCEPTION OCCURED in function sql3_funcs.userDetailsOps()"
        program = "home app"
        logfuncs.insertlog("NA", "NA", program, message, None, e)
        #---Log end---
        return False

print("SQL3_FUNCS Loaded...")

#Test Functions Below this line





#Below Code is for testing purposes

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

#con, cur = connect(nameDB('userLogins.db'))
#query = """CREATE TABLE IF NOT EXISTS key(
#            id INTEGER,
#            key TEXT NOT NULL,
#            FOREIGN KEY (id) REFERENCES user(id)
#            );"""
#cur.execute(query)
#con.commit()

"""
con, cur = connect(nameDB('userLogins.db'))
cur.execute("SELECT * FROM user")
users = cur.fetchall()
cur.execute("SELECT * FROM key")
keys = cur.fetchall()
for user in users:
    print(user)
for key in keys:
    print(key)
"""

#Test Functions Below this line
#con, cur = connect(nameDB('userLogins.db'))
#query = """CREATE TABLE IF NOT EXISTS userDetails(
#            id INTEGER,
#            UserType TEXT NOT NULL,
#            UserFName TEXT NOT NULL,
#            UserMName TEXT,
#            UserLName TEXT NOT NULL,
#            UserEmail TEXT,
#            UserPhone TEXT,
#            UserMessageID TEXT NOT NULL,
#            UserEmailID TEXT NOT NULL,
#            LastPageURL TEXT NOT NULL,
#            FOREIGN KEY (id) REFERENCES user(id)
#            );"""
#cur.execute(query)
#con.commit()

#print(userDetailsOps('Glen', 1))

"""
def insertIntoUserDetails_test():
    values = (2, "Employee-Online", "Gladys", "", "Furtado", "Julianagladysfurtado@gmail.com", '9945936587', "1011", "gladys@Mart-Manager", "Home")
    query = "INSERT INTO userDetails VALUES (?,?,?,?,?,?,?,?,?,?);"
    con, cur = connect(nameDB('userLogins.db'))
    cur.execute(query,values)
    con.commit()
"""
"""
con, cur = connect(nameDB('userLogins.db'))
cur.execute("Select * from user")
rows = cur.fetchall()
cur.execute("Select * from key")
rows2 = cur.fetchall()
for row in rows:
    for row2 in rows2:
        if row[0] == row2[0]:
            print(decrypt_user(row[1], row[2], row2[1]))
"""
"""
con, cur = connect(nameDB('userLogins.db'))
cur.execute("Select * from userDetails;")
rows = cur.fetchall()
for row in rows:
    print(row)
"""
#retrieveUserLogin("Glen", "2001")2 = id
#retrieveUserLogin("Gladys", "1965")3 = id
#print(userDetailsOps('Glen', 1))
