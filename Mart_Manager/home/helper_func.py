from . import sql3_funcs

def allPrograms(user:str) -> list:
    if user == "Admin":
        programsList = [['Admin', 'Admin'],
                        ['Mart_Cust', 'Shop'],
                        ['Mart_Manager', 'Shop-Manager'],
                        ['Logistic', 'Mart-Stock']]
    elif user == "Employee-Online":
        programsList = [['Mart_Cust', 'Shop'],
                        ['Mart_Manager', 'Shop-Manager']]
    elif user == "Employee-offline":
        programsList = [['Logistic', 'Mart-Stock']]
    elif user == "Customer":
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
    
def setSession(request, name):
    values = sql3_funcs.userDetailsOps(name, 1)
    request.session['uname'] = values[0]
    request.session['auth'] = values[1]
    request.session['fname'] = values[2]
    request.session['mname'] = values[3]
    request.session['lname'] = values[4]
    request.session['email'] = values[5]
    request.session['phone'] = values[6]
    request.session['msg_id'] = values[7] 
    request.session['screen'] = values[8]
    
print("HELPER_FUNC.PY:: Running......###")