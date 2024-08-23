print("Log Funcs Loading...")
#home.sql3_funcs
import sqlite3
import os

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
        return con, cur
    except sqlite3.Error as e:
        #---Log start---
        message = "ERROR OCCURED in function sql3_funcs.connect()"
        program = f"home app/DB connection {dbName}"
        insertlog("NA", "NA", program, message, e, None)
        #---Log end---
        return False
    except Exception as e:
        #---Log start---
        message = "EXCEPTION OCCURED in function sql3_funcs.connect()"
        program = "home app"
        insertlog("NA", "NA", program, message, None, e)
        #---Log end---
        return False

def getdatetime():
    import datetime
    import time
    return datetime.date.today(), datetime.datetime.now().time()

def lastid(option: int = 0):
    try:
        con, cur = connect(nameDB('SystemLogs.db'))
        if option == 0:
            print("NOTE : in function lastid():-> Option 0 is Invalid")
            return None
        elif option == 1:
            query = ("SELECT MAX(logID) FROM userLog;")
            cur.execute(query)
            return cur.fetchone()[0]
        elif option == 2:
            query = ("SELECT MAX(logID) FROM errorLog;")
            cur.execute(query)
            return cur.fetchone()[0]
        elif option == 3:
            query = ("SELECT MAX(logID) FROM exceptionLog;")
            cur.execute(query)
            return cur.fetchone()[0]
        else:
            print("NOTE : in function lastid():-> Option is Invalid")
            return None
    except Exception as e:
        print("ERROR : in function lastid():->", e)
        return None
    finally:
        con.close()

def insertlog(uid: str, uname: str, progname: str, LogAction: str, LogError: str = None, LogException: str = None):
    """
    Inserts a log entry into the database.

    Parameters:
    uid (str): The user ID.
    uname (str): The user name.
    progname (str): The program name.
    LogAction (str): The log action.
    LogError (str): The log error (optional).
    LogException (str): The log exception (optional).

    Returns:
    bool: True if the log entry was inserted successfully, False otherwise.
    """
    try:
        if LogAction is not None and LogError is None and LogException is None:
            try:
                con, cur = connect(nameDB('SystemLogs.db'))
                date, timeorg = getdatetime()
                time = timeorg.strftime("%H:%M:%S")
                if lastid(1) is not None:
                    logid = lastid(1) + 1
                else:
                    logid = 1
                query = ("INSERT INTO userLog VALUES (?, ?, ?, ?, ?, ?, ?);")
                values = (logid, uid, uname, progname, date, time, LogAction)
                cur.execute(query, values)
                con.commit()
                return True
            except Exception as e:
                print("ERROR : in function insertlog():->", e)
            finally:
                con.close()
                
        if LogError is not None and LogAction is not None:
            try:
                con, cur = connect(nameDB('SystemLogs.db'))
                date, timeorg = getdatetime()
                time = timeorg.strftime("%H:%M:%S")
                if lastid(2) is not None:
                    logid = lastid(2) + 1
                else:
                    logid = 1
                query = ("INSERT INTO errorLog VALUES (?, ?, ?, ?, ?, ?, ?, ?);")
                values = (logid, uid, uname, progname, date, time, LogAction, LogError)
                cur.execute(query, values)
                con.commit()
                return True
            except Exception as e:
                print("LOG_ERROR : in function insertlog():->", e)
                return False
            finally:
                con.close()

        if LogException is not None and LogAction is not None:
            try:
                con, cur = connect(nameDB('SystemLogs.db'))
                date, timeorg = getdatetime()
                time = timeorg.strftime("%H:%M:%S")
                if lastid(3) is not None:
                    logid = lastid(3) + 1
                else:
                    logid = 1
                query = ("INSERT INTO exceptionLog VALUES (?, ?, ?, ?, ?, ?, ?, ?);")
                values = (logid, uid, uname, progname, date, time, LogAction, LogException)
                cur.execute(query, values)
                con.commit()
                return True
            except Exception as e:
                print("LOG_ERROR : in function insertlog():->", e)
                return False
            finally:
                con.close()

    except Exception as e:
        print("ERROR : in function insertlog():->", e)
        return False
    
