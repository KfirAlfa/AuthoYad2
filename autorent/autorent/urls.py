
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^houses/', include('houses.urls')),
    url(r'^admin/', admin.site.urls),
    ]
