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
from datetime import datetime, timedelta
from django.utils import formats
from .helperfunctions import *

# Create your views here.
x=0

account ='Account'
def home(request):
    return render(request, 'myapp/home.html')

@login_required(login_url='/login/')
def chatbot(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    accounts = Account.objects.filter(user_id__user__username=username)
    return render(request, 'myapp/Chatbot.html', {'accounts': accounts})


# def login(request):
#     return render(request, 'myapp/login.html')

@login_required(login_url='/login/')
def account(request):
    acc=Account.objects.filter(user_id__user__username=uname)
    no_acc=acc.count()
    print(no_acc)
    total_balance=0
    accs=[]
    total_transactions=0
    for i in acc:
        total_balance=total_balance+i.acc_balance
        accs.append(i.acc_no)
    print(total_balance)
    print(accs)
    for i in range(no_acc):
        t=Transaction.objects.filter(paid_from__acc_no=accs[i]).count()
        total_transactions=total_transactions+t
        print(total_transactions)
    fd=0
    for i in range(no_acc):
        c=Account.objects.filter(acc_no=accs[i]).filter(acc_type='FD').count()
        fd=fd+c
        print(fd)
    emi_pending=0
    for i in range(no_acc):
        c=Loan.objects.filter(acc_no__acc_no=accs[i]).count()
        emi_pending=emi_pending+c
    print("emipending:"+str(emi_pending))

        

    






        


    return render(request, 'myapp/account.html')

def atmf(request):
    return render(request, 'myapp/ATM.html')

def monket(request):
    return render(request, 'myapp/Money_market.html')

def checkin(request):
    return render(request, 'myapp/Checking.html')

@login_required(login_url='/login/')
def payment(request):
    return render(request, 'myapp/Payment.html')


def savings(request):
    return render(request, 'myapp/Savings.html')

def mission(request):
    return render(request, 'myapp/Mission.html')

def team(request):
    return render(request, 'myapp/Our_Team.html')

def history(request):
    return render(request, 'myapp/History.html')

def prepaid(request):
    return render(request, 'myapp/Prepaid.html')

@login_required(login_url='/login/')
def transaction(request):
    return render(request, 'myapp/Transaction.html')

@login_required(login_url='/login/')
def cards(request):
    return render(request, 'myapp/Card.html')


def hsave(request):
    return render(request, 'myapp/Health_Savings.html')

def cash_mgmt(request):
    return render(request, 'myapp/Cash_Management.html')

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
                global uname
                uname=User.objects.get(username=username)
                global x
                x=Account.objects.filter(user_id__user__username=username)[0].acc_no
                print("Account Number: "+str(x))
                return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request = request,
                    template_name = "myapp/Login.html",
                    context={"form":form})

