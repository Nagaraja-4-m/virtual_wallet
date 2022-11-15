from django.db import models
from authentication.models import Users

# Create your models here.
class Transactions(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.ForeignKey(Users, related_name='user_transactions', on_delete=models.DO_NOTHING)
    date=models.DateTimeField(auto_now=True)
    amount=models.FloatField()
    transfer_type=models.CharField(max_length=16)
    balance=models.FloatField()
    remark=models.CharField(max_length=1024)

    class Meta:
        db_table='transactions'

class Balance(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.OneToOneField(Users, blank=False, on_delete=models.DO_NOTHING)
    # user=models.ForeignKey(Users,unique=True,on_delete=models.DO_NOTHING)
    last_updated=models.DateTimeField(auto_now=True)
    balance=models.FloatField(default=0.0)

    class Meta:
        db_table='balances'

class Requests(models.Model):
    id=models.AutoField(primary_key=True)
    amount=models.FloatField()
    requested_by=models.ForeignKey(Users, related_name='user_money_requests', on_delete=models.DO_NOTHING)
    requested_to=models.ForeignKey(Users, related_name='user_requests', on_delete=models.DO_NOTHING)
    date=models.DateTimeField(auto_now=True)
    status=models.SmallIntegerField(default=0)  
    remark=models.CharField(max_length=1024, default='Send this much of amount')

    ########
    ''' STATUS: 
    0--> Requested 
    1 --> Accepted / sent 
    2 --> Denied 
    '''
    
    class Meta:
        db_table='requests'