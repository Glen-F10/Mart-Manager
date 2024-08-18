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
    auth = request.session.get('auth')
    return render(request, 'home/test.html', context={
        "name": request.session.get('uname'),
        "user": helper_func.allPrograms(auth),
        "staticPath": helper_func.staticPath(),
    })

def login(request):
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
                "value":True,
            })
    else:
        return render(request, "home/login.html", context={
                "value":False,
            })
    
def logout(request):
    try:
        auth.logout(request)
        message1 = "Logout Successful"
        return render(request, "home/logout.html", context={
            'Message':message1
        })
    except Exception as e:
        message2 = "Logout Unsuccessful"
        print("ERROR OCCURED in function logout() in views.py file :->", e)
        return render(request, "home/logout.html", context={
            "Message":message2
        })

def getSessionInfo(request):#for session data delete at publish
    session_data = request.session.items()
    return HttpResponse(f"<h1>{session_data}</h1>")

def chatRedirect(request):
    if request.session.get('uname') is not None:
        return redirect('chat-index')  #redirecting to mart chat app

def blocking(request):
    access = request.session.get('auth')
    messageHead = 'Warning : Access Denied'
    messageBody = f'You are not authorized to access this page, your authorization is of a {access}. This action is reproted by default please contact your administrator if error'
    return render(request, "home/message_layout.html", context={
        'messageColor': 'danger',
        'messageHead':messageHead,
        'messageBody':messageBody,
        'staticPath': helper_func.staticPath(),
        'name': request.session.get('uname'),
    })

def exception(request):
    messageHead = 'Oops!! Something went wrong'
    messageBody = 'Please try again later, Note: This error is reproted by default please contact your administrator if error persists, Thank you' 
    return render(request, "home/message_layout.html", context={
        'messageColor': 'light',
        'messageHead':messageHead,
        'messageBody':messageBody,
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
        'staticPath': helper_func.staticPath(),
        'name': request.session.get('uname'),
    })