def logout_request(request):
    global account
    account = 'Account'
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
        if(account=='Account'):
            text='Please select account number from dropdown to the left'
        else:

            start_date = parameters.get('date-period').get('startDate')
            end_date = parameters.get('date-period').get('endDate')
            d1 = datefield_parse(start_date)
            d2 = datefield_parse(end_date)
            sender=Transaction.objects.filter(paid_from__acc_no=account).filter(date_time__date__range=[d1, d2])
            print(sender)
            text=''
            if sender.count()==0:
                print('0')
                text='No transactions done between '+str(d1)+' and '+str(d2)
            else:
                c=0
                sum=0
                for i in sender:
                    text=text+str(c)+'.): '+str(i.amount)+' paid to '+str(i.paid_to)+'   '
                    c=c+1
                    print(text)
                    sum=sum+i.amount
                text=text+', So total amount debited= '+str(sum)
        fulfillmentText={'fulfillmentText':text}
       



        # fulfillmentText = {'fulfillmentText': 'You are looking for expenditure\ between'+str(start_date)+' and'+str(end_date)}
    elif action == 'debitcard-expiry':
        if(account=='Account'):
            fulfillmentText={'fulfillmentText':'Please select account number from dropdown to the left'}
        else:

            print(x)
            a=Card.objects.filter(acc_no__acc_no=account).filter(card_type='D')
            print(a)
            c=a.count()
            if(c==0):
                fulfillmentText={'fulfillmentText':'You dont have any debit card linked to your account,You can choose another account from dropdown to the left and try again'}
            else:
                fulfillmentText={'fulfillmentText':'Your debit card expires on '+str(a[0].valid_thru)}

    elif action == 'creditcard-expiry':
        print(x)
        if(account=='Account'):
            fulfillmentText={'fulfillmentText':'Please select account number from dropdown to the left'}
        else:

            a=Card.objects.filter(acc_no__acc_no=account).filter(card_type='C')
            print(a)
            c=a.count()
            if(c==0):
                fulfillmentText={'fulfillmentText':'You dont have any credit card linked to your account.You can change the acount number from dropdown to the left and try again'}
            else:
                fulfillmentText={'fulfillmentText':'Your credit card expires on '+str(a[0].valid_thru)}
        
    elif action == 'expenditure-date':
        if(account=='Account'):
            text='Please select account number from dropdown to the left'
        else:

            start_date=parameters.get('date')
            print(start_date)
            d1 = datefield_parse(start_date)
            d2=d1+timedelta(days=1)
            print(d1)
            print(d2)
            sender=Transaction.objects.filter(paid_from__acc_no=x).filter(date_time__date__range=[d1, d1])
            print(sender)
            text=''
            if sender.count()==0:
                print('0')
                text='No transactions done on '+str(d1)+' You can change the account number from dropdown to the left and try again'
            else:
                c=0
                sum=0
                for i in sender:
                    text=text+str(c)+'.): '+str(i.amount)+' paid to '+str(i.paid_to)+'   '
                    c=c+1
                    print(text)
                    sum=sum+i.amount
                text=text+', So total amount debited= '+str(sum)
        fulfillmentText={'fulfillmentText':text}
        
    elif action == 'emi_status':
        print('accnt nus ishefjndf'+str(account))
        if account=='Account':
            text='Please select account number from dropdown to the left'
            print(text)
        else:
            # print('yo accnt nhmber is'+str(account))
            a=Loan.objects.filter(acc_no__acc_no=account)
            text=''
            print("account number is"+str(account))
            if(a.count()==0):
                text=text+' No emi due in this account.You can change the account number from dropdown to the left and try again.'
            else:
                text=text+'You have a total of '+str(a.count())+' loans'
                c=1
                for i in a:
                    ip=i.installments_paid
                    amount=i.amount
                    amount_paid=i.amount_paid
                    amt_due=amount-amount_paid
                    il=i.num_installments-ip
                    emi=(amt_due//il)+((il*i.interest)//100)
                    text=text+str(c)+') emi-due:  '+str(emi)+'  '
                    c=c+1
        fulfillmentText={'fulfillmentText':text}

    elif action=='transaction-creditcard-period':

        if account=='Account':
            text='Please select account number from dropdown to the left'
        else:

            start_date = parameters.get('date-period').get('startDate')
            end_date = parameters.get('date-period').get('endDate')
            d1 = datefield_parse(start_date)
            d2 = datefield_parse(end_date)
            sender=Transaction.objects.filter(paid_from__acc_no=account).filter(txn_type='A').filter(date_time__date__range=[d1, d2])
            print(sender)
            text=''
            if(sender.count()==0):
                text=text+' no transactions from credit card during this time.You can change the account number from dropdown to the left and try again'
            else:
                c=0
                sum=0
                for i in sender:
                    text=text+str(c)+'.): '+str(i.amount)+' paid to '+str(i.paid_to)+'   '
                    c=c+1
                    print(text)
                    sum=sum+i.amount
                text=text+', So total amount debited from credit card= '+str(sum)
        fulfillmentText={'fulfillmentText':text}
        
    elif action=='transaction-debitcard-period':
        if account=='Account':
            text='Please select account number from dropdown to the left'
        else:

            start_date = parameters.get('date-period').get('startDate')
            end_date = parameters.get('date-period').get('endDate')
            d1 = datefield_parse(start_date)
            d2 = datefield_parse(end_date)
            sender=Transaction.objects.filter(paid_from__acc_no=account).filter(txn_type='B').filter(date_time__date__range=[d1, d2])
            print(sender)
            if(sender.count()==0):
                text='No transaction done from this debit card during this time.You can change the account number from the dropdown to the left and try again'
            else:

                for i in sender:
                    text=text+str(c)+'.): '+str(i.amount)+' paid to '+str(i.paid_to)+'   '
                    c=c+1
                    print(text)
                    sum=sum+i.amount
                text=text+', So total amount debited from debit card= '+str(sum)
        fulfillmentText={'fulfillmentText':text}
    elif action=='fd-general':
        if account=='Account':
            text='Please select account number from dropdown to the left'
        else:
            a=Account.objects.filter(acc_no=account).filter(acc_type__acc_type='FD')
            print(a)
            if(a.count()==0):
                text='This is not your fixed deposit account.If you have one in our bank please select it from the dropdown to the left'
            else:
                for i in a:

                    text='Amount is fixed deposit is: '+str(i.acc_balance)+' and it is maturing on '+str(i.end_date)
        fulfillmentText={'fulfillmentText':text}
    
    elif action=='acc-balance':
        if account=='Account':
            text='Please select account number from dropdown to the left'
        else:
            a=Account.objects.filter(acc_no=account)
            print(a)
            for i in a:
                text='Your account balance is : '+str(i.acc_balance)
        fulfillmentText={'fulfillmentText':text}
    
    elif action=='fd-accno':
        acc=Account.objects.filter(user_id__user__username=uname).filter(acc_type__acc_type='FD')
        text=''
        if acc.count()==0:
            text='You dont have any fixed deposit linked to any accounts. Please visit our nearest branch to open a fixed deposit accout '
        else:
            text=text+'You have a total of '+str(acc.count())+' fixed deposit linked to your account. Their account numbers are:  '
            
            for i in acc:
                text=text+str(i.acc_no)+'and '
        fulfillmentText={'fulfillmentText':text}
    
    elif action=='acc-details':
        savings=Account.objects.filter(user_id__user__username=uname).filter(acc_type__acc_type='SA')
        current=Account.objects.filter(user_id__user__username=uname).filter(acc_type__acc_type='CA')
        recurring=Account.objects.filter(user_id__user__username=uname).filter(acc_type__acc_type='RD')
        fd=Account.objects.filter(user_id__user__username=uname).filter(acc_type__acc_type='FD')
        zerobal=Account.objects.filter(user_id__user__username=uname).filter(acc_type__acc_type='ZB')
        text=''
        totalacc=savings.count()+current.count()+recurring.count()+fd.count()+zerobal.count()
        text=text+ " You have a total of "+str(totalacc)+" accounts linked to us  "
        if savings.count()!=0:
            text=text+ ' You have '+str(savings.count())+ ' savings account and their account numbers are  '
            for i in savings:
                text=text+'  '+str(i.acc_no)
        if current.count()!=0:
            text=text+' You have '+str(current.count())+ ' current accounts  and their account numbers are  '
            for i in current:
                text=text+'  '+str(i.acc_no)
        if recurring.count()!=0:
            text=text+' You have '+str(recurring.count())+ ' recurring accounts and their account numbers are '
            for i in recurring:
                text=text+'  '+str(i.acc_no)+'   '
        if fd.count()!=0:
            text=text+'  You have '+str(fd.count())+ ' fixed deposits  and their account numbers are '
            for i in fd:
                text=text+'  '+str(i.acc_no)
        if zerobal.count()!=0:
            text=text+'  You have '+str(zerobal.count())+ ' zero balance accounts  and their account numbers are  '
            for i in savings:
                text=text+'  '+str(i.acc_no)

        fulfillmentText={'fulfillmentText':text}

    elif action=='acc-type':
        text=' '
        if account=='Account':
            text='Please select account number from dropdown to the left'
        else:
            a=Account.objects.filter(acc_no=account)
            for i in a:
                atype=str(i.acc_type)    
            print(atype)
            if atype=='SA':
                text=text+'This is a savings account'
            elif atype=='RD':
                text=text+'This is a recurring deposit account'
            elif atype=='FD':
                text=text+'This is a fixed deposit account'
            elif atype=='CA':
                text=text+'This is a current account'
            elif atype=='ZB':
                text=text+'This is a zerobalance account'
            
        fulfillmentText={'fulfillmentText':text}

        

        



    
        
                

            
        
    
        



    

        

    

            







        
        
    
    return JsonResponse(fulfillmentText, safe=False)

@csrf_exempt
def chatbot_ajax(request):
    acc = request.POST.get('keyname', None)
    # build a request object
    global account
    account = acc
    print(account)
    data ={}
    if(account):
        data['is_success'] = 'Account changed'
    return JsonResponse(data)