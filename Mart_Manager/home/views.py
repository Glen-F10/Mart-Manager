from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from . import helper_func
from . import logfuncs

# Create your views here.
def index(request):
    if request.session.get('uname') is not None:
        return redirect('homepage')
    else:
        return redirect('login')

def home(request):
    try:
        if request.session.get('uname') is None:
            return redirect('sessionExpired')
        else:
            auth = request.session.get('auth')
            request.session['last_page_url'] = 'homepage'
            return render(request, 'home/home.html', context={
                "name": request.session.get('uname'),
                "user": helper_func.allPrograms(auth),
            })
    except Exception as e:
        #---Log start---
        message = "EXCEPTION OCCURED in function home.home()"
        program = "home app"
        logfuncs.insertlog(request.session.get('uid'), request.session.get('uname'), program, message, None, e)
        return redirect('exception')
        #---Log end---

def login(request):
    try:
        if request.session.get('uname'):
            return redirect('homepage')
        elif request.method == 'POST':
            name = request.POST["uname"]
            pasw = request.POST["password"]
            auth, err = helper_func.checkAuth(name, pasw)
            if auth:
                helper_func.setSession(request, name)
                #---Log start---
                message = "SUCCESSFULLY LOGGED IN in function home.login()"
                program = "home app/login page"
                logfuncs.insertlog(request.session.get('uid'), request.session.get('uname'), program, message, None, None)
                #---Log end---
                return redirect('homepage')
            else:
                #---Log start---
                message = "ERROR OCCURED in function home.login()"
                program = "home app/login page"
                error = f"Bad Credentials username : {name}, password : {pasw}"
                logfuncs.insertlog("NA", "NA", program, message, error, None)
                #---Log end---
                return render(request, "home/login.html", context={
                    "formtype":"errorlogin",
                    "error":"Invalid Username or Password",
                    })
        elif request.session.get('uname') is None:
            return render(request, "home/login.html", context={
                "formtype":"login",
                })
        else:
            #---Log start---
            message = "ERROR OCCURED in function home.login()"
            program = "home app/login page"
            error = "Acessed URL with invalid Method"
            logfuncs.insertlog("NA", "NA", program, message, error, None)
            #---Log end---
            return redirect('blocked')
            
    except Exception as e:
        #---Log start---
        message = "EXCEPTION OCCURED in function home.login()"
        program = "home app/login page"
        logfuncs.insertlog(request.session.get('uid'), request.session.get('uname'), program, message, None, e)
        #---Log end---
        return redirect('exception')
    
def logout(request):
    try:
        if request.session.get('uname') is None:
            return redirect('sessionExpired')
        else:
            uid = request.session.get('uid')
            uname = request.session.get('uname')
            auth.logout(request)
            messageHead = 'You have been Logged out'
            messageBody = 'Please login again to use the application, If error please contact your administrator'
            #---Log start---
            message = "SUCCESSFULLY LOGGED OUT in function home.logout()"
            program = "home app/logout page"
            logfuncs.insertlog(uid, uname, program, message, None, None)
            #---Log end--- 
            return render(request, "home/message_layout.html", context={
                'messageColor': 'warning',
                'messageHead':messageHead,
                'messageBody':messageBody,
                'goback_link': 'login',
                'goback_value': 'Login Again',
                'staticPath': helper_func.staticPath(),
                'name': request.session.get('uname'),
            })
    except Exception as e:
        print("ERROR OCCURED in function logout() in views.py file :->", e)
        #---Log start---
        message = "EXCEPTION OCCURED in function home.logout()"
        program = "home app/logout page"
        logfuncs.insertlog(request.session.get('uid'), request.session.get('uname'), program, message, None, e)
        #---Log end---
        return redirect('exception')

def getSessionInfo(request):#for session data delete at publish
    session_data = request.session.items()
    return HttpResponse(f"<h1>{session_data}</h1>")

def blocking(request):
    try:
        access = request.session.get('auth')
        messageHead = 'Warning : Access Denied'
        messageBody = f'You are not authorized to access this page, your authorization is of a {access}. This action is reproted by default please contact your administrator if error'
        return render(request, "home/message_layout.html", context={
            'messageColor': 'danger',
            'messageHead':messageHead,
            'messageBody':messageBody,
            'goback_link': 'login',
            'goback_value': 'Login Again',
            'name': request.session.get('uname'),
        })
    except Exception as e:
        #---Log start---
        message = "EXCEPTION OCCURED in function home.blocking()"
        program = "home app/blocking page"
        logfuncs.insertlog("NA", "NA", program, message, None, e)
        #---Log end---
        return redirect('exception')

def exception(request):
    try:
        messageHead = 'Oops!! Something went wrong'
        messageBody = 'Please try again later, Note: This error is reproted by default please contact your administrator if error persists, Thank you' 
        return render(request, "home/message_layout.html", context={
            'messageColor': 'light',
            'messageHead':messageHead,
            'messageBody':messageBody,
            'goback_link': request.session.get('last_page_url'),
            'goback_value': 'Go Back',
            'staticPath': helper_func.staticPath(),
            'name': request.session.get('uname'),
        })
    except Exception as e:
        #---Log start---
        message = "EXCEPTION OCCURED in function home.exception()"
        program = "home app/exception page"
        logfuncs.insertlog("NA", "NA", program, message, None, e)
        #---Log end---
        return redirect("404")
    
def pageNotFound(request):
    #---Log start---
    message = "ERROR OCCURED in function home.pageNotFound()"
    program = "home app/404 page"
    error = "Invalid URL"
    logfuncs.insertlog("NA", "NA", program, message, error, None)
    #---Log end---
    messageHead = 'Oops!! Page Not Found ERROR: 404'
    messageBody = 'Please check the link given, Note: This error is reproted by default please contact your administrator if error persists, Thank you' 
    return render(request, "home/message_layout.html", context={
        'messageColor': 'warning',
        'messageHead':messageHead,
        'messageBody':messageBody,
        'goback_link': request.session.get('last_page_url'),
        'goback_value': 'Go Back',
        'staticPath': helper_func.staticPath(),
        'name': request.session.get('uname'),
    })

def sessionExpired(request):
    #---Log start---
    message = "ERROR OCCURED in function home.sessionExpired()"
    program = "home app/sessionExpired page"
    error = "Session Expired"
    logfuncs.insertlog("NA", "NA", program, message, error, None)
    #---Log end---
    messageHead = 'Your Session has expired!'
    messageBody = 'Please login again, Note: This error is reproted by default please contact your administrator if error persists, Thank you' 
    return render(request, "home/message_layout.html", context={
        'messageColor': 'warning',
        'messageHead':messageHead,
        'messageBody':messageBody,
        'goback_link': 'login',
        'goback_value': 'Login Again',
        'staticPath': helper_func.staticPath(),
        'name': request.session.get('uname'),
    })

def chatRedirect(request):
    try:
        if request.session.get('uname') is not None:
            return redirect('chat-index')  #redirecting to mart chat app
        else:
            return redirect('sessionExpired')
    except Exception as e:
        #---Log start---
        message = "EXCEPTION OCCURED in function home.chatRedirect()"
        program = "home app/chatRedirect page"
        logfuncs.insertlog("NA", "NA", program, message, None, e)
        #---Log end---
        return redirect('exception')