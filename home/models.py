from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.contenttypes.models import ContentType

class Post(models.Model):
    title = models.CharField(max_length=50, null=True)
    post = models.TextField()
    user = models.ForeignKey(User)
    amount = models.PositiveIntegerField(default=0)
    location = models.CharField(max_length=100, null=True)
    is_online = models.BooleanField(default=False)
    deadline = models.DateTimeField(null=True)
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

class Rate(models.Model):
    review_number = models.IntegerField(null=True, validators=[MinValueValidator(0), MaxValueValidator(5)], default=3)
    reviewed_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    reviewed_by = models.OneToOneField(User, on_delete=models.CASCADE, related_name='reviewing_user', null=True)
    review = models.TextField(null=True)
