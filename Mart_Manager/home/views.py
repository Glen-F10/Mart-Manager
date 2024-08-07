from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from . import helper_func

# Create your views here.
def index(request):
    if request.session.get('username'):
        return redirect('homepage')
    else:
        return redirect('login')

def home(request):
    return render(request, 'home/home.html', context={
        "name": request.session.get('username')
    })

def login(request):
    if request.session.get('username'):
        return redirect('homepage')
    elif request.method == 'POST':
        name = request.POST["uname"]
        pasw = request.POST["password"]
        auth, err = helper_func.checkAuth(name, pasw)
        if auth==True:
            request.session['username'] = name
            return redirect('homepage')
        else:
            return render(request, "home/login.html", context={
                "value":True,
            })
    else:
        print("running else")
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