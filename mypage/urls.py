from django.urls import path
from .views import *

app_name = 'mypage'

urlpatterns = [
    path('mypage_user', mypage_user, name='mypage'),
    path('mypage_useredit', mypage_useredit, name='mypage_useredit'),
    path('mypage_game', mypage_game, name='mypage_game'),
    path('mypage_device', mypage_device, name='mypage_device'),
    path('mypage_like', mypage_like, name='mypage_like'),
    path('mypage_like/game/<int:g_id>', mypage_Gdislike, name='mypage_Gdislike'),
    path('mypage_like/device/<int:d_id>', mypage_Ddislike, name='mypage_Ddislike'),
    path('dreserve_delete/<int:drs_id>', dreserve_delete, name='dreserve_delete'),
    path('device_return/<int:dr_id>', device_return, name='device_return'),
    path('greserve_delete/<int:grs_id>', greserve_delete, name='greserve_delete'),
    path('game_return/<int:gr_id>', game_return, name='game_return'),
    path('mypage_board', mypage_board, name='mypage_board'),
]