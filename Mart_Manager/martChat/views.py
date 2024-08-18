from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    if request.session.get('uname') is not None:
        return render(request, "martChat/index.html")
    else:
        return redirect('login')