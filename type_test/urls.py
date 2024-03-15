from django.urls import path
from .views import *

app_name = 'type_test'

urlpatterns = [
    path('', type_test, name='type_test'),
    path('type_1/', type_1, name='type_1'),
    path('type_2/', type_2, name='type_2'),
    path('type_3/', type_3, name='type_3'),
    path('type_4/', type_4, name='type_4'),
]