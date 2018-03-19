"""jobportal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from jobportal import views
from rest_framework import routers
from restApi import views as rest_view

router = routers.DefaultRouter()
router.register(r'rest_users', rest_view.UserViewSet)
router.register(r'rest_user_profile', rest_view.UserProfileViewSet)
router.register(r'rest_post', rest_view.PostViewSet)
router.register(r'rest_bid', rest_view.BidViewSet)
router.register(r'rest_rate', rest_view.RateViewSet)

urlpatterns = [
    url(r'^$', views.index, name='index'),
    #url(r'^admin/', admin.site.urls),
    #url(r'account/', include('accounts.urls', namespace='accounts')),
    #url(r'home/', include('home.urls', namespace='home')),
    #url(r'^chat/', include('chat.urls', namespace='chat')),

    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

#if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

