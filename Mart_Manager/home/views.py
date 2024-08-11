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
    auth = request.session.get('auth')
    return render(request, 'home/home.html', context={
        "name": request.session.get('uname'),
        "pages": helper_func.allPrograms(auth),
        "fname": request.session.get('fname'),
        "lname": request.session.get('lname'),
        "email": request.session.get('email'),
        "msg_id": request.session.get('msg_id'),
        "phone": request.session.get('phone'),
        "mname": request.session.get('mname')
    })

def login(request):
    if request.session.get('username'):
        return redirect('homepage')
    elif request.method == 'POST':
        name = request.POST["uname"]
        pasw = request.POST["password"]
        auth, err = helper_func.checkAuth(name, pasw)
        if auth==True:
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

def AdminPage(request):
    return HttpResponse("<h1>Admin</h1>")

def ShopPage(request):
    return HttpResponse("<h1>Shop</h1>")

def ShopManagerPage(request):
    return HttpResponse("<h1>Shop-Manager</h1>")

def ShopStockPage(request):
    return HttpResponse("<h1>Mart-Stock</h1>")