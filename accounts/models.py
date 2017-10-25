from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

class UserProfileManager(models.Manager):
    def get_queryset(self):
        return super(UserProfileManager, self).get_queryset()

class UpdateProfile(models.Model):
    user = models.OneToOneField(User)
    description = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    website = models.URLField(default='')
    phone = models.IntegerField(default=0)
    images = models.ImageField(upload_to='profile_image', blank=True, null=True)

#     def __str__(self):
#         return self.user.username
#

# def create_profile(sender, **kwargs):
#     user = kwargs["instance"]
#     if kwargs["created"]:
#         user_profile = UserProfile(user=user)
#         user_profile.save()
# post_save.connect(create_profile, sender=User)

