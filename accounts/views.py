from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import RegistrationForm, EditProfileForm, UpdateProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.postgres.search import SearchVector
from home.models import Post
from accounts.models import UpdateProfile

# Create your views here.

def home(request):
    return render(request, 'base.html')

def search():
    pass

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('accounts:home'))
    else:
        form = RegistrationForm()

    args = {'form': form}
    return render(request, 'accounts/reg_form.html', args)

def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user

    args = {'user': user}
    return render(request, 'accounts/profile.html', args)

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect(reverse('accounts:profile'))
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'accounts/edit_profile.html', args)

@login_required()
def update_profile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST)

        if form.is_valid():
            form.user = request.user
            form.description = request.POST['description']
            form.city = request.POST['city']
            form.website = request.POST['website']
            form.phone = request.POST['phone']
            UpdateProfile.objects.create(user=form.user, description=form.description, city=form.city, website=form.website, phone=form.phone)
            return redirect(reverse('home:home'))
    else:
        form = UpdateProfileForm(instance=request.user)
        args = {'form':form}
        return render(request, 'accounts/update_profile.html', args)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('accounts:profile'))
        else:
            return redirect(reverse('accounts:change_password'))

    else:
        form = PasswordChangeForm(user=request.user)

        args={'form': form}
        return render(request, 'accounts/change_password.html', args)