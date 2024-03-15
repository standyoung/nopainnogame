from django.contrib import admin
from board.models import *

# Register your models here.


class PostTypeAdmin(admin.ModelAdmin):
    list_display = ('p_type',)


class PostAdmin(admin.ModelAdmin):
    list_display = ('member_id', 'post_date', 'postname', 'p_type', 'contents')


admin.site.register(Post, PostAdmin)
admin.site.register(PostType, PostTypeAdmin)