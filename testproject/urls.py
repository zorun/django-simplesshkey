from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^', include('simplesshkey.urls', namespace='simplesshkey')),
    url(r'^admin/', admin.site.urls),
]
