from home.sql3_funcs import connect, nameDB

def createUserLogDB():
    con, cur = connect(nameDB('SystemLogs.db'))
    query = """CREATE TABLE IF NOT EXISTS userLog(
            logID INTEGER PRIMARY KEY AUTOINCREMENT,
            uid TEXT NOT NULL,
            uname TEXT NOT NULL,
            progname TEXT NOT NULL,
            LogDate TEXT NOT NULL,
            LogTime TEXT NOT NULL,
            LogAction TEXT NOT NULL
            );"""
    cur.execute(query)
    con.commit()
    con.close()

def createErrorLogDB():
    con, cur = connect(nameDB('SystemLogs.db'))
    query = """CREATE TABLE IF NOT EXISTS errorLog(
            logID INTEGER PRIMARY KEY AUTOINCREMENT,
            uid TEXT NOT NULL,
            uname TEXT NOT NULL,
            progname TEXT NOT NULL,
            LogDate TEXT NOT NULL,
            LogTime TEXT NOT NULL,
            LogAction TEXT NOT NULL,
            LogError TEXT NOT NULL
            );"""
    cur.execute(query)
    con.commit()
    con.close()

def createExceptionLogDB():
    con, cur = connect(nameDB('SystemLogs.db'))
    query = """CREATE TABLE IF NOT EXISTS exceptionLog(
            logID INTEGER PRIMARY KEY AUTOINCREMENT,
            uid TEXT NOT NULL,
            uname TEXT NOT NULL,
            progname TEXT NOT NULL,
            LogDate TEXT NOT NULL,
            LogTime TEXT NOT NULL,
            LogAction TEXT NOT NULL,
            LogException TEXT NOT NULL
            );"""
    cur.execute(query)
    con.commit()
    con.close()