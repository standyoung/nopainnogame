from django.contrib import admin
from rental.models import *
from django_summernote.admin import SummernoteModelAdminMixin
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay


# Register your models here.


class DeviceValuesAdmin(admin.ModelAdmin):
    list_display = ['values', 'platform']


class RentalDeviceAdmin(SummernoteModelAdminMixin, admin.ModelAdmin):
    list_display = ['device_id', 'device_name', 'device_pub', 'device_image', 'device_value', 'device_state', 'device_rfee', 'device_check',]
    summernote_fields = ('device_description',)


class DeviceRentalAdmin(admin.ModelAdmin):
    list_display = ['device_rental_id', 'device_id', 'member_id', 'daddress', 'drental_date', 'overdue', 'dreturn_date']

    def changelist_view(self, request, extra_context=None):
        # Aggregate new subscribers per day
        chart_data = (
            DeviceRental.objects.annotate(date=TruncDay("drental_date"))
                .values("date")
                .annotate(y=Count("device_id"))
                .order_by("-date")
        )

        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)


class DeviceReserveAdmin(admin.ModelAdmin):
    list_display = ['device_reserve_id', 'device_id', 'member_id', 'device_reserve_date', 'device_due_date']


class GameRentalAdmin(admin.ModelAdmin):
    list_display = ['game_rental_id', 'game_id', 'member_id', 'gaddress', 'grental_date', 'overdue', 'greturn_date']

    def changelist_view(self, request, extra_context=None):
        # Aggregate new subscribers per day
        chart_data = (
            GameRental.objects.annotate(date=TruncDay("grental_date"))
                .values("date")
                .annotate(y=Count("game_id"))
                .order_by("-date")
        )

        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)


class GenreAdmin(admin.ModelAdmin):
    list_display = ['genre', 'type_id']


class RentalGameAdmin(SummernoteModelAdminMixin, admin.ModelAdmin):
    list_display = ['game_id', 'game_name', 'genre', 'game_image', 'release_date', 'device_value', 'game_stock', 'game_rfee',]
    summernote_fields = ('game_description',)


class GameReserveAdmin(admin.ModelAdmin):
    list_display = ['game_reserve_id', 'game_id', 'member_id', 'game_reserve_date', 'game_due_date']


admin.site.register(RentalDevice, RentalDeviceAdmin)
admin.site.register(DeviceValues, DeviceValuesAdmin)
admin.site.register(DeviceRental, DeviceRentalAdmin)
admin.site.register(DeviceReserve, DeviceReserveAdmin)

admin.site.register(Genre, GenreAdmin)
admin.site.register(RentalGame, RentalGameAdmin)
admin.site.register(GameRental, GameRentalAdmin)
admin.site.register(GameReserve, GameReserveAdmin)