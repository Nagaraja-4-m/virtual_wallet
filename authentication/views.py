from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import *
from wallet.models import Balance
from .functions import *
from .auth_decorators import check_authentication

dashboard_template='wallet/templates/'

PremiumUser_AutoCredit=2500
NonPremiumUser_AutoCredit=1000

# Create your views here.
def login(request):

    if 'ssk_logged_user_id' in request.session:
        return redirect('/')


    if request.method=='POST':
        user_data=request.POST.dict()
        data={'redirect_url':'/','message':None}
        # email_varification_status=
        if not is_email_exist(user_data['email']):
            data['message']=f'{user_data["email"]} not found!'
            return render(request,'alert.html',data)
        try:
            user_obj=Users.objects.filter(email__iexact=user_data['email']).get()
            if user_data['password']==user_obj.password:
                request.session['ssk_logged_user_id'] = user_obj.id  #session created
                return redirect('/')
            else:
                data['message']='Invalid password !'
                return render(request,'alert.html',data)
        except:
            data['message']='Unable to verify email!'
            return render(request,'alert.html',data)
    else:
        return redirect('/')


def registration(request):

    if request.method=='POST':
        user_data=request.POST.dict()
        
        email_varification_status=is_email_exist(user_data['email'])
        data={'redirect_url':'/','message':None}
        if email_varification_status:
            data['message']=f'{user_data["email"]} already exists!'
            return render(request,'alert.html',data)
        elif email_varification_status is None:
            data['message']='Unable to verify email!'
            return render(request,'alert.html',data)
        try:
            if user_data['user_type']=='premium':
                balance=PremiumUser_AutoCredit
            elif user_data['user_type']=='non-premium':
                balance=NonPremiumUser_AutoCredit
            user_object=Users(
                    email=user_data['email'],
                    fullname=user_data['fullname'],
                    user_type=user_data['user_type'],
                    password=user_data['password'] )
            balance_obj=Balance(
                    user=user_object,
                    balance=balance  )
            user_object.save()
            balance_obj.save()
            
            request.session['ssk_logged_user_id'] = user_object.id  #session created

        except Exception as e:
            print(str(e))
            data['message']=f'Uanble to complete the request, Error: {str(e)}'
            return render(request,'alert.html',data)

        return redirect('/')

    else:
        return redirect('/')

# @check_authentication
def logout(request):
    try:
        request.session.pop('ssk_logged_user_id')
    except:
        del request.session
    return redirect('/')