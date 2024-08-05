from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home/home.html')

def login(request):
    if request.method == 'POST':
        name = request.POST["uname"]
        pasw = request.POST["password"]
        
    return render(request, "home/login.html")