print("Log Funcs Loading...")
from sql3_funcs import connect, nameDB
#home.sql3_funcs

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
    if LogAction is None and LogError is None and LogException is None:
        return False
    elif LogAction is not None and LogError is None and LogException is None:
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
            return False
        finally:
            con.close()
    elif LogError is not None and LogAction is not None:
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
            print("ERROR : in function insertlog():->", e)
            return False
        finally:
            con.close()
    elif LogException is not None and LogAction is not None:
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
            print("ERROR : in function insertlog():->", e)
            return False
        finally:
            con.close()
    else:
        print("NOTE : in function insertlog():-> Option is Invalid")
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
