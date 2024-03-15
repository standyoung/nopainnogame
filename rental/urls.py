from django.urls import path
from rental.views import *

app_name = 'rental'

urlpatterns = [
    path('device/list/', device_list, name='device_list_all'),
    path('device/list/<d_values>', device_list, name='device_list'),
    path('device/like/<int:d_id>/', device_like, name="device_like"),
    path('device/<int:d_id>/<d_name>/detail', device_detail, name='device_detail'),
    path('device/<int:d_id>/rent', device_rental, name='device_rental'),
    path('device/<int:d_id>/reserve', device_reserve, name='device_reserve'),
    path('game/list/', game_list, name='game_list_all'),
    path('game/list/device/<g_device>', game_list, name='game_list'),
    path('game/list/genre/<g_genre>', game_list, name='game_list_genre'),
    path('game/like/<int:g_id>/', game_like, name="game_like"),
    path('game/<g_id>/', game_detail, name='game_detail'),
    path('game/<g_id>/rent', game_rental, name='game_rental'),
    path('game/<int:g_id>/reserve', game_reserve, name='game_reserve'),
    path('rental_done', rental_done, name='rental_done'),
    path('reserve_done', reserve_done, name='reserve_done'),
]