from . import sql3_funcs

def allPrograms(user:str) -> list:
    if user is "Admin":
        programsList = [['Admin', 'Admin'],
                        ['Mart_Cust', 'Shop'],
                        ['Mart_Manager', 'Shop-Manager'],
                        ['Logistic', 'Mart-Stock']]
    elif user is "Employee-Online":
        programsList = [['Mart_Cust', 'Shop'],
                        ['Mart_Manager', 'Shop-Manager']]
    elif user is "Employee-offline":
        programsList = [['Logistic', 'Mart-Stock']]
    elif user is "Customer":
        programsList = [['Mart_Cust', 'Shop']]
    else:
        programsList = []
    return programsList

def checkAuth(uname, pasw):
    auth, err = sql3_funcs.retrieveUserLogin(uname, pasw)
    if auth:
        return True, err
    else:
        return False, err
    
print("HELPER_FUNC.PY:: Running......")