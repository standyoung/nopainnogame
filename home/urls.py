from django.urls import path
from .views import *

app_name = 'home'

urlpatterns = [
    path('', home, name='home'),
    path('how_to', how_to, name='how_to'),
    path('how_to_clean', how_to_clean, name='how_to_clean'),
    path('how_to_pick', how_to_pick, name='how_to_pick'),
]