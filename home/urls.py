from django.conf.urls import url
from home.views import HomeView, BidView
from home import views

urlpatterns =[
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    #url(r'^post/(?P<pk>\d+)/bid/$', views.bid_form, name='bid_form'),
    url(r'^post/(?P<pk>\d+)/bid/$', BidView.as_view(), name='bid_form'),
    url(r'^post/(?P<pk>\d+)/(?P<pk_alt>\d+)/$', views.bid_show, name='bid_show'),
    url(r'^connect/(?P<operation>.+)/(?P<pk>\d+)/$', views.change_friends, name='change_friends')
]
