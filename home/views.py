from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from accounts.models import UpdateProfile
from home.forms import HomeForm, BidForm, ReviewForm
from home.models import Post, Friend, Bid, Rate
from django.utils import timezone

class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get(self, request):
        form = HomeForm()
        posts = Post.objects.exclude(user=request.user).order_by('-created')
        myPost = Post.objects.filter(user=request.user).order_by('-created')
        users = User.objects.exclude(id=request.user.id)
        try:
            userprofile = UpdateProfile.objects.get(user=request.user)
        except UpdateProfile.DoesNotExist:
            userprofile = None

        # friend = get_object_or_404(Friend, current_user=request.user)
        # friends = friend.user.all()

        args= {'form':form, 'posts':posts, 'users':users,  'myPost':myPost, 'userprofile':userprofile}
        return render(request, self.template_name, args)


    def post(self, request):
        form = HomeForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            title = form.cleaned_data['title']
            text = form.cleaned_data['post']
            form = HomeForm()
            return redirect('home:home')

        args = {'form':form, 'text':text, 'title':title }
        return render(request, self.template_name, args)

def change_friends(request, operation, pk):
    new_friend = User.objects.get(pk=pk)
    if operation == 'add':
        Friend.make_friend(request.user, new_friend)
    elif operation == 'remove':
        Friend.lose_friend(request.user, new_friend)
    return redirect('home:home')

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    bid = Bid.objects.filter(link_post = pk)
    user = request.user
    bid_accepted = None
    for bids in bid:
        if bids.is_accepted == True:
            bid_accepted = bids.is_accepted
    try:
        userprofile = UpdateProfile.objects.get(user=request.user)
    except UpdateProfile.DoesNotExist:
        userprofile = None

    args = {'post':post, 'bid':bid, 'userprofile':userprofile, 'bid_accepted':bid_accepted, 'user':user}
    return render(request, 'home/post_detail.html', args)

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    try:
        userprofile = UpdateProfile.objects.get(user=request.user)
    except UpdateProfile.DoesNotExist:
        userprofile = None
    if request.method == 'POST':
        form = HomeForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.created = timezone.now()
            post.save()
            messages.success(request, 'Post was edited successfully')
            return redirect('home:post_detail', pk=post.pk)
        else:
            messages.warning(request, 'Please fill up the form')
    else:
        form = HomeForm(instance = post)
    return render(request, 'home/post_edit.html', {'form':form, 'userprofile':userprofile})

# def bid_form(request, pk):
#     #bid = get_object_or_404(Bid, pk=pk)
#     if request.method == 'POST':
#         form = BidForm(request.POST) #instance=bid)
#         if form.is_valid():
#             bid = form.save(commit=False)
#             bid.save()
#             return redirect('home:post_detail') #, pk=bid.pk)
#     else:
#         form = BidForm() #instance=bid)
#     return render(request, 'home/bid_form.html', {'form': form})

class BidView(TemplateView):

    template_name = 'home/bid_form.html'

    def get(self, request, **kwargs):
        form = BidForm()
        try:
            userprofile = UpdateProfile.objects.get(user=request.user)
        except UpdateProfile.DoesNotExist:
            userprofile = None

        args = {'form':form, 'userprofile':userprofile}
        return render(request, self.template_name, args)

    def post(self, request, pk, **kwargs):
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.link_user = request.user
            bid.link_post = Post.objects.get(pk=pk)
            bid.save()
            form = BidForm()
            messages.success(request, "Bid was successful")
            return redirect('home:home')

        try:
            userprofile = UpdateProfile.objects.get(user=request.user)
        except UpdateProfile.DoesNotExist:
            userprofile = None

        args = {'form' : form, 'userprofile':userprofile}
        return render(request, self.template_name, args)

