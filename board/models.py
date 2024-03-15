from django.db import models
from django.urls import reverse

from account.models import User


# Create your models here.
class PostType(models.Model):
    p_type = models.CharField(max_length=200, db_index=True)

    def __str__(self):
        return self.p_type

    def get_ptype_url(self):
        return reverse('board:board', args=[self.p_type])


class Post(models.Model):
    member_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='board_id')
    p_type = models.ForeignKey(PostType, on_delete=models.SET_NULL, null=True)
    post_date = models.DateTimeField(auto_now_add=True)
    postname = models.CharField(max_length=100)
    contents = models.TextField()

    class Meta:
        ordering = ['-post_date']

    def __str__(self):
        return self.postname

    def get_post_url(self):
        return reverse('board:board_detail', args=[self.id])