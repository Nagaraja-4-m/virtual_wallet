from django.db import models

# Create your models here.

class Users(models.Model):
    id=models.AutoField(primary_key=True)
    email=models.EmailField()
    fullname=models.CharField(max_length=512)
    user_type=models.CharField(max_length=32)
    status=models.SmallIntegerField(default=1)
    password=models.CharField(max_length=128)

    class Meta:
        db_table='users'


