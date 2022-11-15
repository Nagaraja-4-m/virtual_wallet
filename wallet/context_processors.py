from authentication.models import Users

def loadUserdata(request):
    try:
        user_Id=request.session['ssk_logged_user_id']
        user_Data=Users.objects.filter(id=user_Id).values('id','fullname','email')[0]
        user_Data.update({'isAuthenticated':True})
        return {'logged_user':user_Data}
    except (KeyError,IndexError):
        pass
    except Exception as e:
        print(f':::: Error occured ::::\nfile path: {__file__}, loadUserdata() \n Error desc: {str(e)}')
    return {}