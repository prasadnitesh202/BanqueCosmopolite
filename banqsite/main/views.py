from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse, JsonResponse
from .models import *

# Create your views here.


def home(request):
    return render(request, 'myapp/home.html')

@login_required(login_url='/login/')
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
                # print(Account.objects.filter(user=username))
                x=Account.objects.filter(user_id__user__username=username)[0].acc_no
                print("Account Number: "+str(x))
                return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request = request,
                    template_name = "myapp/Login.html",
                    context={"form":form})

def logout_request(request):
    logout(request)
    return redirect("main:home")


@csrf_exempt
def webhook(request):

    # build a request object
    req = json.loads(request.body)
    # get action from json
    action = req.get('queryResult').get('action')
    parameters = req.get('queryResult').get('parameters')
    # return a fulfillment message
    parameters = req.get('queryResult').get('parameters')
    if action == 'get_accnum':
        account_type = parameters.get('account-type')
        if account_type == 'Savings':
            fulfillmentText = {'fulfillmentText': 'Your savings account has \
            balanced toppings'}
        else:
            fulfillmentText = {'fulfillmentText': 'Speaking to you from \
            backend'}
    elif action == 'lastlogin':
        fulfillmentText = {'fulfillmentText': 'Last login details to be\n fetched from backend later'}
    elif action == 'expense-dateperiod':
        start_date = parameters.get('date-period').get('startDate')
        end_date = parameters.get('date-period').get('endDate')
        fulfillmentText = {'fulfillmentText': 'You are looking for expenditure\ between'+str(start_date)+' and'+str(end_date)}
    # elif action == 'debitcard-expiry':
    
    return JsonResponse(fulfillmentText, safe=False)