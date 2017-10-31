from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import RegistrationForm, EditProfileForm, UpdateProfileForm, SearchForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.postgres.search import SearchVector

from home.forms import ReviewForm
from home.models import Post, Rate
from accounts.models import UpdateProfile

# Create your views here.

def home(request):
    return render(request, 'base.html')

def search(request):
    # if request.method == 'POST':
    #     form = SearchForm(request.POST)
    #
    #     if form.is_valid():
    #         search_item = Post.objects.filter(text_search = 'i need a freelancer')
    #
    # else:
    #     form = SearchForm()
    #
    # # search_item = Post.objects.filter(text_search = 'i need a freelancer')
    # return render(request, 'base.html' , {'form':form, 'search_item':search_item})
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
        #userprofile = get_object_or_404(UpdateProfile, user=User.objects.get(pk=pk))
        # try:
        #     userprofile = get_object_or_404(UpdateProfile, user=User.objects.get(pk=pk))
        # except ObjectDoesNotExist:
        #     userprofile = None

        if(get_object_or_404(UpdateProfile, user=User.objects.get(pk=pk)) is None):
            userprofile = UpdateProfile.objects.get_or_create(user=User.objects.get(pk=pk))
        else :
            userprofile = get_object_or_404(UpdateProfile, user=User.objects.get(pk=pk))

        if request.method == 'POST':
            form = ReviewForm(request.POST)

            if form.is_valid():
                rate = form.save(commit=False)
                rate.reviewed_user = User.objects.get(pk=pk)
                rate.reviewed_by = request.user
                rate.save()
                return redirect('home:home')
        else:
            form = ReviewForm()

    else:
        form = {}
        user = request.user
        userprofile = get_object_or_404(UpdateProfile, user=request.user)

    rate = Rate.objects.filter(reviewed_user = user.pk)
    present_review = 0
    count = 0
    for rates in rate:
        present_review = present_review + rates.review_number
        count = count + 1

    if count > 0:
        total_review = present_review / count
    else:
        total_review = 0

    args = {'user': user, 'userprofile':userprofile, 'form':form, 'total_review': total_review, }
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
        form = UpdateProfileForm(request.POST, request.FILES)

        if form.is_valid():
            form.user = request.user
            form.description = request.POST['description']
            form.city = request.POST['city']
            form.website = request.POST['website']
            form.phone = request.POST['phone']
            form.images = request.FILES['images']
            UpdateProfile.objects.create(user=form.user, description=form.description, city=form.city, website=form.website, phone=form.phone, images=form.images)
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