from django.shortcuts import render, redirect
from django.http import HttpResponse

from authentication.auth_decorators import check_authentication
from authentication.models import Users
from . models import *

# Create your views here.

# Sending in percentage
PrimiumUserSendingChargePercentage=3
NonPrimiumUserSendingChargePercentage=5

# Sending in percentage
PrimiumUserRecevingChargePercentage=1
NonPrimiumUserRecevingChargePercentage=3



def getTransactionCharges(user,action):
    '''Action values
        1 --> Receving
        -1 --> Sending
    '''
    if user.user_type=='premium':
        if action==1:
            return PrimiumUserRecevingChargePercentage # return 1
        elif action == -1:
            return PrimiumUserSendingChargePercentage #return 3
    elif user.user_type=='non-premium':
        if action==1:
            return NonPrimiumUserRecevingChargePercentage   # return 3
        elif action == -1:
            return NonPrimiumUserSendingChargePercentage #return 5

def getChargableAmount(user,amount,action):
    rate=getTransactionCharges(user,action)
    return ((float(rate)/100)*float(amount))


def isUserHasEnoughBalance(user, amount,charges,action):
    balance=float(Balance.objects.filter(user=user).values('balance')[0]['balance'])
    print('user balance',balance)
    # chargable_Amount=charges
    print(type(user),type(amount),type(charges))
    if ( action==1 and (charges <= balance)):   #if user is receiver
        return True
    elif ( action==-1 and (float(amount)+charges <=balance )):  #if user is sender
        return True
    else:
        return False

def updateBalanceAndTransactions(user,amount,charges,action,remark):
    ''''
    action=1 -- > receving
    action=-1 -- > sending, 
    '''
    balance_obj=Balance.objects.filter(user=user).get()
    if action==1:
        balance_obj.balance=round((balance_obj.balance+float(amount))-charges, 2)
        transaction_obj=Transactions(amount=amount,user=user,transfer_type='credit',balance=balance_obj.balance,remark=remark)
        return True, balance_obj,transaction_obj
    elif action==-1:
        balance_obj.balance=round((balance_obj.balance-(float(amount)+charges)),2)
        transaction_obj=Transactions(amount=amount,user=user,transfer_type='debit',balance=balance_obj.balance,remark=remark)
        return True, balance_obj,transaction_obj

# ===========================   view functions =================================

def test(request):
    return render(request,'base2.html')

def getLoggedUserData(request):
    data={}
    try:
        # useremail=request.session['user_logged']
        # data.update(Users.objects.filter(email__iexact=useremail).values('email')[0])
        data.update({'isUserAuthenticated':True})
        return data
    except:
        return {}

# @check_authentication
def dashboard(request ,**kwargs):
    data={}
    # data.update(getLoggedUserData(request))
    data.update({'title':'Home'})
    # return render(request, 'base2.html')
    return render(request, 'dashboard.html')

@check_authentication
def wallet(request):
    balance=Balance.objects.filter(user_id=request.session['ssk_logged_user_id']).values('balance')[0]['balance']
    transactions=Transactions.objects.filter(user_id=request.session['ssk_logged_user_id']).all().order_by('-date')
    data={'title':'Wallet','transactions':transactions,'balance':balance}
    return render(request, 'wallet.html',data)

@check_authentication
def sendMoney(request):
    users=Users.objects.exclude(id=request.session['ssk_logged_user_id']).values('id','fullname','email').order_by('fullname')
    data={'title':'Send Money'}
    data.update({'users':users})

    if request.method == 'GET':
        return render(request, 'send_money.html', data)
    
    if request.method == 'POST':
        temp_data=request.POST.dict()

        amount=temp_data['amount']
        receiving_user_obj=Users.objects.filter(id=temp_data['userid']).get()
        sending_user_obj=Users.objects.filter(id=request.session['ssk_logged_user_id']).get()
        
        sending_charge=float(getChargableAmount(sending_user_obj,amount,-1))
        receiving_charge=float(getChargableAmount(receiving_user_obj,amount,1))
        
        if not isUserHasEnoughBalance(sending_user_obj,amount,sending_charge,-1):
            data.update({'status':False,'message':'You dont have enough balance to send amount'})
            return render(request, 'send_money.html', data)
        if not isUserHasEnoughBalance(receiving_user_obj,amount,receiving_charge, 1):
            data.update({'status':False,'message':'Receiver not have enough balance to receive amount'})
            return render(request, 'send_money.html', data)
        
        try:
            rec=updateBalanceAndTransactions(receiving_user_obj,amount,receiving_charge,1,temp_data['remark'])
            sen=updateBalanceAndTransactions(sending_user_obj,amount,sending_charge,-1,temp_data['remark'])
            if rec[0] and sen[0]:
                rec[1].save()
                sen[1].save()
                rec[2].save()
                sen[2].save()
                data.update({'status':True,'message':'Amount sent sucessfuly'})
                return render(request, 'send_money.html', data)
            else:
                data.update({'status':False,'message':'Sorry!, we are unable to process the request'})
                return render(request, 'send_money.html', data)
        except Exception as e:
            data.update({'status':False,'message':f'Sorry!, we are unable to process the request,{str(e)}'})
            return render(request, 'send_money.html', data)
            
        
