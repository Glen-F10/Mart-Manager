from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from . import helper_func

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
        print("EXCEPTION OCCURED in function home():->",e)
        return redirect('exception')

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
                return redirect('homepage')
            else:
                return render(request, "home/login.html", context={
                    "formtype":"errorlogin",
                    "error":"Invalid Username or Password",
                    })
        elif request.session.get('uname') is None:
            return render(request, "home/login.html", context={
                "formtype":"login",
                })
        else:
            return redirect('blocked')
            
    except Exception as e:
        print("EXCEPTION OCCURED in function login():->",e)
        return redirect('exception')
    
def logout(request):
    try:
        if request.session.get('uname') is None:
            return redirect('sessionExpired')
        else:
            auth.logout(request)
            messageHead = 'You have been Logged out'
            messageBody = 'Please login again to use the application, If error please contact your administrator' 
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
        return redirect('exception')

def getSessionInfo(request):#for session data delete at publish
    session_data = request.session.items()
    return HttpResponse(f"<h1>{session_data}</h1>")

def blocking(request):
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

def exception(request):
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

def pageNotFound(request):
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
    if request.session.get('uname') is not None:
        return redirect('chat-index')  #redirecting to mart chat app