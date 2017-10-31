from django import forms
from home.models import Post, Bid, Rate

from django.contrib.auth.models  import User


class HomeForm(forms.ModelForm):
    post = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Write post',
        }
    ))
    title = forms.CharField()

    LOCATION_CHOICE = (('Kathmandu', 'Kathmandu'), ('Pokhara', 'Pokhara'), ('Pokhara', 'Chitwan'))
    location = forms.ChoiceField(widget=forms.Select, choices=LOCATION_CHOICE)

    class Meta:
        model = Post
        fields = ('title', 'post', 'amount', 'location', 'is_online', 'deadline')

class BidForm(forms.ModelForm):

    class Meta:
        model = Bid
        fields = ('amount', 'description',)

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Rate
        fields = ('review_number', 'review',)



