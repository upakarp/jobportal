from django.contrib.auth.models import User, Group
from rest_framework import serializers

from accounts.models import UpdateProfile
from home.models import Post, Bid, Rate


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UpdateProfile
        fields = (
            'user', 'description', 'city', 'website', 'phone', 'images'
        )

class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'post', 'user', 'amount', 'location', 'is_online', 'deadline', 'created', 'updated', 'is_bidded', 'who_bidded')

class BidSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bid
        fields = ('amount', 'description', 'link_user', 'link_post', 'is_accepted')

class RateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rate
        fields = ('review_number', 'reviewed_user', 'reviewed_by', 'review')
