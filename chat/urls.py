from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^ground$', views.chat , name='chat'),
    # url(r'^msgs/$', views.PublicMessages, name='msgs'),

]