from django import forms
from home.models import Post, Bid


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

