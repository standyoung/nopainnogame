from django.contrib import admin
from account.models import User
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('member_name', 'member_id', 'password', 'address', 'phone', 'overdue', 'type_id')

    search_fields = ['member_id']
    list_filter = ('type_id',)


admin.site.register(User, UserAdmin)