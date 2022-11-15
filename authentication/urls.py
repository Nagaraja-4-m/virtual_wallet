
from django.urls import path
from . import views

urlpatterns = [
    path('login',views.login, name='user_login'),
    path('register',views.registration, name='user_regisration'),
    path('logout',views.logout, name='user_logout'),
]