def bid_show(request, pk, pk_alt):
    post = get_object_or_404(Post, pk=pk)
    bid = get_object_or_404(Bid, pk=pk_alt)
    try:
        userprofile = UpdateProfile.objects.get(user=request.user)
    except UpdateProfile.DoesNotExist:
        userprofile = None

    if request.method == 'POST':
        bid.is_accepted = True
        if bid.is_accepted == True:
            post.is_bidded = True
            post.who_bidded = bid.link_user
            post.save()
        bid.save()
        return redirect('home:home')
    args = {'bid':bid, 'post':post, 'userprofile':userprofile}
    return render(request, 'home/bid_show.html', args)

# def friend(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if post.is_bidded == True:
#         userid = post.who_bidded
#
#     return render(request, 'home/home.html', userid)

# def rate(request, pk):
#     rate = Rate.objects.filter(pk=pk)
#     if request.method == 'POST':
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             rate = form.save(commit=False)
#
#             rate.save()
#             return redirect('home:home')
#     else:
#         form = ReviewForm()
#     return render(request, 'home/rate.html', {'form':form })

class RateView(TemplateView):

    template_name = 'accounts/profile.html'

    def get(self, request, **kwargs):
        form = ReviewForm()
        try:
            userprofile = UpdateProfile.objects.get(user=request.user)
        except UpdateProfile.DoesNotExist:
            userprofile = None
        args = {'form':form, 'userprofile':userprofile}
        return render(request, self.template_name, args)

    def post(self, request, pk, **kwargs):
        form = ReviewForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.reviewed_user = User.objects.get(pk=pk)
            rate.reviewed_by = request.user
            rate.save()
            form = ReviewForm()
            messages.success("Reviewed user successful")
            return redirect('home:home')

        try:
            userprofile = UpdateProfile.objects.get(user=request.user)
        except UpdateProfile.DoesNotExist:
            userprofile = None
        args = {'form' : form, 'userprofile':userprofile}
        return render(request, self.template_name, args)

def rate_show(request, pk):
    rate = get_object_or_404(Rate)
    try:
        userprofile = UpdateProfile.objects.get(user=request.user)
    except UpdateProfile.DoesNotExist:
        userprofile = None

    args = {'rate':rate, 'userprofile':userprofile}
    return render(request, 'home/rate_show.html', args)

def my_job(request):
    myJob = Post.objects.filter(user=request.user).order_by('-created')
    try:
        userprofile = UpdateProfile.objects.get(user=request.user)
    except UpdateProfile.DoesNotExist:
        userprofile = None
    args = {'myJob': myJob, 'userprofile':userprofile}
    return render(request, 'home/myJob.html', args)

def post_job(request):
    if request.method == 'POST':
        form = HomeForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            # title = form.cleaned_data['title']
            # text = form.cleaned_data['post']
            form = HomeForm()
            return redirect('home:home')
    else:
        form = HomeForm()

    try:
        userprofile = UpdateProfile.objects.get(user=request.user)
    except UpdateProfile.DoesNotExist:
        userprofile = None
    args = {'form': form, 'userprofile':userprofile}
    return render(request, 'home/post_job.html', args)

def map(request):
    try:
        userprofile = UpdateProfile.objects.get(user=request.user)
    except UpdateProfile.DoesNotExist:
        userprofile = None
    latitude = None
    longitude = None

    try:
        if userprofile.city == 'Pokhara' or userprofile.city == 'pokhara':
            latitude = 28.237987
            longitude = 83.9955879

        if userprofile.city == 'Kathmandu' or userprofile.city == 'kathmandu':
            latitude = 27.7172453
            longitude = 85.3239605

        if userprofile.city == 'Chitwan' or userprofile.city == 'chitwan':
            latitude = 27.5291
            longitude = 84.3542
    except:
        userprofile = None

    args = {'userprofile':userprofile, 'latitude':latitude, 'longitude':longitude}
    return render(request, 'home/map.html', args)

def paypal_return(request):
    return render(request, 'home/thanks.html')

@csrf_exempt
def verify_phone(request):
    try:
        userprofile = UpdateProfile.objects.get(user=request.user)
    except UpdateProfile.DoesNotExist:
        userprofile = None

    return render(request, 'home/verify_phone.html', {'userprofile':userprofile})