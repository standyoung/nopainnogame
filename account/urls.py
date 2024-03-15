from django.urls import path
from account.views import *

app_name = 'account'

urlpatterns = [
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('login/', login, name='login'),
    path('find_id/', find_id, name='find_id'),
    path('find_pw/', find_pw, name='find_pw'),
]