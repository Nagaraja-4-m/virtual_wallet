
from .models import Users
#__________________________________  USER related functions ___________________________________________

def is_email_exist(email):
    try:
        status=Users.objects.filter(email__iexact=email).exists()  #if not exsists RETURNS FALSE'
        return status #means email already exists
    except:
        return None