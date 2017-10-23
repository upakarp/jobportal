from django import forms
from home.models import Post, Bid, Rate

from django.contrib.auth.models  import User


class HomeForm(forms.ModelForm):
    post = forms.CharField(widget=forms.TextInput(
        attrs = {
            'class':'form-control',
            'placeholder':'Write post',
        }
    ))
    title = forms.CharField()

    class Meta:
        model = Post
        fields = ('title' ,'post',)

class BidForm(forms.ModelForm):

    class Meta:
        model = Bid
        fields = ('amount', 'description',)

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Rate
        fields = ('review_number', 'review',)



