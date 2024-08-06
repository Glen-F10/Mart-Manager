from . import sql3_funcs

def checkAuth(uname, pasw):
    auth, err = sql3_funcs.retrieveUserLogin(uname, pasw)
    if auth:
        return True, err
    else:
        return False, err