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
    return programsList

def checkAuth(uname, pasw):
    auth, err = sql3_funcs.retrieveUserLogin(uname, pasw)
    if auth:
        return True, err
    else:
        return False, err
    
def setSession(request, name):
    values = sql3_funcs.userDetailsOps(name, 1)
    request.session['uid'] = values[0]
    request.session['uname'] = values[1]
    request.session['auth'] = values[2]
    request.session['fname'] = values[3]
    request.session['mname'] = values[4]
    request.session['lname'] = values[5]
    request.session['email'] = values[6]
    request.session['phone'] = values[7]
    request.session['msg_id'] = values[8]
    request.session['eml_id'] = values[9]
    request.session['last_page_url'] = values[10]

    

print("HELPER_FUNC.PY:: Running......###")

def staticPath():
    current_dir = os.path.join(os.path.abspath(__file__))   
    static_dir = os.path.join(current_dir, '..', '..','static')
    static_actual = (os.path.normpath(os.path.join(static_dir,)))
    return_static = static_actual.replace('\\', '/')
    return return_static


