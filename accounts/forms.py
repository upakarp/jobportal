from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from accounts import models
from accounts.models import UpdateProfile
from home.models import Post


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True),

    class Meta:
        model = User
        fields=(
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        #user.password = self.cleaned_data['password']

        if commit:
            user.save()

        return user

class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password'
        )

class UpdateProfileForm(forms.ModelForm):

    class Meta:
        model = UpdateProfile
        fields = (
            'city',
            'description',
            'website',
            'phone',
            'images'
        )

class SearchForm(forms.ModelForm):
    search_text = forms.CharField(max_length=200)