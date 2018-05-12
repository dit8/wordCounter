from django.conf.urls import include, url
from . import views

# I use different
urlpatterns = [
    url(r'^$', views.postData, name='postData')
]