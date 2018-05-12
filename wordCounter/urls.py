"""wordCounter URL Configuration
urls rout is under each app
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^wordcounter/', include('wordCounterPost.urls')),
    url(r'^wordstatistics', include('wordStatistics.urls'))
]





# from django.contrib import include, admin
# from django.urls import path
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path(r'^wordCounter/', include()),
# ]

