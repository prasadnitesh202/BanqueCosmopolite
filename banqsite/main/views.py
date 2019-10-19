from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def home(request):
    return render(request, 'myapp/home.html')


def chatbot(request):
    return render(request, 'myapp/Chatbot.html')


def login(request):
	return render(request, 'myapp/login.html')