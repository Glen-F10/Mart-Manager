from django.shortcuts import render
from . import helper_func

# Create your views here.
def home(request):
    return render(request, 'home/home.html')

def login(request):
    if request.method == 'POST':
        print("running if")
        name = request.POST["uname"]
        pasw = request.POST["password"]
        auth = helper_func.checkAuth(name, pasw)
        print(auth)
        if auth==True:
            return render(request, "home/home.html")
        else:
            return render(request, "home/login.html", context={
                "value":True,
            })
    else:
        print("running else")
        return render(request, "home/login.html", context={
                "value":False,
            })