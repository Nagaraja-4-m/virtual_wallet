
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='user_dashboard'),
    path('wallet', views.wallet, name='user_wallet'),
    path('send-money', views.sendMoney, name='user_sendmoney'),
    path('req-money', views.reqMoney, name='user_reqmoney'),
    path('req-received', views.reqReceived, name='user_reqreceived'),
    path('req-action/<req_id>/<action>', views.respondRequest, name='req_action'),
    path('test', views.test, name='testt'),
]
