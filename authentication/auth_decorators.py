from django.shortcuts import redirect

#Authentication verification
def  check_authentication(view_func):
    def wrapper_funct(request,*args,**kwargs):
        if 'ssk_logged_user_id' in request.session:
            return view_func(request,*args,**kwargs)
        else:
            return redirect('/')

    return wrapper_funct