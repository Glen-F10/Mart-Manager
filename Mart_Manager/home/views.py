from django.shortcuts import render
from django.http import HttpResponse
from . import helper_func

# Create your views here.
def home(request):
    return render(request, 'home/home.html')

def login(request):
    if request.method == 'POST':
        name = request.POST["uname"]
        pasw = request.POST["password"]
        auth, err = helper_func.checkAuth(name, pasw)
        if auth==True:
            if request.session.get('username') == name:
                print("getting old session")
                sname = request.session.get('username')
            else:
                print("creating new session")
                request.session['username'] = name
                sname = request.session.get('username')
            return render(request, "home/home.html", context={
                "name":sname,
            })
        else:
            return render(request, "home/login.html", context={
                "value":True,
            })
    else:
        print("running else")
        return render(request, "home/login.html", context={
                "value":False,
            })

def getSessionInfo(request):#for session data delete at publish
    session_data = request.session.items()
    return HttpResponse(f"<h1>{session_data}</h1>")  