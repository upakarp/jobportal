from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db import models
from django.contrib.contenttypes.models import ContentType


class Post(models.Model):
    title = models.TextField(null=True)
    post = models.CharField(max_length=500)
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_bidded = models.BooleanField(default=False)
    who_bidded = models.ForeignKey(User, related_name='connected', null=True)

class Friend(models.Model):
    users = models.ManyToManyField(User)
    current_user = models.ForeignKey(User, related_name='owner', null=True)

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user = current_user
        )
        friend.users.add(new_friend)

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_friend)

class Bid(models.Model):
    amount = models.PositiveIntegerField(null=False, default=0)
    description = models.TextField(null=True)
    link_user = models.ForeignKey(User, on_delete=models.CASCADE)
    link_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default = False)
