from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^public_chat/$', views.PublicPost , name='post'),
    url(r'^msgs/$', views.PublicMessages, name='msgs'),

]