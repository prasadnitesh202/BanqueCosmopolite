from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    return render(request, 'myapp/home.html')


def chatbot(request):
    return render(request, 'myapp/Chatbot.html')


# def login(request):
#     return render(request, 'myapp/login.html')

@login_required(login_url='/login/')
def account(request):
    return render(request, 'myapp/account.html')


def login_req(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                print("Hi "+User.objects.get(username=username).first_name)
                return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request = request,
                    template_name = "myapp/Login.html",
                    context={"form":form})

def logout_request(request):
    logout(request)
    return redirect("main:home")