@check_authentication
def reqMoney(request):
    users=Users.objects.exclude(id=request.session['ssk_logged_user_id']).values('id','fullname','email').order_by('fullname')
    data={'title':'Request money','users':users}
    if request.method == 'GET':
        return render(request, 'req_money.html', data)

    if request.method == 'POST':
        temp_data=request.POST.dict()
        
        amount=temp_data['amount']
        
        requested_to_user_obj=Users.objects.filter(id=temp_data['userid']).get()
        requested_by_user_obj=Users.objects.filter(id=request.session['ssk_logged_user_id']).get()
        requests_obj=Requests(amount=round(float(amount),2),requested_by=requested_by_user_obj,requested_to=requested_to_user_obj,
                                status=0, remark=temp_data['remark'])
        requests_obj.save()
        data.update({'status':True,'message':'Request placed'})
        return render(request, 'req_money.html', data)


@check_authentication
def reqReceived(request):
    requests=Requests.objects.filter(requested_to=request.session['ssk_logged_user_id']).all().order_by('status')
    # users=Users.objects.exclude(id=request.session['ssk_logged_user_id']).values('id','fullname','email').order_by('fullname')
    data={'title':'Requests Received','requests':requests}
    if request.method == 'GET':
        return render(request, 'req_received.html', data)
    if request.method =='POST':
        return render(request, 'req_received.html', data)

# @check_authentication()
def respondRequest(request,req_id,action):
        req_obj=Requests.objects.filter(requested_to=request.session['ssk_logged_user_id']).filter(id=req_id).get()
        print('obj',req_obj)
        if action=='0':   #accept the request
            req_obj.status=2
            req_obj.save()
            return redirect('/req-received')
        elif action=='1':   
            data={'redirect_url':'/req-received','message':None}
            amount=req_obj.amount
            receiving_user_obj=req_obj.requested_by
            sending_user_obj=req_obj.requested_to
            sending_charge=float(getChargableAmount(sending_user_obj,amount,-1))
            receiving_charge=float(getChargableAmount(receiving_user_obj,amount,1))
            if not isUserHasEnoughBalance(sending_user_obj,amount,sending_charge,-1):
               data['message']='You dont have enough balance to send amount'
               return render(request, 'alert.html', data)
            if not isUserHasEnoughBalance(receiving_user_obj,amount,receiving_charge, 1):
                data['message']='Receiver not have enough balance to receive amount'
                return render(request, 'alert.html', data)
            
            try:
                rec=updateBalanceAndTransactions(receiving_user_obj,amount,receiving_charge,1,req_obj.remark)
                sen=updateBalanceAndTransactions(sending_user_obj,amount,sending_charge,-1,req_obj.remark)
                if rec[0] and sen[0]:
                    rec[1].save()
                    sen[1].save()
                    rec[2].save()
                    sen[2].save()
                    req_obj.status=1
                    req_obj.save()
                    # return HttpResponse('here -3')
                    data['message']='Amount sent sucessfuly '
                    return render(request, 'alert.html', data)
                else:
                    data['message']='Sorry!, we are unable to process the request'
                    # return HttpResponse('here -4')
                    # return redirect('/req-received')
                    # data.update({'status':False,'message':'Sorry!, we are unable to process the request'})
                    return render(request, 'alert.html', data)
            except Exception as e:
                data['message']=f'Sorry!, we are unable to process the request,{str(e)}'
                # return HttpResponse('here -5')
                # return redirect('/req-received')
                # data.update({'status':False,'message':f'Sorry!, we are unable to process the request,{str(e)}'})
                return render(request, 'alert.html', data)
                # return redirect('/req-received')
        else:
            return redirect('/req-received')
        