from . import sql3_funcs
import os

def allPrograms(user:str) -> list:
    """
    Retrurn Pattern is a list and elements are.

    [access, adminpage, shop, Inventory, site-Manager]
    """
    if user == "Admin":
        programsList = ['Admin', '', '', '', '']
    elif user == "Employee-Online":
        programsList = ['Employee-Site', 'd-none', '', 'd-none', '']
    elif user == "Employee-offline":
        programsList = ['Employee-Logistics', 'd-none', 'd-none', '', 'd-none']
    elif user == "Customer":
        programsList = ['Customer', 'd-none', '', 'd-none', 'd-none']
    else:
        programsList = []
    print(programsList)
    return programsList

def checkAuth(uname, pasw):
    auth, err = sql3_funcs.retrieveUserLogin(uname, pasw)
    if auth:
        return True, err
    else:
        return False, err
    
def setSession(request, name):
    print("Setting Session")
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

def staticPath():
    current_dir = os.path.join(os.path.abspath(__file__))   
    static_dir = os.path.join(current_dir, '..', '..','static')
    static_actual = (os.path.normpath(os.path.join(static_dir,)))
    return_static = static_actual.replace('\\', '/')
    return return_static