def retrievelogs(option1: str, option2: str, argument: str):
    """
    Retrieves logs from the database based on the given options and arguments.

    Args:
        option1 (str): table name, Acceptable Values are => userLog, errorLog, exceptionLog.
        option2 (str): Column name of the table, Acceptable Values are => LogDate, LogTime, LogAction, LogError, LogException, uid, uname, program.
        argument (str): The value to filter by for the specified field.

    Returns:
        A list of log entries matching the specified criteria, or False if an error occurs.
    """
    validOption2 = ["LogDate", "LogTime", "LogAction", "LogError", "LogException", "uid", "uname", "program", "logid"]
    validOption1 = ["userLog", "errorLog", "exceptionLog"]
    try:
        try: 
            def getLogs():
                con, cur = connect(nameDB('SystemLogs.db'))
                try:
                    if option2 in validOption2:
                        query = (f"SELECT * FROM {option1} WHERE {option2} = ?;")
                        print(query)
                        print(argument)
                        cur.execute(query, (argument,))
                        rows = cur.fetchall()
                        con.close()
                        return rows
                    else:
                        #--Log Start--
                        message = "ERROR in function logfuncs.retrieveLogs()"
                        program = "home app"
                        error = f"Invalid Argument Value = {argument} given for table = {option1} and option = {option2}"
                        insertlog("NA", "NA", program, message, error, None)
                        #---Log end---
                        return False
                except Exception as e:
                    #--Log Start--
                    message = "EXCEPTION in function logfuncs.retrieveLogs()"
                    program = "home app"
                    insertlog("NA", "NA", program, message, None, str(e))
                    #---Log end---
                    con.close()
                    return False
        except Exception as e:
            #--Log Start--
            message = "EXCEPTION in function logfuncs.retrieveLogs()"
            program = "home app"
            insertlog("NA", "NA", program, message, None, str(e))
            #---Log end---
            return False
    
        if option1 in validOption1:
            if option2 in validOption2:
                return getLogs()
            else:
                #--Log Start--
                message = "ERROR in function logfuncs.retrieveUserLogs()"
                program = "home app"
                error = f"Invalid Option Value = {option2} given for table = {option1}"
                insertlog("NA", "NA", program, message, error, None)
                #---Log end---
                return False
        else:
            #--Log Start--
            message = "ERROR in function logfuncs.retrieveUserLogs()"
            program = "home app"
            error = f"Invalid Table Value = {option1} given"
            insertlog("NA", "NA", program, message, error, None)
            #---Log end---
            return False
    except Exception as e:
        #--Log Start--
        message = "EXCEPTION in function logfuncs.retrieveLogs()"
        program = "home app"
        insertlog("NA", "NA", program, message, None, str(e))
        #---Log end---
        return False

    
print("Log Funcs Loaded...")
#Commented code below is for testing purposes

#insertlog('admin', 'admin', 'admin', 'admin')
#insertlog('admin', 'admin', 'admin', 'admin', 'test')
#insertlog('admin', 'admin', 'admin', 'admin', None, 'test')
"""
con, cur = connect(nameDB('SystemLogs.db'))
query = ("SELECT * FROM userLog;")
cur.execute(query)
for i in cur.fetchall():
    print(i)
query = ("SELECT * FROM errorLog;")
cur.execute(query)
for i in cur.fetchall():
    print(i)
query = ("SELECT * FROM exceptionLog;")
cur.execute(query)
for i in cur.fetchall():
    print(i)
"""

# def createUserLogDB():
#     con, cur = connect(nameDB('SystemLogs.db'))
#     query = """CREATE TABLE IF NOT EXISTS userLog(
#             logID INTEGER PRIMARY KEY AUTOINCREMENT,
#             uid TEXT NOT NULL,
#             uname TEXT NOT NULL,
#             progname TEXT NOT NULL,
#             LogDate TEXT NOT NULL,
#             LogTime TEXT NOT NULL,
#             LogAction TEXT NOT NULL
#             );"""
#     cur.execute(query)
#     con.commit()
#     con.close()

# def createErrorLogDB():
#     con, cur = connect(nameDB('SystemLogs.db'))
#     query = """CREATE TABLE IF NOT EXISTS errorLog(
#             logID INTEGER PRIMARY KEY AUTOINCREMENT,
#             uid TEXT NOT NULL,
#             uname TEXT NOT NULL,
#             progname TEXT NOT NULL,
#             LogDate TEXT NOT NULL,
#             LogTime TEXT NOT NULL,
#             LogAction TEXT NOT NULL,
#             LogError TEXT NOT NULL
#             );"""
#     cur.execute(query)
#     con.commit()
#     con.close()

# def createExceptionLogDB():
#     con, cur = connect(nameDB('SystemLogs.db'))
#     query = """CREATE TABLE IF NOT EXISTS exceptionLog(
#             logID INTEGER PRIMARY KEY AUTOINCREMENT,
#             uid TEXT NOT NULL,
#             uname TEXT NOT NULL,
#             progname TEXT NOT NULL,
#             LogDate TEXT NOT NULL,
#             LogTime TEXT NOT NULL,
#             LogAction TEXT NOT NULL,
#             LogException TEXT NOT NULL
#             );"""
#     cur.execute(query)
#     con.commit()
#     con.close()

# createUserLogDB()
# createErrorLogDB()
# createExceptionLogDB()

"""
#To Delete All Logs efficiently
con, cur = connect(nameDB('SystemLogs.db'))

cur.execute('DELETE FROM userLog;')
cur.execute('DELETE FROM errorLog;')
cur.execute('DELETE FROM exceptionLog;')
con.commit()
cur.execute('VACUUM;')
con.commit()
con.close()
"""

#Test Functions Here

print(retrievelogs("errorLog", "uid", "NA"))

con, cur = connect(nameDB('SystemLogs.db'))
query = ("SELECT * FROM exceptionLog;")
cur.execute(query)
for i in cur.fetchall():
    print(i)
