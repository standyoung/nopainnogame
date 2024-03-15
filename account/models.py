from django.conf import settings
from django.db import models


# Create your models here.
class User(models.Model):
    member_name = models.CharField(max_length=40, null=False)
    member_id = models.CharField(max_length=40, null=False, unique=True)
    password = models.CharField(max_length=40, null=False)
    address = models.CharField(max_length=60, null=False)
    phone = models.CharField(max_length=40, null=False, unique=True)
    overdue = models.IntegerField(default=0)
    type_id = models.IntegerField(null=True)

    def __str__(self):
        return self.member_id
