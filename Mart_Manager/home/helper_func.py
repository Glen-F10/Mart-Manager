print("Helper Funcs Loading...")
from . import sql3_funcs
from . import logfuncs
import os

def allPrograms(user:str) -> list:
    """
    Retrurn Pattern is a list and elements are.

    [access, adminpage, shop, Inventory, site-Manager]
    """
    try:
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
    except Exception as e:
        #---Log start---
        message = "ERROR: in function helper_func.allPrograms()"
        program = "home app"
        error = str(e)
        logfuncs.insertlog("NA", "NA", program, message, error, None)
        #---Log end---

def checkAuth(uname, pasw):
    auth = sql3_funcs.retrieveUserLogin(uname, pasw)
    if auth:
        #---Log start---
        message = "SUCCESSFULLY LOGGED IN in function helper_func.checkAuth()"
        program = "home app"
        logfuncs.insertlog("NA", uname, program, message, None, None)
        #---Log end---
        return True
    else:
        #---Log start---
        message = "ERROR: in function helper_func.checkAuth()"
        program = "home app"
        error = f"Bad Credentials username : {uname}, password : {pasw}"
        logfuncs.insertlog("NA", "NA", program, message, error, None)
        return False
    
def setSession(request, name):
    try:
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
        return True
    except Exception as e:
        #---Log start---
        message = "ERROR: in function helper_func.setSession()"
        program = "home app"
        error = str(e)
        logfuncs.insertlog("NA", "NA", program, message, error, None)
        #---Log end---
        return False

    

print("Helper Funcs Loaded")

"""
def staticPath():
    current_dir = os.path.join(os.path.abspath(__file__))   
    static_dir = os.path.join(current_dir, '..', '..','static')
    static_actual = (os.path.normpath(os.path.join(static_dir,)))
    return_static = static_actual.replace('\\', '/')
    return return_static
"""


