from django.urls import path
from .views import *

app_name = 'board'

urlpatterns = [
    path('', board, name='board'),
    path('write', board_write, name='board_write'),
    path('postwrite', board_write_post, name='board_write_post'),
    path('delete/<p_id>', board_delete, name='board_delete'),
    path('edit/<p_id>', board_edit, name='board_edit'),
    path('<p_type>', board, name='board'),
    path('detail/<id>', board_detail, name='board_detail'),
]