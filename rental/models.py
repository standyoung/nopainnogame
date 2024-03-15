from datetime import datetime, timedelta

from django.db import models
from django.urls import reverse
# Create your models here.
from django_random_queryset import RandomManager

from account.models import User


class DeviceValues(models.Model):
    platform_choice = (
        ('PS', 'PlayStaion'),
        ('ND', 'Nintendo'),
    )

    values = models.CharField(max_length=200, null=False, db_index=True)
    platform = models.CharField(max_length=2, null=True, choices=platform_choice)

    def __str__(self):
        return self.values

    def get_absolute_url(self):
        return reverse('rental:device_list', args=[self.values])

    def get_gdabsolute_url(self):
        return reverse('rental:game_list', args=[self.values])


class RentalDevice(models.Model):
    state_choice = (
        ('매우좋음', '매우좋음'),
        ('좋음', '좋음'),
        ('보통', '보통'),
    )
    check_choice = (
        (0, '대여가능'),
        (1, '대여중'),
    )
    device_id = models.IntegerField(unique=True, null=False, primary_key=True)
    device_name = models.CharField(max_length=40, null=False,)
    device_pub = models.DateField()
    device_image = models.ImageField(upload_to='static/device/', null=False, blank=True)
    device_value = models.ForeignKey(DeviceValues, on_delete=models.SET_NULL, null=True, related_name='devices')
    device_state = models.CharField(max_length=10, choices=state_choice)
    device_rfee = models.IntegerField()
    device_check = models.IntegerField(default=0, choices=check_choice)
    device_description = models.TextField(max_length=500)
    device_like = models.ManyToManyField(User, related_name='device_like', blank=True)

    class Meta:
        ordering = ['device_id']

    def __str__(self):
        return self.device_name

    def get_dabsolute_url(self):
        return reverse('rental:device_detail', args=[self.device_id, self.device_name])

    def get_drental_url(self):
        return reverse('rental:device_rental', args=[self.device_id])

    def get_dreserve_url(self):
        return reverse('rental:device_reserve', args=[self.device_id])


class Genre(models.Model):
    choice_type = (
        (1, '1: speed'),
        (2, '2: simple'),
        (3, '3: competition'),
        (4, '4: explorer'),
    )

    genre = models.CharField(max_length=20, db_index=True)
    type_id = models.IntegerField(choices=choice_type)

    def __str__(self):
        return self.genre

    def get_absolute_url(self):
        return reverse('rental:game_list_genre', args=[self.genre])


class RentalGame(models.Model):
    game_id = models.IntegerField(unique=True, primary_key=True)
    game_name = models.CharField(max_length=40)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, related_name='games')
    game_image = models.ImageField(upload_to='static/game/', null=False, blank=True)
    release_date = models.DateField()
    device_value = models.ForeignKey(DeviceValues, on_delete=models.SET_NULL, null=True, related_name='games')
    game_stock = models.IntegerField()
    game_rfee = models.IntegerField()
    game_description = models.TextField(max_length=500)
    game_like = models.ManyToManyField(User, related_name='game_like', blank=True)
    game_video = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ['game_id', '-device_value', '-genre']

    def __str__(self):
        return self.game_name

    def get_gabsolute_url(self):
        return reverse('rental:game_detail', args=[self.game_id])

    def get_grental_url(self):
        return reverse('rental:game_rental', args=[self.game_id])

    def get_greserve_url(self):
        return reverse('rental:game_reserve', args=[self.game_id])


def get_drental_date():
    return datetime.now().date() + timedelta(days=1)


class DeviceRental(models.Model):
    device_rental_id = models.IntegerField(unique=True, primary_key=True)
    device_id = models.ForeignKey(RentalDevice, on_delete=models.CASCADE, null=False, related_name='dRentals_id')
    member_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='dRentals_id')
    daddress = models.CharField(max_length=60, null=False)
    drental_date = models.DateField(default=get_drental_date, editable=False)
    overdue = models.IntegerField(null=True, blank=True)
    dreturn_date = models.DateField(null=True)

    class Meta:
        ordering = ['device_rental_id']


class DeviceReserve(models.Model):
    device_reserve_id = models.IntegerField(unique=True, primary_key=True)
    device_id = models.ForeignKey(RentalDevice, on_delete=models.CASCADE, null=False, related_name='dReserve_d_id')
    member_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='dReserve_m_id')
    device_reserve_date = models.DateField(auto_now_add=True) #예약한 날짜
    device_due_date = models.DateField() #대여예정일

    class Meta:
        ordering = ['device_reserve_id']


class GameRental(models.Model):
    game_rental_id = models.IntegerField(unique=True, primary_key=True)
    game_id = models.ForeignKey(RentalGame, on_delete=models.CASCADE, null=False, related_name='gRentals_id')
    member_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='gRentals_id')
    gaddress = models.CharField(max_length=60, null=False)
    grental_date = models.DateField(default=get_drental_date, editable=False)
    overdue = models.IntegerField(null=True, blank=True)
    greturn_date = models.DateField(null=True)

    class Meta:
        ordering = ['game_rental_id']


class GameReserve(models.Model):
    game_reserve_id = models.IntegerField(unique=True, primary_key=True)
    game_id = models.ForeignKey(RentalGame, on_delete=models.CASCADE, null=False, related_name='gReserve_g_id')
    member_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='gReserve_m_id')
    game_reserve_date = models.DateField(auto_now_add=True) #예약한 날짜
    game_due_date = models.DateField() #대여예정일

    class Meta:
        ordering = ['game_reserve_id']